"""Convert a quiz written in Markdown into an exam JSON file.

Expected Markdown layout (see the Python Basics quiz for an example):

    ## Section heading
    **Q1.** Question text (may span lines / include ```code``` blocks)
    A) option
    B) option
    ...
    ## Answer Key
    ### Section heading
    1. **B** — explanation

Usage:
    python tools/md_to_exam.py QUIZ.md topics/my-topic/exams/my-exam.json \
        --id my-exam --title "My Exam" --minutes 60 [--description "..."]
"""
import argparse
import json
import re
import sys

Q_RE = re.compile(r"^\*\*Q(\d+)\.\*\*\s*(.*)$")
OPT_RE = re.compile(r"^([A-H])\)\s*(.*)$")
KEY_RE = re.compile(r"^(\d+)\.\s+\*\*([A-H])\*\*(?:\s*\([^)]*\))?\s*[—–-]+\s*(.*)$")


def parse(md: str):
    lines = md.splitlines()
    try:
        key_start = next(i for i, l in enumerate(lines) if l.strip().lower() == "## answer key")
    except StopIteration:
        sys.exit("No '## Answer Key' heading found")

    questions, section, cur, in_code = [], None, None, False
    for line in lines[:key_start]:
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("## "):
            section = line[3:].strip()
            cur = None
            continue
        m = None if in_code else Q_RE.match(line)
        if m:
            cur = {"id": int(m.group(1)), "section": section, "prompt": [m.group(2)] if m.group(2) else [], "options": []}
            questions.append(cur)
            continue
        if cur is None:
            continue
        om = None if in_code else OPT_RE.match(line)
        if om:
            cur["options"].append({"key": om.group(1), "text": om.group(2).strip()})
        elif not cur["options"] and line.strip() != "---":
            cur["prompt"].append(line)

    answers = {}
    for line in lines[key_start:]:
        km = KEY_RE.match(line.strip())
        if km:
            answers[int(km.group(1))] = (km.group(2), km.group(3).strip())

    for q in questions:
        q["prompt"] = "\n".join(q["prompt"]).strip()
        if q["id"] not in answers:
            sys.exit(f"Q{q['id']} has no answer in the key")
        q["answer"], q["explanation"] = answers[q["id"]]
        if q["answer"] not in {o["key"] for o in q["options"]}:
            sys.exit(f"Q{q['id']}: answer {q['answer']} is not one of its options")
    return questions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown")
    ap.add_argument("output")
    ap.add_argument("--id", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--minutes", type=int, required=True)
    ap.add_argument("--description", default="")
    a = ap.parse_args()
    with open(a.markdown, encoding="utf-8") as f:
        qs = parse(f.read())
    exam = {"id": a.id, "title": a.title, "description": a.description,
            "duration_minutes": a.minutes, "questions": qs}
    with open(a.output, "w", encoding="utf-8") as f:
        json.dump(exam, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(qs)} questions to {a.output}")


if __name__ == "__main__":
    main()
