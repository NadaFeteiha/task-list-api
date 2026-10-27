from flask import Flask
from .db import db, migrate
from .errors import ServiceError
from .models import task, goal
from .routes.task_routes import task_bp, get_tasks
from .routes.goal_routes import goal_bp
from .routes.route_utilities import error_response
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

    # Turn errors raised by schemas and services into 400/404 JSON responses
    app.register_error_handler(ServiceError, error_response)

    # default route
    app.add_url_rule("/", view_func=get_tasks)

    return app
