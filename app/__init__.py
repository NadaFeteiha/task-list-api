from flask import Flask
from .db import db, migrate
from .models import task, goal
from .routes.task_routes import task_bp, get_tasks
from .routes.goal_routes import goal_bp
import os
from dotenv import load_dotenv


load_dotenv()


def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(task_bp)
    app.register_blueprint(goal_bp)

    # default route
    app.add_url_rule("/", view_func=get_tasks)

    return app
