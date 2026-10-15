from flask import Blueprint
from ..models.task import Task
from ..db import db


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
