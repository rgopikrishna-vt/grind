from datetime import timedelta

from flask import Blueprint, abort, current_app, flash, g, jsonify, redirect, render_template, request, url_for

from .auth import login_required
from .db import from_iso, get_db, now, to_iso
from .exams import get_exam
from .topics import get_topic

bp = Blueprint("views", __name__)


# ---------- helpers ----------

def _attempt_or_404(attempt_id):
    a = get_db().execute("SELECT * FROM attempts WHERE id = ? AND user_id = ?", (attempt_id, g.user["id"])).fetchone()
    if a is None:
        abort(404)
    return a


def _answers(attempt_id):
    rows = get_db().execute("SELECT question_id, choice FROM answers WHERE attempt_id = ?", (attempt_id,))
    return {r["question_id"]: r["choice"] for r in rows}


def _grade(exam, answers):
    return sum(1 for q in exam["questions"] if answers.get(q["id"]) == q["answer"])


def _finalize(attempt, status):
    """Score an in-progress attempt and close it. Returns the fresh row."""
    db = get_db()
    exam = get_exam(attempt["exam_id"])
    total = len(exam["questions"]) if exam else 0
    score = _grade(exam, _answers(attempt["id"])) if exam else 0
    db.execute(
        "UPDATE attempts SET status = ?, submitted_at = ?, score = ?, total = ? WHERE id = ? AND status = 'in_progress'",
        (status, to_iso(now()), score, total, attempt["id"]),
    )
    db.commit()
    return db.execute("SELECT * FROM attempts WHERE id = ?", (attempt["id"],)).fetchone()


def _expired(attempt, grace=0):
    return now() > from_iso(attempt["deadline"]) + timedelta(seconds=grace)


def _close_if_expired(attempt):
    """Attempts whose time ran out (e.g. the browser was closed) are graded on whatever was saved."""
    if attempt["status"] == "in_progress" and _expired(attempt, current_app.config["SUBMIT_GRACE_SECONDS"]):
        return _finalize(attempt, "timed_out")
    return attempt


def close_expired_for_user():
    rows = get_db().execute("SELECT * FROM attempts WHERE user_id = ? AND status = 'in_progress'", (g.user["id"],)).fetchall()
    for a in rows:
        _close_if_expired(a)


def _summaries(rows):
    out = []
    for a in rows:
        exam = get_exam(a["exam_id"])
        started, ended = from_iso(a["started_at"]), from_iso(a["submitted_at"])
        pct = round(100 * a["score"] / a["total"]) if a["total"] else 0
        out.append({
            "row": a,
            "exam_title": exam["title"] if exam else a["exam_id"],
            "percent": pct,
            "passed": exam is not None and pct >= exam["pass_percent"],
            "duration": _fmt_duration((ended - started).total_seconds()) if ended else None,
            "started": started,
        })
    return out


def _fmt_duration(seconds):
    seconds = int(max(0, seconds))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m:02d}m {s:02d}s" if h else f"{m}m {s:02d}s"


# ---------- pages ----------

@bp.route("/")
@login_required
def dashboard():
    from .topic_views import home_cards
    close_expired_for_user()
    recent = get_db().execute(
        "SELECT * FROM attempts WHERE user_id = ? AND status != 'in_progress' ORDER BY id DESC LIMIT 5",
        (g.user["id"],),
    ).fetchall()
    return render_template("dashboard.html", cards=home_cards(g.user["id"]), recent=_summaries(recent))


@bp.route("/exams/<exam_id>")
@login_required
def exam_detail(exam_id):
    exam = get_exam(exam_id) or abort(404)
    close_expired_for_user()
    rows = get_db().execute(
        "SELECT * FROM attempts WHERE user_id = ? AND exam_id = ? ORDER BY id DESC", (g.user["id"], exam_id)
    ).fetchall()
    active = next((r for r in rows if r["status"] == "in_progress"), None)
    done = [r for r in rows if r["status"] != "in_progress"]
    topic = get_topic(exam["topic_id"])
    return render_template("exam_detail.html", exam=exam, topic=topic, tab="quiz", active=active, history=_summaries(done))


