import os
import secrets

from dotenv import load_dotenv
from flask import Flask

from . import db, auth, views, render, practice_views, topic_views, topics


def _load_env_files():
    """Load .env.local then .env from the project root (e.g. DATABASE_URL pulled by `neon deploy`).
    Real environment variables always win, so Render's settings take precedence."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for name in (".env.local", ".env"):
        path = os.path.join(root, name)
        if os.path.exists(path):
            load_dotenv(path, override=False)


def create_app(test_config=None):
    if not (test_config or {}).get("TESTING"):
        _load_env_files()
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.update(
        # Set DATABASE_URL to a postgres:// URL (e.g. Neon) to use Postgres; otherwise SQLite is used.
        DATABASE_URL=os.environ.get("DATABASE_URL", ""),
        # Optional direct (non -pooler) Neon URL, used only for creating the schema at startup.
        DATABASE_URL_UNPOOLED=os.environ.get("DATABASE_URL_UNPOOLED", ""),
        DATABASE=os.environ.get("INTERVIEWIQ_DB", os.path.join(app.instance_path, "interviewiq.sqlite3")),
        # One folder per topic, each with its lesson, practice exercises and exams (see app/topics.py).
        TOPICS_DIR=os.environ.get("GRIND_TOPICS", os.path.join(os.path.dirname(app.root_path), "topics")),
        # Pyodide (Python for the browser) runs practice code client-side. Must end with "/".
        PYODIDE_URL=os.environ.get("PYODIDE_URL", "https://cdn.jsdelivr.net/npm/pyodide@0.29.5/"),
        # Seconds of slack after the deadline for the final auto-submit request to arrive.
        SUBMIT_GRACE_SECONDS=15,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config:
        app.config.update(test_config)
    app.config["SECRET_KEY"] = app.config.get("SECRET_KEY") or os.environ.get("SECRET_KEY") or _instance_secret(app)

    db.init_app(app)
    topics.init_app(app)
    render.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(practice_views.bp)
    app.register_blueprint(topic_views.bp)
    return app


def _instance_secret(app):
    """Persist a random secret key in the instance folder so sessions survive restarts."""
    path = os.path.join(app.instance_path, "secret_key")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(secrets.token_hex(32))
    with open(path) as f:
        return f.read().strip()
