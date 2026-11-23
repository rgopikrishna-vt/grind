import json
import os

import pytest

from app import create_app
from app.db import get_db, now, to_iso
from app.lesson import parse_lesson, slugify
from app.topics import load_topics

from test_app import app, client, csrf, register, start  # noqa: F401  (shared fixtures)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPIC = "/topics/python-basics"

LESSON = """# My Lesson

Intro with a [link to lists](#2-lists) and [another file](Other%20File.md).

---

## Table of Contents

1. [Basics](#1-basics)

---

## 1. Basics

```python
# not a heading
print("hi")
```

## 2. Lists

### Slicing tricks

| Op | Cost |
|----|------|
| `a[i]` | O(1) |

See [basics](#1-basics) and [tricks](#slicing-tricks) and [docs](https://docs.python.org).
"""


def write_topic(root, tid, title, lesson=None, exercises=(), exams=()):
    path = root / tid
    (path / "practice").mkdir(parents=True)
    (path / "exams").mkdir()
    (path / "topic.json").write_text(json.dumps({"title": title}))
    if lesson:
        (path / "lesson.md").write_text(lesson)
    for i, (ex_id, lesson_no) in enumerate(exercises):
        src = open(os.path.join(ROOT, "topics", "python-basics", "practice", "13-two-sum.md")).read()
        src = src.replace("id: two-sum", f"id: {ex_id}").replace("lesson: 7", f"lesson: {lesson_no}")
        (path / "practice" / f"{i:02d}-{ex_id}.md").write_text(src)
    for exam_id in exams:
        (path / "exams" / f"{exam_id}.json").write_text(json.dumps({
            "id": exam_id, "title": exam_id, "duration_minutes": 5,
            "questions": [{"id": 1, "prompt": "?", "options": [{"key": "A", "text": "a"}], "answer": "A"}],
        }))
    return path


# ---------- loading ----------

def test_python_basics_topic(app):
    topics = app.extensions["topics"]
    t = topics["python-basics"]
    assert t["title"] == "Python Basics"
    assert len(t["lesson"]["sections"]) == 31  # the Table of Contents is dropped
    assert [e["id"] for e in t["exams"]] == ["python-basics"]
    assert len(t["exercises"]) == 54
    assert all(ex["lesson"] is not None for ex in t["exercises"]), "every exercise links to a lesson section"
    assert app.extensions["exams"]["python-basics"]["topic_id"] == "python-basics"
    assert app.extensions["practice"]["two-sum"]["topic_id"] == "python-basics"
    lists = t["lesson"]["by_number"][7]
    assert lists["id"] == "7-lists" and "two-sum" in [e["id"] for e in lists["exercises"]]


def test_lesson_parsing_and_links():
    lesson = parse_lesson(LESSON, "demo")
    assert lesson["title"] == "My Lesson"
    assert [s["id"] for s in lesson["sections"]] == ["1-basics", "2-lists"]
    intro = str(lesson["intro_html"])
    assert 'href="/topics/demo/lesson/2-lists"' in intro
    assert "another file" in intro and "Other%20File.md" not in intro  # unresolvable .md link becomes text
    basics, lists = lesson["sections"]
    assert "not a heading" in str(basics["html"]), "# lines inside code fences stay code"
    assert "try-code" in str(basics["html"]) and 'class="code hl"' in str(basics["html"])
    html = str(lists["html"])
    assert 'id="slicing-tricks"' in html and "<table" in html
    assert 'href="/topics/demo/lesson/1-basics"' in html
    assert 'href="/topics/demo/lesson/2-lists#slicing-tricks"' in html
    assert 'href="https://docs.python.org" target="_blank" rel="noopener"' in html


def test_lesson_html_is_escaped():
    html = str(parse_lesson("## 1. X\n\n<script>alert(1)</script>\n", "demo")["sections"][0]["html"])
    assert "<script>" not in html


