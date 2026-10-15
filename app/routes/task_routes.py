from flask import Blueprint, make_response, abort
from ..models.task import Task
from ..db import db


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.get("")
def get_tasks():
    """Get all tasks"""
    query = db.select(Task)
    tasks = db.session.scalars(query).all()
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response, 200


@task_bp.get("/<task_id>")
def get_task(task_id):
    """Get task by id"""
    task_response = validate_task(task_id).to_dict()
    return task_response, 200


# helper function
def validate_task(task_id):
    """check if id is valid"""
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"Invalid task id: {task_id}"}, 400))

    task = db.session.get(Task, task_id)

    if not task:
        abort(make_response({"message": f"Task with id {task_id} not found"}, 404))

    return task
