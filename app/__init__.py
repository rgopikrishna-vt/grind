import os
import secrets

from flask import Flask

from . import db, exams, auth, views, render


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.update(
        # Set DATABASE_URL to a postgres:// URL (e.g. Neon) to use Postgres; otherwise SQLite is used.
        DATABASE_URL=os.environ.get("DATABASE_URL", ""),
        DATABASE=os.environ.get("INTERVIEWIQ_DB", os.path.join(app.instance_path, "interviewiq.sqlite3")),
        EXAMS_DIR=os.environ.get("INTERVIEWIQ_EXAMS", os.path.join(os.path.dirname(app.root_path), "exams")),
        # Seconds of slack after the deadline for the final auto-submit request to arrive.
        SUBMIT_GRACE_SECONDS=15,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )
    if test_config:
        app.config.update(test_config)
    app.config["SECRET_KEY"] = app.config.get("SECRET_KEY") or os.environ.get("SECRET_KEY") or _instance_secret(app)

    db.init_app(app)
    exams.init_app(app)
    render.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    return app


def _instance_secret(app):
    """Persist a random secret key in the instance folder so sessions survive restarts."""
    path = os.path.join(app.instance_path, "secret_key")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(secrets.token_hex(32))
    with open(path) as f:
        return f.read().strip()
