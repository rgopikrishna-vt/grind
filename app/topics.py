"""Topics are folders in topics/. Each one bundles a lesson, practice exercises and quizzes:

    topics/
      python-basics/            # the folder name is the topic id (lowercase, digits, dashes)
        topic.json              # {"title": "...", "description": "...", "order": 1}
        lesson.md               # optional: the lesson, split into pages at each "## " heading
        practice/*.md           # optional: practice exercises (see app/practice.py)
        exams/*.json            # optional: timed quizzes/exams (see app/exams.py)

Add a folder (or run tools/new_topic.py) and restart: the topic shows up on the home page with
whichever of Lesson, Practice and Quiz it has. Topics are listed by "order", then title.
"""
import json
import os
from collections import OrderedDict

from flask import current_app

from .exams import load_exams
from .lesson import parse_lesson
from .practice import ID_RE, load_exercises

TOPIC_FILE = "topic.json"


def load_topics(directory):
    """Return (topics, exams, exercises): topics by id, plus every exam and exercise by id."""
    topics, exams, exercises = [], OrderedDict(), OrderedDict()
    if not os.path.isdir(directory):
        return OrderedDict(), exams, exercises
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if not os.path.isfile(os.path.join(path, TOPIC_FILE)):
            continue
        if not ID_RE.match(name):
            raise ValueError(f"topics/{name}: folder name must be lowercase letters, digits and dashes")
        with open(os.path.join(path, TOPIC_FILE), encoding="utf-8") as f:
            meta = json.load(f)
        if not meta.get("title"):
            raise ValueError(f"topics/{name}/{TOPIC_FILE}: missing 'title'")
        topic = {
            "id": name,
            "title": meta["title"],
            "description": meta.get("description", ""),
            "order": meta.get("order", 1000),
            "lesson": None,
        }
        lesson_path = os.path.join(path, "lesson.md")
        if os.path.isfile(lesson_path):
            with open(lesson_path, encoding="utf-8") as f:
                topic["lesson"] = parse_lesson(f.read(), name)

        topic_exercises = load_exercises(os.path.join(path, "practice"))
        for ex in topic_exercises.values():
            if ex["id"] in exercises:
                raise ValueError(f"topics/{name}: exercise id '{ex['id']}' is already used by another topic")
            ex["topic_id"] = name
            exercises[ex["id"]] = ex
            if topic["lesson"] and ex["lesson"] is not None:
                section = topic["lesson"]["by_number"].get(ex["lesson"])
                if section is None:
                    raise ValueError(f"topics/{name}: exercise '{ex['id']}' points at lesson section {ex['lesson']}, which doesn't exist")
                section["exercises"].append(ex)
        topic["exercises"] = list(topic_exercises.values())

        topic_exams = load_exams(os.path.join(path, "exams"))
        for exam in topic_exams.values():
            if exam["id"] in exams:
                raise ValueError(f"topics/{name}: exam id '{exam['id']}' is already used by another topic")
            exam["topic_id"] = name
            exams[exam["id"]] = exam
        topic["exams"] = list(topic_exams.values())
        topics.append(topic)

    topics.sort(key=lambda t: (t["order"], t["title"].lower()))
    return OrderedDict((t["id"], t) for t in topics), exams, exercises


def init_app(app):
    topics, exams, exercises = load_topics(app.config["TOPICS_DIR"])
    app.extensions["topics"] = topics
    app.extensions["exams"] = exams
    app.extensions["practice"] = exercises


def all_topics():
    return current_app.extensions["topics"]


def get_topic(topic_id):
    return all_topics().get(topic_id)
