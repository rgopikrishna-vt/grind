"""Database access for SQLite (local default) or Postgres (e.g. Neon) when DATABASE_URL is set.

Queries are written once with `?` placeholders; the Postgres wrapper translates them to `%s`.
"""
import sqlite3
from datetime import datetime, timezone

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id {pk},
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users (lower(username));
CREATE TABLE IF NOT EXISTS attempts (
    id {pk},
    user_id INTEGER NOT NULL REFERENCES users(id),
    exam_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    deadline TEXT NOT NULL,
    submitted_at TEXT,
    status TEXT NOT NULL DEFAULT 'in_progress',
    score INTEGER,
    total INTEGER
);
CREATE INDEX IF NOT EXISTS idx_attempts_user ON attempts (user_id, exam_id);
CREATE TABLE IF NOT EXISTS answers (
    attempt_id INTEGER NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL,
    choice TEXT NOT NULL,
    PRIMARY KEY (attempt_id, question_id)
);
CREATE TABLE IF NOT EXISTS practice_progress (
    user_id INTEGER NOT NULL REFERENCES users(id),
    exercise_id TEXT NOT NULL,
    code TEXT,
    attempts INTEGER NOT NULL DEFAULT 0,
    hints_used INTEGER NOT NULL DEFAULT 0,
    solution_viewed INTEGER NOT NULL DEFAULT 0,
    solved_at TEXT,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (user_id, exercise_id)
);
CREATE TABLE IF NOT EXISTS lesson_progress (
    user_id INTEGER NOT NULL REFERENCES users(id),
    topic_id TEXT NOT NULL,
    section_id TEXT NOT NULL,
    read_at TEXT NOT NULL,
    PRIMARY KEY (user_id, topic_id, section_id)
);
CREATE TABLE IF NOT EXISTS notebooks (
    id {pk},
    user_id INTEGER NOT NULL REFERENCES users(id),
    title TEXT NOT NULL,
    cells TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notebooks_user ON notebooks (user_id, updated_at);
"""
SQLITE_PK = "INTEGER PRIMARY KEY AUTOINCREMENT"
POSTGRES_PK = "INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY"


class IntegrityError(Exception):
    """Raised for unique-constraint violations on either backend."""


def now():
    return datetime.now(timezone.utc)


def to_iso(dt):
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def from_iso(s):
    return datetime.fromisoformat(s) if s else None


def is_postgres(url):
    return bool(url) and url.startswith(("postgres://", "postgresql://"))


class _PostgresDB:
    """Minimal sqlite3-like facade over a psycopg connection."""

    def __init__(self, url):
        import psycopg
        from psycopg.rows import dict_row

        self._errors = psycopg.errors
        # Neon's -pooler endpoint is PgBouncer in transaction mode: disable psycopg's
        # automatic server-side prepared statements so pooled backends can be swapped freely.
        self.conn = psycopg.connect(url, row_factory=dict_row, connect_timeout=15, prepare_threshold=None)

    def execute(self, sql, params=()):
        try:
            return self.conn.execute(sql.replace("?", "%s"), params)
        except self._errors.UniqueViolation as e:
            self.conn.rollback()
            raise IntegrityError(str(e)) from e
        except Exception:
            self.conn.rollback()
            raise

    def executescript(self, sql):
        self.conn.execute(sql)
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class _SqliteDB:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def execute(self, sql, params=()):
        try:
            return self.conn.execute(sql, params)
        except sqlite3.IntegrityError as e:
            raise IntegrityError(str(e)) from e

    def executescript(self, sql):
        self.conn.executescript(sql)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


def _connect(app, direct=False):
    url = app.config.get("DATABASE_URL")
    # Schema changes go over the direct connection when one is configured (Neon recommends
    # unpooled connections for migrations); request traffic uses the pooled DATABASE_URL.
    if direct and is_postgres(url) and is_postgres(app.config.get("DATABASE_URL_UNPOOLED")):
        url = app.config["DATABASE_URL_UNPOOLED"]
    if is_postgres(url):
        return _PostgresDB(url)
    return _SqliteDB(app.config["DATABASE"])


def get_db():
    if "db" not in g:
        g.db = _connect(current_app)
    return g.db


def close_db(_=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    db = _connect(app, direct=True)
    try:
        pk = POSTGRES_PK if is_postgres(app.config.get("DATABASE_URL")) else SQLITE_PK
        db.executescript(SCHEMA.format(pk=pk))
    finally:
        db.close()
