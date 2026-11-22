"""Python side of the practice kernel.

This file runs inside Pyodide (Python compiled to WebAssembly) in a Web Worker in the user's
browser; it never runs user code on the server. The test suite imports it with CPython to check
that every exercise's reference solution passes its own tests.

Two entry points:
  run_cell(code, ns_key, stdin, emit)  run one notebook cell in a persistent namespace, like Jupyter
  grade(code, groups, emit)            run code in a fresh namespace, then each test assert
"""
import ast
import builtins
import io
import linecache
import sys
import traceback

_namespaces = {}
_cell_counter = [0]
MAX_REPR = 2000


def _fresh_namespace():
    return {"__name__": "__main__", "__builtins__": builtins}


def reset(ns_key=None):
    if ns_key is None:
        _namespaces.clear()
    else:
        _namespaces.pop(ns_key, None)


class _Stream(io.TextIOBase):
    def __init__(self, kind, emit):
        self.kind, self.emit = kind, emit

    def writable(self):
        return True

    def write(self, s):
        if s:
            self.emit(self.kind, s)
        return len(s)


def _register_source(code, label):
    _cell_counter[0] += 1
    filename = f"<{label}-{_cell_counter[0]}>"
    linecache.cache[filename] = (len(code), None, code.splitlines(True), filename)
    return filename


def _short_repr(value):
    text = repr(value)
    return text if len(text) <= MAX_REPR else text[:MAX_REPR] + " …"


def format_exception(exc):
    """Traceback that only shows the user's own frames (cells and tests), not this runner's."""
    tbe = traceback.TracebackException.from_exception(exc)
    tbe.stack = traceback.StackSummary.from_list([f for f in tbe.stack if f.filename.startswith("<")])
    lines = list(tbe.format())
    if lines and lines[0].startswith("Traceback") and not tbe.stack:
        lines = lines[1:]
    return "".join(lines).rstrip("\n")


def _compile_cell(code, filename):
    """Compile a cell; if the last statement is an expression, return it separately so its
    value can be displayed the way a notebook does."""
    tree = ast.parse(code, filename, "exec")
    last = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = ast.Expression(tree.body.pop().value)
    body = compile(tree, filename, "exec")
    return body, (compile(last, filename, "eval") if last is not None else None)


class _Redirect:
    def __init__(self, emit, stdin=""):
        self.emit, self.stdin = emit, stdin

    def __enter__(self):
        self.saved = sys.stdout, sys.stderr, sys.stdin
        sys.stdout = _Stream("stdout", self.emit)
        sys.stderr = _Stream("stderr", self.emit)
        sys.stdin = io.StringIO(self.stdin or "")
        return self

    def __exit__(self, *exc):
        sys.stdout, sys.stderr, sys.stdin = self.saved
        return False


def _input_eof_hint(exc, stdin):
    if isinstance(exc, EOFError) and not stdin:
        return "\n\nThis cell called input(). Type the input lines into the cell's stdin box, then run it again."
    return ""


def run_cell(code, ns_key="default", stdin="", emit=None):
    """Run a cell. Returns {"result": repr of the last expression or None, "error": text or None}."""
    emit = emit or (lambda kind, text: None)
    ns = _namespaces.setdefault(ns_key, _fresh_namespace())
    filename = _register_source(code, "cell")
    try:
        body, last = _compile_cell(code, filename)
    except SyntaxError as exc:
        return {"result": None, "error": format_exception(exc)}
    with _Redirect(emit, stdin):
        try:
            exec(body, ns)
            value = eval(last, ns) if last is not None else None
        except BaseException as exc:  # SystemExit, KeyboardInterrupt included: report, don't die
            return {"result": None, "error": format_exception(exc) + _input_eof_hint(exc, stdin)}
    if value is not None:
        ns["_"] = value
        return {"result": _short_repr(value), "error": None}
    return {"result": None, "error": None}


def _is_simple_equality(stmt):
    t = stmt.test
    return isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(t.ops[0], ast.Eq)


def grade(code, groups, emit=None):
    """Run `code` in a fresh namespace, then the tests.

    groups: list of (kind, source) where kind is "example" (shown to the user) or "hidden".
    Each top-level `assert` in a source is one test. Other statements (imports, setup) run as
    setup and fail the whole run if they raise.

    Returns {"error": text or None, "results": [{"kind", "n", "src", "ok", "got", "expected",
    "message"}], "passed": int, "total": int}.
    """
    emit = emit or (lambda kind, text: None)
    ns = _fresh_namespace()
    filename = _register_source(code, "solution")
    out = {"error": None, "results": [], "passed": 0, "total": 0}
    with _Redirect(emit):
        try:
            exec(compile(code, filename, "exec"), ns)
        except BaseException as exc:
            out["error"] = format_exception(exc)
            return out
    counts = {}
    for kind, source in groups:
        if not source or not source.strip():
            continue
        tree = ast.parse(source, f"<{kind}-tests>", "exec")
        for stmt in tree.body:
            seg = ast.get_source_segment(source, stmt) or ""
            if not isinstance(stmt, ast.Assert):
                mod = ast.Module(body=[stmt], type_ignores=[])
                with _Redirect(emit):
                    try:
                        exec(compile(mod, f"<{kind}-tests>", "exec"), ns)
                    except BaseException as exc:
                        out["error"] = f"Test setup failed: {seg}\n{format_exception(exc)}"
                        return out
                continue
            counts[kind] = counts.get(kind, 0) + 1
            res = {"kind": kind, "n": counts[kind], "src": seg, "ok": False, "got": None, "expected": None, "message": None}
            with _Redirect(emit):
                try:
                    if _is_simple_equality(stmt):
                        got = eval(compile(ast.Expression(stmt.test.left), "<test>", "eval"), ns)
                        expected = eval(compile(ast.Expression(stmt.test.comparators[0]), "<test>", "eval"), ns)
                        res["ok"] = bool(got == expected)
                        if not res["ok"]:
                            res["got"], res["expected"] = _short_repr(got), _short_repr(expected)
                    else:
                        exec(compile(ast.Module(body=[stmt], type_ignores=[]), "<test>", "exec"), ns)
                        res["ok"] = True
                except AssertionError as exc:
                    res["message"] = str(exc) or None
                except BaseException as exc:
                    res["message"] = format_exception(exc)
            out["results"].append(res)
    out["total"] = len(out["results"])
    out["passed"] = sum(1 for r in out["results"] if r["ok"])
    return out
