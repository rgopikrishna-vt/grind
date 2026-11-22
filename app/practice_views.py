"""Practice section: coding exercises and free scratchpad notebooks.

All Python runs in the browser (Pyodide in a Web Worker). The server only stores each user's
code, hint/solution usage, solved status and notebooks.
"""
import json

from flask import Blueprint, abort, current_app, flash, g, jsonify, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db, now, to_iso
from .practice import all_exercises, get_exercise, topics

bp = Blueprint("practice", __name__)

MAX_CODE = 100_000
MAX_NOTEBOOK = 1_000_000
MAX_CELLS = 300
MAX_TITLE = 120


def _progress_map():
    rows = get_db().execute("SELECT * FROM practice_progress WHERE user_id = ?", (g.user["id"],)).fetchall()
    return {r["exercise_id"]: r for r in rows}


def _progress(exercise_id):
    return get_db().execute(
        "SELECT * FROM practice_progress WHERE user_id = ? AND exercise_id = ?", (g.user["id"], exercise_id)
    ).fetchone()


def _ensure_progress(exercise_id):
    db = get_db()
    db.execute(
        "INSERT INTO practice_progress (user_id, exercise_id, updated_at) VALUES (?, ?, ?) "
        "ON CONFLICT(user_id, exercise_id) DO NOTHING",
        (g.user["id"], exercise_id, to_iso(now())),
    )


def _json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400)
    return data


def _code_from(data):
    code = data.get("code")
    if not isinstance(code, str) or len(code) > MAX_CODE:
        abort(400)
    return code


def practice_summary(user_id):
    """Solved count for the dashboard card."""
    row = get_db().execute(
        "SELECT COUNT(*) AS n FROM practice_progress WHERE user_id = ? AND solved_at IS NOT NULL", (user_id,)
    ).fetchone()
    ids = set(all_exercises())
    return {"solved": min(row["n"], len(ids)), "total": len(ids)}


# ---------- exercises ----------

@bp.route("/practice")
@login_required
def index():
    progress = _progress_map()
    groups = []
    for topic, exercises in topics().items():
        items = []
        for ex in exercises:
            p = progress.get(ex["id"])
            state = "solved" if p and p["solved_at"] else ("started" if p and (p["code"] or p["attempts"]) else "new")
            items.append({"ex": ex, "state": state, "attempts": p["attempts"] if p else 0})
        groups.append({"topic": topic, "rows": items, "solved": sum(1 for i in items if i["state"] == "solved")})
    total = len(all_exercises())
    solved = sum(gr["solved"] for gr in groups)
    nxt = next((i["ex"] for gr in groups for i in gr["rows"] if i["state"] != "solved"), None)
    return render_template("practice/index.html", groups=groups, total=total, solved=solved, next_ex=nxt)


@bp.route("/practice/<exercise_id>")
@login_required
def exercise(exercise_id):
    ex = get_exercise(exercise_id) or abort(404)
    p = _progress(exercise_id)
    ids = list(all_exercises())
    i = ids.index(exercise_id)
    return render_template(
        "practice/exercise.html",
        ex=ex,
        progress=p,
        code=(p["code"] if p and p["code"] is not None else ex["starter"]),
        prev_id=ids[i - 1] if i > 0 else None,
        next_id=ids[i + 1] if i + 1 < len(ids) else None,
    )


@bp.route("/practice/<exercise_id>/save", methods=("POST",))
@login_required
def save(exercise_id):
    get_exercise(exercise_id) or abort(404)
    data = _json()
    code = _code_from(data)
    db = get_db()
    _ensure_progress(exercise_id)
    db.execute(
        "UPDATE practice_progress SET code = ?, updated_at = ? WHERE user_id = ? AND exercise_id = ?",
        (code, to_iso(now()), g.user["id"], exercise_id),
    )
    hints = data.get("hints_used")
    if isinstance(hints, int) and hints > 0:
        db.execute(
            "UPDATE practice_progress SET hints_used = ? WHERE user_id = ? AND exercise_id = ? AND hints_used < ?",
            (hints, g.user["id"], exercise_id, hints),
        )
    db.commit()
    return jsonify(ok=True)


@bp.route("/practice/<exercise_id>/submit", methods=("POST",))
@login_required
def submit(exercise_id):
    """Record a graded submission. Grading happens in the browser, so this trusts the client;
    it is a self-study tool, not a proctored exam."""
    get_exercise(exercise_id) or abort(404)
    data = _json()
    code = _code_from(data)
    passed = data.get("passed") is True
    stamp = to_iso(now())
    db = get_db()
    _ensure_progress(exercise_id)
    db.execute(
        "UPDATE practice_progress SET code = ?, attempts = attempts + 1, updated_at = ? WHERE user_id = ? AND exercise_id = ?",
        (code, stamp, g.user["id"], exercise_id),
    )
    first_solve = False
    if passed:
        cur = db.execute(
            "UPDATE practice_progress SET solved_at = ? WHERE user_id = ? AND exercise_id = ? AND solved_at IS NULL",
            (stamp, g.user["id"], exercise_id),
        )
        first_solve = cur.rowcount == 1
    db.commit()
    p = _progress(exercise_id)
    return jsonify(ok=True, solved=bool(p["solved_at"]), first_solve=first_solve, attempts=p["attempts"])


