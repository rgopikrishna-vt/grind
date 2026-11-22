"""Practice exercises are Markdown files in the practice/ folder, one exercise per file.
Drop a new file in to add an exercise. Files are listed in filename order, so prefix them
with a number (e.g. 36-my-exercise.md).

File format:

    ---
    id: two-sum                 # URL-safe and unique
    title: Two Sum
    topic: Dictionaries         # exercises are grouped by topic
    difficulty: easy            # easy | medium | hard
    ---

    ## Prompt
    Markdown: what to build. `inline code`, **bold**, fenced code and "- " bullet lists work.

    ## Starter
    ```python
    def two_sum(nums, target):
        pass
    ```

    ## Examples            (optional) shown to the learner; each `assert` is one test
    ```python
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    ```

    ## Tests               hidden tests, run on Submit after the examples
    ```python
    assert two_sum([3, 3], 6) == [0, 1]
    ```

    ## Hints               (optional) one "- " bullet per hint, revealed one at a time
    - Hint one.
    - Hint two.

    ## Solution
    ```python
    def two_sum(nums, target): ...
    ```

    ## Explanation         (optional) Markdown shown with the solution
"""
import os
import re
from collections import OrderedDict

from flask import current_app

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
DIFFICULTIES = ("easy", "medium", "hard")
SECTION_RE = re.compile(r"^##[ \t]+(.+?)[ \t]*$", re.M)
CODE_RE = re.compile(r"```[\w+-]*[ \t]*\n(.*?)^```", re.S | re.M)
REQUIRED_SECTIONS = ("prompt", "starter", "tests", "solution")


def parse_exercise(text, name="exercise"):
    text = text.replace("\r\n", "\n")
    meta = {}
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end == -1:
            raise ValueError(f"{name}: front matter is not closed with ---")
        for line in text[4:end].splitlines():
            line = line.split(" #", 1)[0].strip()
            if line:
                key, _, value = line.partition(":")
                meta[key.strip().lower()] = value.strip()
        text = text[end + 4:]
    sections = {}
    matches = list(SECTION_RE.finditer(text))
    for i, m in enumerate(matches):
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[m.group(1).strip().lower()] = text[m.end():body_end].strip("\n")

    for field in ("id", "title", "topic", "difficulty"):
        if not meta.get(field):
            raise ValueError(f"{name}: missing '{field}' in front matter")
    if not ID_RE.match(meta["id"]):
        raise ValueError(f"{name}: id must be lowercase letters, digits and dashes")
    if meta["difficulty"] not in DIFFICULTIES:
        raise ValueError(f"{name}: difficulty must be one of {', '.join(DIFFICULTIES)}")
    for s in REQUIRED_SECTIONS:
        if s not in sections:
            raise ValueError(f"{name}: missing '## {s.title()}' section")

    def code(section, required=True):
        body = sections.get(section, "")
        m = CODE_RE.search(body)
        if not m:
            if required:
                raise ValueError(f"{name}: '## {section.title()}' needs a ```python code block")
            return ""
        return m.group(1).rstrip() + "\n"

    hints = []
    for line in sections.get("hints", "").splitlines():
        if line.startswith("- "):
            hints.append(line[2:].strip())
        elif line.strip() and hints:
            hints[-1] += " " + line.strip()

    examples = code("examples", required=False)
    tests = code("tests")
    return {
        "hidden_count": _count_asserts(tests),
        "example_count": _count_asserts(examples),
        "try_snippet": _try_snippet(examples),
        "id": meta["id"],
        "title": meta["title"],
        "topic": meta["topic"],
        "difficulty": meta["difficulty"],
        "prompt": sections["prompt"].strip(),
        "starter": code("starter"),
        "examples": examples,
        "tests": tests,
        "hints": hints,
        "solution": code("solution"),
        "explanation": sections.get("explanation", "").strip(),
    }


def _count_asserts(source):
    import ast
    try:
        return sum(1 for s in ast.parse(source).body if isinstance(s, ast.Assert))
    except SyntaxError:
        return 0


def _try_snippet(examples):
    """The call from the first `assert call == expected` example, to prefill the scratch cell."""
    import ast
    try:
        for stmt in ast.parse(examples).body:
            t = getattr(stmt, "test", None)
            if isinstance(stmt, ast.Assert) and isinstance(t, ast.Compare) and isinstance(t.left, ast.Call):
                return ast.get_source_segment(examples, t.left)
    except SyntaxError:
        pass
    return ""


def load_exercises(directory):
    found = OrderedDict()
    if not os.path.isdir(directory):
        return found
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".md") or name.lower() == "readme.md":
            continue
        with open(os.path.join(directory, name), encoding="utf-8") as f:
            ex = parse_exercise(f.read(), name)
        if ex["id"] in found:
            raise ValueError(f"{name}: duplicate exercise id '{ex['id']}'")
        ex["number"] = len(found) + 1
        found[ex["id"]] = ex
    return found


def init_app(app):
    app.extensions["practice"] = load_exercises(app.config["PRACTICE_DIR"])


def all_exercises():
    return current_app.extensions["practice"]


def get_exercise(exercise_id):
    return all_exercises().get(exercise_id)


def topics():
    grouped = OrderedDict()
    for ex in all_exercises().values():
        grouped.setdefault(ex["topic"], []).append(ex)
    return grouped
