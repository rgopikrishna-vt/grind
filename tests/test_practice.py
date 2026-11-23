import json
import os
import re

import pytest

import importlib.util

from app.practice import load_exercises, parse_exercise

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The same runner the browser loads into Pyodide, imported here with CPython.
_spec = importlib.util.spec_from_file_location("grind_runner", os.path.join(ROOT, "app", "static", "practice", "runner.py"))
runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runner)
EXERCISES = load_exercises(os.path.join(ROOT, "topics", "python-basics", "practice"))
N = len(EXERCISES)
PRACTICE = "/topics/python-basics/practice"

from test_app import app, client, csrf, register  # noqa: E402,F401  (shared fixtures)


def groups(ex):
    return [("example", ex["examples"]), ("hidden", ex["tests"])]


def test_starter_set_loaded():
    assert len(EXERCISES) >= 30
    for ex in EXERCISES.values():
        assert ex["hints"], f"{ex['id']} has no hints"
        assert ex["hidden_count"] >= 3, f"{ex['id']} needs at least 3 hidden tests"


@pytest.mark.parametrize("ex_id", list(EXERCISES))
def test_solution_passes_its_tests(ex_id):
    ex = EXERCISES[ex_id]
    res = runner.grade(ex["solution"], groups(ex))
    assert res["error"] is None, res["error"]
    failed = [r for r in res["results"] if not r["ok"]]
    assert not failed, failed
    assert res["total"] == ex["example_count"] + ex["hidden_count"]


@pytest.mark.parametrize("ex_id", list(EXERCISES))
def test_starter_does_not_pass(ex_id):
    ex = EXERCISES[ex_id]
    res = runner.grade(ex["starter"], groups(ex))
    assert res["error"] is not None or res["passed"] < res["total"]


def test_grade_reports_got_and_expected():
    res = runner.grade("def f(x):\n    return x + 1\n", [("hidden", "assert f(1) == 2\nassert f(2) == 5\n")])
    assert [r["ok"] for r in res["results"]] == [True, False]
    assert res["results"][1]["got"] == "3" and res["results"][1]["expected"] == "5"


def test_grade_reports_errors():
    res = runner.grade("def f(:\n", [("hidden", "assert f() == 1")])
    assert "SyntaxError" in res["error"]
    res = runner.grade("def f():\n    return 1 / 0\n", [("hidden", "assert f() == 1")])
    assert "ZeroDivisionError" in res["results"][0]["message"]
    assert "grind_runner" not in res["results"][0]["message"] and "runner.py" not in res["results"][0]["message"]


def test_run_cell_keeps_state_and_shows_last_value():
    out = []
    emit = lambda kind, text: out.append((kind, text))
    runner.reset("t")
    assert runner.run_cell("x = 20\nprint('hi')", "t", emit=emit) == {"result": None, "error": None}
    assert out == [("stdout", "hi"), ("stdout", "\n")]
    assert runner.run_cell("x * 2 + 2", "t")["result"] == "42"
    assert runner.run_cell("x", "other")["error"].endswith("NameError: name 'x' is not defined")


def test_run_cell_reads_stdin():
    out = []
    r = runner.run_cell("name = input('Name? ')\nprint('Hi', name)", "s", stdin="Ana\n", emit=lambda k, t: out.append(t))
    assert r["error"] is None
    assert "".join(out) == "Name? Hi Ana\n"
    r = runner.run_cell("input()", "s")
    assert "EOFError" in r["error"] and "stdin box" in r["error"]


def test_parse_rejects_bad_files():
    with pytest.raises(ValueError, match="missing 'difficulty'"):
        parse_exercise("---\nid: x\ntitle: X\ntopic: T\n---\n## Prompt\nhi\n")
    with pytest.raises(ValueError, match="Solution"):
        parse_exercise("---\nid: x\ntitle: X\ntopic: T\ndifficulty: easy\n---\n## Prompt\nhi\n## Starter\n```python\npass\n```\n## Tests\n```python\nassert 1\n```\n")


# ---------- web ----------

def _json_post(client, url, token, body):
    return client.post(url, data=json.dumps(body), headers={"X-CSRF-Token": token, "Content-Type": "application/json"})


def test_practice_pages_require_login(client):
    assert client.get("/practice").status_code == 302
    assert client.get("/scratchpad").status_code == 302


