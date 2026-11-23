"""Exams are plain JSON files in a topic's exams/ folder (topics/<topic>/exams/). Drop a new file in
to add an exam. Exam ids must be unique across all topics, because attempts are stored by id.

File format:
{
  "id": "python-basics",              # URL-safe, unique
  "title": "Python Basics",
  "description": "...",
  "duration_minutes": 60,
  "pass_percent": 70,                 # optional, default 70
  "questions": [
    {"id": 1, "section": "...", "prompt": "markdown",
     "options": [{"key": "A", "text": "markdown"}, ...],
     "answer": "B", "explanation": "markdown"}
  ]
}
"""
import json
import os
from collections import OrderedDict

from flask import current_app

DEFAULT_PASS_PERCENT = 70


def load_exams(directory):
    found = OrderedDict()
    if not os.path.isdir(directory):
        return found
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(directory, name), encoding="utf-8") as f:
            exam = json.load(f)
        _validate(exam, name)
        exam.setdefault("description", "")
        exam.setdefault("pass_percent", DEFAULT_PASS_PERCENT)
        exam["by_id"] = {q["id"]: q for q in exam["questions"]}
        sections = OrderedDict()
        for q in exam["questions"]:
            sections.setdefault(q.get("section") or "General", []).append(q["id"])
        exam["sections"] = sections
        found[exam["id"]] = exam
    return found


def _validate(exam, name):
    for field in ("id", "title", "duration_minutes", "questions"):
        if field not in exam:
            raise ValueError(f"{name}: missing '{field}'")
    ids = set()
    for q in exam["questions"]:
        if q["id"] in ids:
            raise ValueError(f"{name}: duplicate question id {q['id']}")
        ids.add(q["id"])
        if q["answer"] not in {o["key"] for o in q["options"]}:
            raise ValueError(f"{name}: question {q['id']} answer is not an option")


def all_exams():
    return current_app.extensions["exams"]


def get_exam(exam_id):
    return all_exams().get(exam_id)