@bp.route("/practice/<exercise_id>/solution", methods=("POST",))
@login_required
def solution(exercise_id):
    ex = get_exercise(exercise_id) or abort(404)
    db = get_db()
    _ensure_progress(exercise_id)
    db.execute(
        "UPDATE practice_progress SET solution_viewed = 1 WHERE user_id = ? AND exercise_id = ?",
        (g.user["id"], exercise_id),
    )
    db.commit()
    md = current_app.jinja_env.filters["md"]
    return jsonify(ok=True, solution=ex["solution"], explanation_html=str(md(ex["explanation"])) if ex["explanation"] else "")


# ---------- scratchpad notebooks ----------

WELCOME_CELLS = [
    {"type": "markdown", "source": "# Scratchpad\nA free notebook for trying things out. Cells share variables, like Jupyter. "
     "**Shift+Enter** runs a cell and moves to the next one; **Ctrl/Cmd+Enter** runs it in place. "
     "Double-click a text cell to edit it."},
    {"type": "code", "source": "nums = [5, 3, 8, 1]\nsorted(nums)"},
    {"type": "code", "source": "from collections import Counter\nCounter(\"mississippi\").most_common(2)"},
]


def _notebook_or_404(nb_id):
    nb = get_db().execute("SELECT * FROM notebooks WHERE id = ? AND user_id = ?", (nb_id, g.user["id"])).fetchone()
    if nb is None:
        abort(404)
    return nb


def _clean_cells(cells):
    if not isinstance(cells, list) or len(cells) > MAX_CELLS:
        abort(400)
    out = []
    for c in cells:
        if not isinstance(c, dict) or c.get("type") not in ("code", "markdown") or not isinstance(c.get("source", ""), str):
            abort(400)
        cell = {"type": c["type"], "source": c.get("source", "")}
        if c["type"] == "code" and isinstance(c.get("stdin"), str) and c["stdin"]:
            cell["stdin"] = c["stdin"]
        out.append(cell)
    return out


@bp.route("/scratchpad")
@login_required
def notebooks():
    rows = get_db().execute(
        "SELECT id, title, created_at, updated_at FROM notebooks WHERE user_id = ? ORDER BY updated_at DESC, id DESC",
        (g.user["id"],),
    ).fetchall()
    return render_template("practice/notebooks.html", notebooks=rows)


@bp.route("/scratchpad/new", methods=("POST",))
@login_required
def new_notebook():
    db = get_db()
    count = db.execute("SELECT COUNT(*) AS n FROM notebooks WHERE user_id = ?", (g.user["id"],)).fetchone()["n"]
    stamp = to_iso(now())
    cells = WELCOME_CELLS if count == 0 else [{"type": "code", "source": ""}]
    nb_id = db.execute(
        "INSERT INTO notebooks (user_id, title, cells, created_at, updated_at) VALUES (?, ?, ?, ?, ?) RETURNING id",
        (g.user["id"], f"Notebook {count + 1}", json.dumps(cells), stamp, stamp),
    ).fetchone()["id"]
    db.commit()
    return redirect(url_for("practice.notebook", nb_id=nb_id))


@bp.route("/scratchpad/<int:nb_id>")
@login_required
def notebook(nb_id):
    nb = _notebook_or_404(nb_id)
    return render_template("practice/notebook.html", nb=nb, cells=json.loads(nb["cells"]))


@bp.route("/scratchpad/<int:nb_id>/save", methods=("POST",))
@login_required
def save_notebook(nb_id):
    _notebook_or_404(nb_id)
    if request.content_length and request.content_length > MAX_NOTEBOOK:
        abort(413)
    data = _json()
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        abort(400)
    cells = json.dumps(_clean_cells(data.get("cells")))
    if len(cells) > MAX_NOTEBOOK:
        abort(413)
    db = get_db()
    db.execute(
        "UPDATE notebooks SET title = ?, cells = ?, updated_at = ? WHERE id = ? AND user_id = ?",
        (title.strip()[:MAX_TITLE], cells, to_iso(now()), nb_id, g.user["id"]),
    )
    db.commit()
    return jsonify(ok=True)


@bp.route("/scratchpad/<int:nb_id>/delete", methods=("POST",))
@login_required
def delete_notebook(nb_id):
    nb = _notebook_or_404(nb_id)
    db = get_db()
    db.execute("DELETE FROM notebooks WHERE id = ? AND user_id = ?", (nb_id, g.user["id"]))
    db.commit()
    flash(f"Deleted “{nb['title']}”.", "ok")
    return redirect(url_for("practice.notebooks"))