def test_practice_progress_flow(client):
    register(client)
    assert client.get("/practice").headers["Location"].endswith("/topics/python-basics/practice")
    html = client.get(PRACTICE).get_data(as_text=True)
    assert f"0 of {N} solved" in html and "Two Sum" in html
    page = client.get("/practice/two-sum").get_data(as_text=True)
    assert "def two_sum(nums, target):" in page
    assert "seen = {}" not in page, "the solution must not be sent before it is asked for"
    token = csrf(client, PRACTICE)

    assert _json_post(client, "/practice/two-sum/save", token, {"code": "my draft", "hints_used": 2}).get_json()["ok"]
    assert "my draft" in client.get("/practice/two-sum").get_data(as_text=True)

    r = _json_post(client, "/practice/two-sum/submit", token, {"code": "attempt 1", "passed": False}).get_json()
    assert r == {"ok": True, "solved": False, "first_solve": False, "attempts": 1}
    r = _json_post(client, "/practice/two-sum/submit", token, {"code": "attempt 2", "passed": True}).get_json()
    assert r["solved"] and r["first_solve"] and r["attempts"] == 2
    r = _json_post(client, "/practice/two-sum/submit", token, {"code": "attempt 3", "passed": False}).get_json()
    assert r["solved"] and not r["first_solve"], "solved stays solved"
    assert f"1 of {N} solved" in client.get(PRACTICE).get_data(as_text=True)
    assert f"1/{N} exercises solved" in client.get("/").get_data(as_text=True)

    sol = _json_post(client, "/practice/two-sum/solution", token, {}).get_json()
    assert "seen = {}" in sol["solution"] and "<p>" in sol["explanation_html"]


def test_practice_rejects_bad_input(client):
    register(client)
    token = csrf(client, PRACTICE)
    assert client.get("/practice/nope").status_code == 404
    assert _json_post(client, "/practice/two-sum/save", token, {"code": 5}).status_code == 400
    assert _json_post(client, "/practice/two-sum/save", token, {"code": "x" * 200_000}).status_code == 400
    assert client.post("/practice/two-sum/save", json={"code": "x"}).status_code == 400  # no CSRF token


def test_progress_is_per_user(client, app):
    register(client, "alice")
    token = csrf(client, PRACTICE)
    _json_post(client, "/practice/fizzbuzz/submit", token, {"code": "alice code", "passed": True})
    other = app.test_client()
    register(other, "bob")
    assert f"0 of {N} solved" in other.get(PRACTICE).get_data(as_text=True)
    assert "alice code" not in other.get("/practice/fizzbuzz").get_data(as_text=True)


def test_scratchpad_notebooks(client, app):
    register(client)
    token = csrf(client, "/scratchpad")
    r = client.post("/scratchpad/new", data={"csrf_token": token})
    nb_url = r.headers["Location"]
    nb_id = int(nb_url.rstrip("/").split("/")[-1])
    page = client.get(nb_url).get_data(as_text=True)
    assert "Scratchpad" in page and "Counter" in page  # welcome cells on the first notebook

    cells = [{"type": "markdown", "source": "# Notes"}, {"type": "code", "source": "print(input())", "stdin": "hi"}]
    ok = _json_post(client, f"/scratchpad/{nb_id}/save", token, {"title": "  Graphs  ", "cells": cells})
    assert ok.get_json()["ok"]
    listing = client.get("/scratchpad").get_data(as_text=True)
    assert "Graphs" in listing
    page = client.get(nb_url).get_data(as_text=True)
    assert re.search(r'"stdin":\s*"hi"', page)

    assert _json_post(client, f"/scratchpad/{nb_id}/save", token, {"title": "x", "cells": [{"type": "bogus"}]}).status_code == 400
    assert _json_post(client, f"/scratchpad/{nb_id}/save", token, {"title": "", "cells": []}).status_code == 400

    other = app.test_client()
    register(other, "mallory")
    assert other.get(nb_url).status_code == 404
    t2 = csrf(other, "/scratchpad")
    assert _json_post(other, f"/scratchpad/{nb_id}/save", t2, {"title": "pwn", "cells": []}).status_code == 404

    second = client.post("/scratchpad/new", data={"csrf_token": token}).headers["Location"]
    assert "Counter" not in client.get(second).get_data(as_text=True)  # later notebooks start empty

    r = client.post(f"/scratchpad/{nb_id}/delete", data={"csrf_token": token})
    assert r.status_code == 302
    assert client.get(nb_url).status_code == 404
