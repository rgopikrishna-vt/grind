"""Create a new topic folder in topics/, optionally from a lesson and a quiz written in Markdown.

    python tools/new_topic.py my-topic --title "My Topic" \
        [--description "..."] [--order 2] \
        [--lesson "My Lesson.md"] \
        [--quiz "My Quiz.md" --minutes 45 [--quiz-title "My Topic Quiz"]]

It writes topics/my-topic/topic.json, copies the lesson to lesson.md, converts the quiz with
md_to_exam.py into exams/<topic id>.json, and makes an empty practice/ folder for exercises.
The lesson is checked the same way the app checks it at startup. Restart the app to see it.
"""
import argparse
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

from app.lesson import parse_lesson  # noqa: E402
from app.practice import ID_RE  # noqa: E402
from md_to_exam import parse as parse_quiz  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id", help="folder name and URL id: lowercase letters, digits and dashes")
    ap.add_argument("--title", required=True)
    ap.add_argument("--description", default="")
    ap.add_argument("--order", type=int, default=100, help="position on the home page (lower comes first)")
    ap.add_argument("--lesson", help="lesson Markdown file, split into sections at each '## ' heading")
    ap.add_argument("--quiz", help="quiz Markdown file in the md_to_exam.py layout")
    ap.add_argument("--minutes", type=int, help="quiz time limit (required with --quiz)")
    ap.add_argument("--quiz-title", help="defaults to the topic title")
    ap.add_argument("--topics-dir", default=os.path.join(ROOT, "topics"))
    a = ap.parse_args()

    if not ID_RE.match(a.id):
        sys.exit("id must be lowercase letters, digits and dashes")
    if a.quiz and not a.minutes:
        sys.exit("--minutes is required with --quiz")
    path = os.path.join(a.topics_dir, a.id)
    if os.path.exists(path):
        sys.exit(f"{path} already exists")

    lesson_text = None
    if a.lesson:
        with open(a.lesson, encoding="utf-8") as f:
            lesson_text = f.read()
        lesson = parse_lesson(lesson_text, a.id)  # raises if it has no sections
    questions = None
    if a.quiz:
        with open(a.quiz, encoding="utf-8") as f:
            questions = parse_quiz(f.read())

    os.makedirs(os.path.join(path, "practice"))
    with open(os.path.join(path, "topic.json"), "w", encoding="utf-8") as f:
        json.dump({"title": a.title, "description": a.description, "order": a.order}, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if lesson_text is not None:
        shutil.copyfile(a.lesson, os.path.join(path, "lesson.md"))
        print(f"Lesson: {len(lesson['sections'])} sections")
    if questions is not None:
        os.makedirs(os.path.join(path, "exams"))
        exam = {"id": a.id, "title": a.quiz_title or a.title, "description": a.description,
                "duration_minutes": a.minutes, "questions": questions}
        with open(os.path.join(path, "exams", f"{a.id}.json"), "w", encoding="utf-8") as f:
            json.dump(exam, f, indent=2, ensure_ascii=False)
        print(f"Quiz: {len(questions)} questions, {a.minutes} minutes")
    print(f"Created {os.path.relpath(path, ROOT)}/. Add exercises to its practice/ folder, then restart the app.")


if __name__ == "__main__":
    main()
