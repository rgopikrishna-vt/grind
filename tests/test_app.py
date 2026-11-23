import os
import re
from datetime import timedelta

import pytest

from app import create_app
from app.db import from_iso, get_db, to_iso


# Tests always run on SQLite. Set TEST_DATABASE_URL=postgresql://... to also run them on Postgres
# (the tables in that database are dropped before each test).
BACKENDS = ["sqlite"] + (["postgres"] if os.environ.get("TEST_DATABASE_URL") else [])


@pytest.fixture(params=BACKENDS)
def app(request, tmp_path):
    config = {"TESTING": True, "SECRET_KEY": "test", "DATABASE": str(tmp_path / "t.sqlite3")}
    if request.param == "postgres":
        import psycopg

        url = os.environ["TEST_DATABASE_URL"]
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute("DROP TABLE IF EXISTS answers, attempts, practice_progress, lesson_progress, notebooks, users")
        config["DATABASE_URL"] = url
    return create_app(config)


@pytest.fixture
def client(app):
    return app.test_client()


def csrf(client, path="/login"):
    html = client.get(path).get_data(as_text=True)
    return re.search(r'name="csrf-token" content="([^"]+)"', html).group(1)


def register(client, username="alice", password="password123"):
    token = csrf(client, "/register")
    return client.post("/register", data={"username": username, "password": password, "confirm": password, "csrf_token": token})


def start(client, exam="python-basics"):
    token = csrf(client, "/")
    r = client.post(f"/exams/{exam}/start", data={"csrf_token": token})
    return int(r.headers["Location"].rstrip("/").split("/")[-1]), token


def test_exam_loaded(app):
    exam = app.extensions["exams"]["python-basics"]
    assert len(exam["questions"]) == 130
    assert all(q["answer"] and q["explanation"] for q in exam["questions"])


def test_requires_login(client):
    assert client.get("/").status_code == 302


def test_register_login_logout(client):
    assert register(client).status_code == 302
    assert "Python Basics" in client.get("/").get_data(as_text=True)
    client.post("/logout", data={"csrf_token": csrf(client, "/")})
    assert client.get("/").status_code == 302
    token = csrf(client)
    r = client.post("/login", data={"username": "ALICE", "password": "password123", "csrf_token": token})
    assert r.status_code == 302 and client.get("/").status_code == 200


def test_duplicate_username(client):
    register(client)
    client.post("/logout", data={"csrf_token": csrf(client, "/")})
    assert "taken" in register(client).get_data(as_text=True)


def test_csrf_enforced(client):
    assert client.post("/register", data={"username": "bob", "password": "x" * 8, "confirm": "x" * 8}).status_code == 400


def test_take_page_hides_answers(client):
    register(client)
    aid, _ = start(client)
    html = client.get(f"/attempts/{aid}").get_data(as_text=True)
    assert "Explanation" not in html and "is-answer" not in html


def test_full_attempt_scoring_and_review(client, app):
    register(client)
    aid, token = start(client)
    exam = app.extensions["exams"]["python-basics"]
    qs = exam["questions"]
    hdr = {"X-CSRF-Token": token}
    for q in qs[:10]:  # 10 right
        assert client.post(f"/attempts/{aid}/answer", json={"question_id": q["id"], "choice": q["answer"]}, headers=hdr).json["ok"]
    for q in qs[10:15]:  # 5 wrong
        wrong = next(o["key"] for o in q["options"] if o["key"] != q["answer"])
        client.post(f"/attempts/{aid}/answer", json={"question_id": q["id"], "choice": wrong}, headers=hdr)
    assert client.post(f"/attempts/{aid}/answer", json={"question_id": 1, "choice": "Z"}, headers=hdr).status_code == 400
    client.post(f"/attempts/{aid}/submit", data={"csrf_token": token})
    html = client.get(f"/attempts/{aid}/result").get_data(as_text=True)
    assert "10 of 130 correct" in html and "5 wrong" in html and "115 unanswered" in html
    assert "Explanation" in html
    # Answers are locked after submit
    assert client.post(f"/attempts/{aid}/answer", json={"question_id": 20, "choice": "A"}, headers=hdr).status_code == 409
    # Retake creates a new attempt, and results lists both once finished
    aid2, token = start(client)
    assert aid2 != aid
    client.post(f"/attempts/{aid2}/submit", data={"csrf_token": token})
    assert client.get("/results").get_data(as_text=True).count("Review</a>") == 2


def test_start_resumes_active_attempt(client):
    register(client)
    a1, _ = start(client)
    a2, _ = start(client)
    assert a1 == a2


def test_expired_attempt_auto_closes(client, app):
    register(client)
    aid, token = start(client)
    with app.app_context():
        db = get_db()
        row = db.execute("SELECT started_at, deadline FROM attempts WHERE id = ?", (aid,)).fetchone()
        past = from_iso(row["deadline"]) - timedelta(hours=2)
        db.execute("UPDATE attempts SET deadline = ? WHERE id = ?", (to_iso(past), aid))
        db.commit()
    r = client.post(f"/attempts/{aid}/answer", json={"question_id": 1, "choice": "B"}, headers={"X-CSRF-Token": token})
    assert r.status_code == 409
    assert client.get(f"/attempts/{aid}").status_code == 302
    assert "time ran out" in client.get(f"/attempts/{aid}/result").get_data(as_text=True)


def test_users_cannot_see_each_others_attempts(client):
    register(client, "alice")
    aid, _ = start(client)
    client.post("/logout", data={"csrf_token": csrf(client, "/")})
    register(client, "bob")
    assert client.get(f"/attempts/{aid}").status_code == 404
    assert client.get(f"/attempts/{aid}/result").status_code == 404