def test_slugify_matches_github():
    assert slugify("11. Conditionals: `if` / `elif` / `else`") == "11-conditionals-if--elif--else"
    assert slugify("15. `enumerate`, `zip`, and `sorted`") == "15-enumerate-zip-and-sorted"


def test_load_topics_from_folders(tmp_path):
    write_topic(tmp_path, "b-topic", "Bravo", exercises=[("ex-b", 1)])
    write_topic(tmp_path, "a-topic", "Alpha", lesson=LESSON, exercises=[("ex-a", 2)], exams=["quiz-a"])
    (tmp_path / "not-a-topic").mkdir()  # folders without topic.json are ignored
    topics, exams, exercises = load_topics(str(tmp_path))
    assert list(topics) == ["a-topic", "b-topic"]
    assert topics["b-topic"]["lesson"] is None and topics["b-topic"]["exams"] == []
    assert list(exams) == ["quiz-a"] and set(exercises) == {"ex-a", "ex-b"}
    assert topics["a-topic"]["lesson"]["by_number"][2]["exercises"][0]["id"] == "ex-a"


def test_ids_must_be_unique_across_topics(tmp_path):
    write_topic(tmp_path, "one", "One", exercises=[("same", 1)])
    write_topic(tmp_path, "two", "Two", exercises=[("same", 1)])
    with pytest.raises(ValueError, match="already used"):
        load_topics(str(tmp_path))


def test_exercise_must_point_at_real_section(tmp_path):
    write_topic(tmp_path, "one", "One", lesson=LESSON, exercises=[("ex", 99)])
    with pytest.raises(ValueError, match="lesson section 99"):
        load_topics(str(tmp_path))


# ---------- pages ----------

def test_topic_pages_require_login(client):
    for path in ("/", TOPIC, f"{TOPIC}/lesson", f"{TOPIC}/lesson/7-lists", f"{TOPIC}/practice", f"{TOPIC}/quiz"):
        assert client.get(path).status_code == 302, path


def test_home_and_overview(client):
    register(client)
    home = client.get("/").get_data(as_text=True)
    assert "Python Basics" in home and "0/31 sections read" in home and "0/54 exercises solved" in home
    page = client.get(TOPIC).get_data(as_text=True)
    for text in ("Lesson", "Practice", "Quiz", "Start: What Is Python, and How Do You Run It", "130 questions"):
        assert text in page
    assert client.get("/topics/nope").status_code == 404
    assert client.get(f"{TOPIC}/quiz").headers["Location"].endswith("/exams/python-basics")
    exam = client.get("/exams/python-basics").get_data(as_text=True)
    assert 'class="active" aria-current="page">Quiz' in exam


def test_lesson_reading_progress(client):
    register(client)
    index = client.get(f"{TOPIC}/lesson").get_data(as_text=True)
    assert "0 of 31 sections read" in index and "Table of Contents" not in index
    page = client.get(f"{TOPIC}/lesson/7-lists").get_data(as_text=True)
    assert "Section 7 of 31" in page and "Practice this" in page and "Two Sum" in page
    assert f'href="{TOPIC}/lesson/17-comprehensions-and-generator-expressions"' in page
    assert client.get(f"{TOPIC}/lesson/nope").status_code == 404

    token = csrf(client, f"{TOPIC}/lesson")
    r = client.post(f"{TOPIC}/lesson/7-lists/read", data={"csrf_token": token, "next": "1"})
    assert r.headers["Location"].endswith(f"{TOPIC}/lesson/8-tuples")
    client.post(f"{TOPIC}/lesson/7-lists/read", data={"csrf_token": token})  # twice is fine
    assert "1 of 31 sections read" in client.get(f"{TOPIC}/lesson").get_data(as_text=True)
    assert "1/31 sections read" in client.get("/").get_data(as_text=True)
    assert "Mark as unread" in client.get(f"{TOPIC}/lesson/7-lists").get_data(as_text=True)

    client.post(f"{TOPIC}/lesson/7-lists/read", data={"csrf_token": token, "read": "0"})
    assert "0 of 31 sections read" in client.get(f"{TOPIC}/lesson").get_data(as_text=True)
    assert client.post(f"{TOPIC}/lesson/7-lists/read", data={}).status_code == 400  # CSRF

    last = f"{TOPIC}/lesson/31-where-to-go-from-here"
    assert client.post(f"{last}/read", data={"csrf_token": token, "next": "1"}).headers["Location"].endswith(f"{TOPIC}/lesson")