@bp.route("/exams/<exam_id>/start", methods=("POST",))
@login_required
def start_exam(exam_id):
    exam = get_exam(exam_id) or abort(404)
    close_expired_for_user()
    db = get_db()
    active = db.execute(
        "SELECT id FROM attempts WHERE user_id = ? AND exam_id = ? AND status = 'in_progress'", (g.user["id"], exam_id)
    ).fetchone()
    if active:  # one live attempt per exam; resume it rather than resetting the clock
        return redirect(url_for("views.take", attempt_id=active["id"]))
    start = now()
    attempt_id = db.execute(
        "INSERT INTO attempts (user_id, exam_id, started_at, deadline, total) VALUES (?, ?, ?, ?, ?) RETURNING id",
        (g.user["id"], exam_id, to_iso(start), to_iso(start + timedelta(minutes=exam["duration_minutes"])), len(exam["questions"])),
    ).fetchone()["id"]
    db.commit()
    return redirect(url_for("views.take", attempt_id=attempt_id))


@bp.route("/attempts/<int:attempt_id>")
@login_required
def take(attempt_id):
    attempt = _close_if_expired(_attempt_or_404(attempt_id))
    if attempt["status"] != "in_progress":
        return redirect(url_for("views.result", attempt_id=attempt_id))
    exam = get_exam(attempt["exam_id"]) or abort(404)
    remaining = max(0, int((from_iso(attempt["deadline"]) - now()).total_seconds()))
    return render_template("take.html", exam=exam, attempt=attempt, answers=_answers(attempt_id), remaining=remaining)


@bp.route("/attempts/<int:attempt_id>/answer", methods=("POST",))
@login_required
def save_answer(attempt_id):
    attempt = _attempt_or_404(attempt_id)
    data = request.get_json(silent=True) or {}
    if attempt["status"] != "in_progress" or _expired(attempt, grace=2):
        return jsonify(ok=False, error="time_up"), 409
    exam = get_exam(attempt["exam_id"]) or abort(404)
    try:
        qid = int(data.get("question_id"))
    except (TypeError, ValueError):
        return jsonify(ok=False, error="bad_question"), 400
    q = exam["by_id"].get(qid)
    if q is None:
        return jsonify(ok=False, error="bad_question"), 400
    choice = data.get("choice")
    db = get_db()
    if choice in (None, ""):
        db.execute("DELETE FROM answers WHERE attempt_id = ? AND question_id = ?", (attempt_id, qid))
    elif choice in {o["key"] for o in q["options"]}:
        db.execute(
            "INSERT INTO answers (attempt_id, question_id, choice) VALUES (?, ?, ?) "
            "ON CONFLICT(attempt_id, question_id) DO UPDATE SET choice = excluded.choice",
            (attempt_id, qid, choice),
        )
    else:
        return jsonify(ok=False, error="bad_choice"), 400
    db.commit()
    return jsonify(ok=True)


@bp.route("/attempts/<int:attempt_id>/submit", methods=("POST",))
@login_required
def submit(attempt_id):
    attempt = _attempt_or_404(attempt_id)
    if attempt["status"] == "in_progress":
        timed_out = _expired(attempt) or request.form.get("reason") == "timeout"
        _finalize(attempt, "timed_out" if timed_out else "submitted")
    return redirect(url_for("views.result", attempt_id=attempt_id))


@bp.route("/attempts/<int:attempt_id>/result")
@login_required
def result(attempt_id):
    attempt = _close_if_expired(_attempt_or_404(attempt_id))
    if attempt["status"] == "in_progress":
        flash("This attempt is still running.", "error")
        return redirect(url_for("views.take", attempt_id=attempt_id))
    exam = get_exam(attempt["exam_id"])
    if exam is None:
        abort(404, "This exam is no longer available.")
    answers = _answers(attempt_id)
    sections = []
    for name, qids in exam["sections"].items():
        correct = sum(1 for qid in qids if answers.get(qid) == exam["by_id"][qid]["answer"])
        sections.append({"name": name, "correct": correct, "total": len(qids)})
    unanswered = sum(1 for q in exam["questions"] if q["id"] not in answers)
    summary = _summaries([attempt])[0]
    return render_template(
        "result.html", exam=exam, attempt=attempt, answers=answers, sections=sections,
        summary=summary, unanswered=unanswered, wrong=attempt["total"] - attempt["score"] - unanswered,
    )


@bp.route("/results")
@login_required
def results():
    close_expired_for_user()
    rows = get_db().execute(
        "SELECT * FROM attempts WHERE user_id = ? AND status != 'in_progress' ORDER BY id DESC", (g.user["id"],)
    ).fetchall()
    return render_template("results.html", history=_summaries(rows))
