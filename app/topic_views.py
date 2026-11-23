"""Topic pages: overview, lesson, practice list and quiz for each topic in topics/."""
from flask import Blueprint, abort, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db, now, to_iso
from .practice import group
from .topics import all_topics, get_topic

bp = Blueprint("topics", __name__)


# ---------- progress helpers (shared with the home page) ----------

def read_sections(topic_id, user_id):
    rows = get_db().execute(
        "SELECT section_id FROM lesson_progress WHERE user_id = ? AND topic_id = ?", (user_id, topic_id)
    ).fetchall()
    return {r["section_id"] for r in rows}


def practice_states(user_id):
    rows = get_db().execute(
        "SELECT exercise_id, code, attempts, solved_at FROM practice_progress WHERE user_id = ?", (user_id,)
    ).fetchall()
    out = {}
    for r in rows:
        out[r["exercise_id"]] = "solved" if r["solved_at"] else ("started" if (r["code"] or r["attempts"]) else "new")
    return out


def exam_stats(exam, user_id):
    db = get_db()
    stats = db.execute(
        "SELECT COUNT(*) AS n, MAX(score * 1.0 / total) AS best FROM attempts "
        "WHERE user_id = ? AND exam_id = ? AND status != 'in_progress' AND total > 0",
        (user_id, exam["id"]),
    ).fetchone()
    active = db.execute(
        "SELECT id FROM attempts WHERE user_id = ? AND exam_id = ? AND status = 'in_progress'", (user_id, exam["id"])
    ).fetchone()
    return {
        "exam": exam,
        "attempts": stats["n"],
        "best": round(100 * float(stats["best"])) if stats["best"] is not None else None,
        "active_id": active["id"] if active else None,
    }


def topic_progress(topic, user_id, states=None):
    """Lesson, practice and quiz progress for one topic, for cards and the overview."""
    states = practice_states(user_id) if states is None else states
    out = {"topic": topic, "lesson": None, "practice": None, "exams": []}
    lesson = topic["lesson"]
    if lesson:
        done = read_sections(topic["id"], user_id)
        sections = lesson["sections"]
        read = sum(1 for s in sections if s["id"] in done)
        out["lesson"] = {
            "read": read,
            "total": len(sections),
            "next": next((s for s in sections if s["id"] not in done), None),
            "started": read > 0,
        }
    if topic["exercises"]:
        solved = sum(1 for ex in topic["exercises"] if states.get(ex["id"]) == "solved")
        out["practice"] = {
            "solved": solved,
            "total": len(topic["exercises"]),
            "next": next((ex for ex in topic["exercises"] if states.get(ex["id"]) != "solved"), None),
        }
    out["exams"] = [exam_stats(e, user_id) for e in topic["exams"]]
    return out


def _topic_or_404(topic_id):
    return get_topic(topic_id) or abort(404)


def _lesson_or_404(topic):
    if not topic["lesson"]:
        abort(404)
    return topic["lesson"]


# ---------- pages ----------

@bp.route("/topics/<topic_id>")
@login_required
def overview(topic_id):
    topic = _topic_or_404(topic_id)
    from .views import close_expired_for_user
    close_expired_for_user()
    return render_template("topics/overview.html", topic=topic, tab="overview", p=topic_progress(topic, g.user["id"]))


@bp.route("/topics/<topic_id>/lesson")
@login_required
def lesson(topic_id):
    topic = _topic_or_404(topic_id)
    lesson = _lesson_or_404(topic)
    done = read_sections(topic_id, g.user["id"]) & set(lesson["by_id"])
    nxt = next((s for s in lesson["sections"] if s["id"] not in done), None)
    return render_template("topics/lesson_index.html", topic=topic, tab="lesson", lesson=lesson, done=done, next_section=nxt)


@bp.route("/topics/<topic_id>/lesson/<section_id>")
@login_required
def section(topic_id, section_id):
    topic = _topic_or_404(topic_id)
    lesson = _lesson_or_404(topic)
    sec = lesson["by_id"].get(section_id) or abort(404)
    done = read_sections(topic_id, g.user["id"]) & set(lesson["by_id"])
    states = practice_states(g.user["id"]) if sec["exercises"] else {}
    secs = lesson["sections"]
    i = sec["index"]
    return render_template(
        "topics/lesson_section.html", topic=topic, tab="lesson", lesson=lesson, sec=sec, done=done, states=states,
        prev_sec=secs[i - 1] if i > 0 else None, next_sec=secs[i + 1] if i + 1 < len(secs) else None,
    )


@bp.route("/topics/<topic_id>/lesson/<section_id>/read", methods=("POST",))
@login_required
def mark_read(topic_id, section_id):
    topic = _topic_or_404(topic_id)
    lesson = _lesson_or_404(topic)
    sec = lesson["by_id"].get(section_id) or abort(404)
    db = get_db()
    if request.form.get("read") == "0":
        db.execute(
            "DELETE FROM lesson_progress WHERE user_id = ? AND topic_id = ? AND section_id = ?",
            (g.user["id"], topic_id, section_id),
        )
        db.commit()
        return redirect(url_for("topics.section", topic_id=topic_id, section_id=section_id))
    db.execute(
        "INSERT INTO lesson_progress (user_id, topic_id, section_id, read_at) VALUES (?, ?, ?, ?) "
        "ON CONFLICT(user_id, topic_id, section_id) DO NOTHING",
        (g.user["id"], topic_id, section_id, to_iso(now())),
    )
    db.commit()
    secs = lesson["sections"]
    nxt = secs[sec["index"] + 1] if sec["index"] + 1 < len(secs) else None
    if nxt and request.form.get("next") == "1":
        return redirect(url_for("topics.section", topic_id=topic_id, section_id=nxt["id"]))
    if not nxt and request.form.get("next") == "1":
        return redirect(url_for("topics.lesson", topic_id=topic_id))
    return redirect(url_for("topics.section", topic_id=topic_id, section_id=section_id))


@bp.route("/topics/<topic_id>/practice")
@login_required
def practice(topic_id):
    topic = _topic_or_404(topic_id)
    if not topic["exercises"]:
        abort(404)
    states = practice_states(g.user["id"])
    groups = []
    for name, exercises in group(topic["exercises"]).items():
        rows = [{"ex": ex, "state": states.get(ex["id"], "new")} for ex in exercises]
        groups.append({"topic": name, "rows": rows, "solved": sum(1 for r in rows if r["state"] == "solved")})
    solved = sum(gr["solved"] for gr in groups)
    nxt = next((r["ex"] for gr in groups for r in gr["rows"] if r["state"] != "solved"), None)
    return render_template(
        "practice/index.html", topic=topic, tab="practice", groups=groups,
        total=len(topic["exercises"]), solved=solved, next_ex=nxt,
    )


@bp.route("/topics/<topic_id>/quiz")
@login_required
def quiz(topic_id):
    topic = _topic_or_404(topic_id)
    if len(topic["exams"]) == 1:
        return redirect(url_for("views.exam_detail", exam_id=topic["exams"][0]["id"]))
    if not topic["exams"]:
        abort(404)
    from .views import close_expired_for_user
    close_expired_for_user()
    cards = [exam_stats(e, g.user["id"]) for e in topic["exams"]]
    return render_template("topics/quiz.html", topic=topic, tab="quiz", cards=cards)


def home_cards(user_id):
    states = practice_states(user_id)
    return [topic_progress(t, user_id, states) for t in all_topics().values()]