def test_lesson_progress_is_per_user(client, app):
    register(client, "alice")
    token = csrf(client, f"{TOPIC}/lesson")
    client.post(f"{TOPIC}/lesson/1-what-is-python-and-how-do-you-run-it/read", data={"csrf_token": token})
    other = app.test_client()
    register(other, "bob")
    assert "0 of 31 sections read" in other.get(f"{TOPIC}/lesson").get_data(as_text=True)


def test_try_lesson_code_in_scratchpad(client):
    register(client)
    token = csrf(client, f"{TOPIC}/lesson/7-lists")
    r = client.post("/scratchpad/new", data={"csrf_token": token, "code": "nums = [1, 2]\nprint(nums)\n", "source": "Python Basics: Lists"})
    page = client.get(r.headers["Location"]).get_data(as_text=True)
    assert "Python Basics: Lists" in page and "print(nums)" in page and "Counter" not in page


def test_exercise_page_links_to_topic_and_lesson(client):
    register(client)
    page = client.get("/practice/two-sum").get_data(as_text=True)
    assert f'href="{TOPIC}/practice"' in page and f'href="{TOPIC}/lesson/7-lists"' in page


def test_existing_attempts_show_under_topic(client, app):
    """Attempts saved before topics existed (exam_id 'python-basics') still count."""
    register(client)
    with app.app_context():
        db = get_db()
        uid = db.execute("SELECT id FROM users").fetchone()["id"]
        stamp = to_iso(now())
        db.execute(
            "INSERT INTO attempts (user_id, exam_id, started_at, deadline, submitted_at, status, score, total) "
            "VALUES (?, 'python-basics', ?, ?, ?, 'submitted', 104, 130)",
            (uid, stamp, stamp, stamp),
        )
        db.commit()
    assert "Best 80%" in client.get("/").get_data(as_text=True)
    assert "Best <strong>80%</strong>" in client.get(TOPIC).get_data(as_text=True)
    attempt_id, _ = start(client)
    assert client.get(f"/attempts/{attempt_id}").status_code == 200


def test_topics_dir_config(tmp_path):
    write_topic(tmp_path, "solo", "Solo", lesson=LESSON)
    app = create_app({"TESTING": True, "SECRET_KEY": "t", "DATABASE": str(tmp_path / "t.db"), "TOPICS_DIR": str(tmp_path)})
    c = app.test_client()
    register(c)
    page = c.get("/topics/solo").get_data(as_text=True)
    assert "Lesson" in page and ">Practice<" not in page and ">Quiz<" not in page
    assert c.get("/topics/solo/practice").status_code == 404
    assert c.get("/topics/solo/quiz").status_code == 404
    assert c.get("/practice").headers["Location"].endswith("/")


def test_new_topic_tool(tmp_path):
    import subprocess
    import sys

    lesson = tmp_path / "lesson.md"
    lesson.write_text(LESSON)
    quiz = tmp_path / "quiz.md"
    quiz.write_text("## Section 1\n**Q1.** Pick A\nA) yes\nB) no\n\n## Answer Key\n### Section 1\n1. **A** — because\n")
    out = tmp_path / "topics"
    out.mkdir()
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "new_topic.py"), "demo", "--title", "Demo", "--lesson", str(lesson),
         "--quiz", str(quiz), "--minutes", "5", "--topics-dir", str(out)],
        check=True, capture_output=True,
    )
    topics, exams, _ = load_topics(str(out))
    assert topics["demo"]["title"] == "Demo" and len(topics["demo"]["lesson"]["sections"]) == 2
    assert exams["demo"]["duration_minutes"] == 5 and len(exams["demo"]["questions"]) == 1
