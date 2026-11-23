# Grind

A lightweight web app for studying by topic. Each topic has a **lesson** to read, **practice** exercises you run and auto-check in the browser, and a timed multiple-choice **quiz**. Users create an account, work through a topic, take the quiz against the clock, and get a score with a full review of their answers and the explanations. They can retake any quiz and see every past result.

Built with Flask. It stores data in Postgres (for example [Neon](https://neon.tech)) when `DATABASE_URL` is set, and in a local SQLite file otherwise. No JavaScript framework and no build step.

## Features

- Sign up and log in (passwords hashed, CSRF protected forms).
- **Topics**: the home page lists every topic with your lesson, practice and quiz progress. Opening a topic shows its Overview, Lesson, Practice and Quiz tabs.
- **Lessons**: one page per lesson section with a section list, "Mark as read" progress, syntax-highlighted code with a "Try it in the scratchpad" button on every Python example, and links to the practice exercises for that section.
- Timed exams. The deadline is enforced on the server: answers save as you go, the exam auto-submits at zero, and an attempt left open in a closed tab is graded on its saved answers once time is up.
- One question at a time with a navigator, flags, and keyboard shortcuts (A–D answer, ← → move, F flag).
- Results page with score, pass/fail, time used, a per-section breakdown, and a review of every question showing your answer, the correct answer and the explanation (filter by wrong, unanswered or correct).
- Retake any exam; "My results" lists every finished attempt.
- **Practice**: 54 auto-graded Python exercises for Python Basics, grouped by subject and linked to the lesson section they practise, each a notebook-style page with the task, examples, your code cell, a "Try it" cell, hints revealed one at a time, and a reference solution with an explanation. Your code saves as you type, and solved exercises are tracked per user.
- **Scratchpad**: free Python notebooks with code and Markdown cells that share variables like Jupyter, an optional stdin box for `input()`, and autosave.
- Light and dark mode, works on phones.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app wsgi run --debug
```

Open http://127.0.0.1:5000 and create an account. Without `DATABASE_URL`, data is stored in `instance/interviewiq.sqlite3`. To use Postgres locally, export `DATABASE_URL=postgresql://...` first. Tables are created automatically on startup. On macOS, run gunicorn locally without `--preload` when using Postgres: macOS's DNS resolver crashes (SIGSEGV) in workers forked after the master has connected. Linux hosts such as Render are unaffected.

Run the tests with `pip install -r requirements-dev.txt && pytest`. They run on SQLite; set `TEST_DATABASE_URL` to a throwaway Postgres database to run them on Postgres as well (its tables are dropped).

## Topics

Everything a topic needs lives in one folder under `topics/`. The folder name is the topic id used in URLs.

```
topics/
  python-basics/
    topic.json          {"title": "Python Basics", "description": "...", "order": 1}
    lesson.md           the lesson (optional)
    practice/*.md       practice exercises (optional)
    exams/*.json        timed quizzes (optional, one or more)
```

Add a folder and restart; the topic appears on the home page with whichever parts it has. Topics are sorted by `order`, then title. Exam and exercise ids must be unique across all topics, because saved attempts and practice progress are stored by id. Keep an id unchanged once people have used it.

### Adding a topic from Markdown

If you have a lesson and a quiz written in Markdown, one command sets up the folder:

```bash
python tools/new_topic.py concepts-refresher --title "Python Concepts Refresher" \
  --description "..." --order 2 \
  --lesson "Python Concepts Refresher.md" \
  --quiz "Concepts Refresher Quiz.md" --minutes 45
```

It copies the lesson to `lesson.md`, converts the quiz into `exams/<id>.json`, writes `topic.json`, and creates an empty `practice/` folder. Every part is optional except `--title`.

### Lessons

`lesson.md` is ordinary Markdown (CommonMark plus tables). The `# ` title and the text before the first `## ` heading are the lesson's introduction. Each `## ` heading starts a section with its own page, in file order. A `## Table of Contents` section is skipped, since the app builds its own. Links to headings in the same file, such as `[section 17](#17-comprehensions-and-generator-expressions)`, go to the right section page. Links to other `.md` files are shown as plain text. Raw HTML in the file is not rendered.

A heading that starts with a number (`## 7. Lists`) gives the section that number. A practice exercise with `lesson: 7` in its front matter is listed under "Practice this" on that section, and its page links back to it.

Read progress is stored per user and section, keyed by the heading's anchor (`7-lists`). Renaming a heading resets its read mark.

### Quizzes

Quizzes are JSON files in a topic's `exams/` folder.

```json
{
  "id": "python-basics",
  "title": "Python Basics",
  "description": "Shown on the quiz card.",
  "duration_minutes": 60,
  "pass_percent": 70,
  "questions": [
    {
      "id": 1,
      "section": "Section 1 — Running Python",
      "prompt": "What command runs `hello.py`?",
      "options": [{"key": "A", "text": "`java hello.py`"}, {"key": "B", "text": "`python3 hello.py`"}],
      "answer": "B",
      "explanation": "`python3 hello.py` runs a script file."
    }
  ]
}
```

`prompt`, option `text` and `explanation` accept a small Markdown subset: fenced code blocks, `inline code`, **bold** and *italic*. `pass_percent` is optional (default 70).

If your quiz is written in Markdown in the same layout as the Python Basics quiz (`**Q1.**` questions with `A)` options, then an `## Answer Key` with `1. **B** — explanation` lines), convert it on its own with:

```bash
python tools/md_to_exam.py "My Quiz.md" topics/my-topic/exams/my-quiz.json \
  --id my-quiz --title "My Quiz" --minutes 45 --description "..."
```

The converter checks that every question has an answer in the key and that the answer is one of its options.

### Timing

Python Basics has 130 questions in 60 minutes, about 28 seconds per question. That is deliberately tight. Change `duration_minutes` in the JSON to adjust it.

## Practice exercises

Python for the Practice section runs **in the browser**, never on the server: [Pyodide](https://pyodide.org) (CPython compiled to WebAssembly) runs in a Web Worker, so a stuck loop can be stopped without freezing the page. Submit times out after 10 seconds. The first visit downloads Pyodide (about 10 MB, then cached by the browser). Pages load it from jsDelivr; set `PYODIDE_URL` to host it elsewhere. The code editor is CodeMirror 5 from cdnjs, with a plain textarea as a fallback.

Grading happens in the browser too, so the server trusts the result it is sent. That's fine for self-study, but don't use it for proctored tests.

Exercises are Markdown files in a topic's `practice/` folder, one per file, listed in filename order. Add a file and restart to publish it:

````markdown
---
id: two-sum
title: Two Sum
topic: Lists                # group heading on the topic's Practice page
difficulty: easy            # easy, medium or hard
lesson: 7                   # optional: the lesson section it practises
---

## Prompt
Markdown text. `code`, **bold**, fenced code and "- " lists work.

## Starter
```python
def two_sum(nums, target):
    pass
```

## Examples
```python
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
```

## Tests
```python
assert two_sum([3, 3], 6) == [0, 1]
```

## Hints
- One bullet per hint, revealed one at a time.

## Solution
```python
def two_sum(nums, target): ...
```

## Explanation
Optional Markdown shown with the solution.
````

Every top-level `assert` in Examples or Tests is one test. Examples are shown to the learner; Tests stay hidden, though for a failed `assert x == y` the learner still sees what they got and what was expected. Any other statement in those blocks runs as setup. `pytest` runs each reference solution through the same runner the browser uses (`app/static/practice/runner.py`), so a broken exercise fails the build. It also checks that the starter code does not already pass.

## Deploy to Render with Neon

1. In [Neon](https://console.neon.tech), create a project and copy its connection string (it looks like `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`). The pooled connection string works too.
2. In Render choose **New → Blueprint**, pick this repo, and apply. When asked for `DATABASE_URL`, paste the Neon pooled connection string (host ends in `-pooler`); optionally set `DATABASE_URL_UNPOOLED` to the direct one, which is used only to create tables at startup.

The Blueprint creates a free web service running gunicorn and generates a `SECRET_KEY`. The app creates its tables in Neon on first start. Because all data lives in Neon, Render's free instance is fine: redeploys and restarts lose nothing. Free Render services sleep after 15 minutes idle, so the first request after a quiet spell takes a few extra seconds.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | random, saved in `instance/secret_key` | Signs session cookies |
| `DATABASE_URL` | unset | Postgres connection string (e.g. Neon pooled URL). When set, Postgres is used instead of SQLite |
| `DATABASE_URL_UNPOOLED` | unset | Optional direct (non-pooled) Postgres URL, used only for schema creation at startup |
| `INTERVIEWIQ_DB` | `instance/interviewiq.sqlite3` | SQLite database path, used when `DATABASE_URL` is unset |
| `GRIND_TOPICS` | `topics/` | Folder of topic folders |
| `PYODIDE_URL` | `https://cdn.jsdelivr.net/npm/pyodide@0.29.5/` | Where browsers load Pyodide from (must end with `/`) |
