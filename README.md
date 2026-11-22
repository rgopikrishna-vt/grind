# Grind

A lightweight web app for taking timed multiple-choice exams. Users create an account, pick an exam, take it against the clock, and get a score with a full review of their answers and the explanations. They can retake any exam and see every past result.

Built with Flask. It stores data in Postgres (for example [Neon](https://neon.tech)) when `DATABASE_URL` is set, and in a local SQLite file otherwise. No JavaScript framework and no build step.

## Features

- Sign up and log in (passwords hashed, CSRF protected forms).
- Dashboard of every available exam with your attempt count and best score.
- Timed exams. The deadline is enforced on the server: answers save as you go, the exam auto-submits at zero, and an attempt left open in a closed tab is graded on its saved answers once time is up.
- One question at a time with a navigator, flags, and keyboard shortcuts (A–D answer, ← → move, F flag).
- Results page with score, pass/fail, time used, a per-section breakdown, and a review of every question showing your answer, the correct answer and the explanation (filter by wrong, unanswered or correct).
- Retake any exam; "My results" lists every finished attempt.
- Light and dark mode, works on phones.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
flask --app wsgi run --debug
```

Open http://127.0.0.1:5000 and create an account. Without `DATABASE_URL`, data is stored in `instance/interviewiq.sqlite3`. To use Postgres locally, export `DATABASE_URL=postgresql://...` first. Tables are created automatically on startup.

Run the tests with `pip install -r requirements-dev.txt && pytest`. They run on SQLite; set `TEST_DATABASE_URL` to a throwaway Postgres database to run them on Postgres as well (its tables are dropped).

## Adding an exam

Exams are JSON files in `exams/`. Every `.json` file there shows up as an available exam on the next restart; nothing else needs to change.

```json
{
  "id": "python-basics",
  "title": "Python Basics",
  "description": "Shown on the exam card.",
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

If your quiz is written in Markdown in the same layout as the Python Basics quiz (`**Q1.**` questions with `A)` options, then an `## Answer Key` with `1. **B** — explanation` lines), convert it with:

```bash
python tools/md_to_exam.py "My Quiz.md" exams/my-quiz.json \
  --id my-quiz --title "My Quiz" --minutes 45 --description "..."
```

The converter checks that every question has an answer in the key and that the answer is one of its options.

### Timing

Python Basics has 130 questions in 60 minutes, about 28 seconds per question. That is deliberately tight. Change `duration_minutes` in the JSON to adjust it.

## Deploy to Render with Neon

1. In [Neon](https://console.neon.tech), create a project and copy its connection string (it looks like `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`). The pooled connection string works too.
2. In Render choose **New → Blueprint**, pick this repo, and apply. When asked for `DATABASE_URL`, paste the Neon connection string.

The Blueprint creates a free web service running gunicorn and generates a `SECRET_KEY`. The app creates its tables in Neon on first start. Because all data lives in Neon, Render's free instance is fine: redeploys and restarts lose nothing. Free Render services sleep after 15 minutes idle, so the first request after a quiet spell takes a few extra seconds.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_KEY` | random, saved in `instance/secret_key` | Signs session cookies |
| `DATABASE_URL` | unset | Postgres connection string (e.g. Neon). When set, Postgres is used instead of SQLite |
| `INTERVIEWIQ_DB` | `instance/interviewiq.sqlite3` | SQLite database path, used when `DATABASE_URL` is unset |
| `INTERVIEWIQ_EXAMS` | `exams/` | Folder of exam JSON files |
