from flask import Blueprint, make_response, abort, request, Response
from ..models.task import Task
from ..db import db
from .route_utilities import (
    validate_model,
    create_model_with_response,
    get_models_with_filters,
)
from ..services.slack import send_slack_notification


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# ================================================================================
#                                 Get
# ================================================================================


@task_bp.get("")
def get_tasks():
    """Get all tasks"""
    return get_models_with_filters(Task, request.args), 200


@task_bp.get("/<task_id>")
def get_task(task_id):
    """Get task by id"""
    task_response = validate_model(Task, task_id).to_dict()
    return task_response, 200


# ================================================================================
#                                 Create
# ================================================================================


@task_bp.post("")
def create_tasks():
    """create new task"""
    request_body = request.get_json()
    validate_task_data(request_body)
    return create_model_with_response(Task, request_body)


# ================================================================================
#                                 Update
# ================================================================================


@task_bp.put("/<task_id>")
def update_task(task_id):
    """update task by id"""
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    validate_update_task_data(request_body)

    if "title" in request_body:
        task.title = request_body["title"]

    if "description" in request_body:
        task.description = request_body["description"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@task_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    """mark task as complete"""
    task = validate_model(Task, task_id)
    task.completed_at = db.func.now()
    db.session.commit()

    send_slack_notification(f"Someone just completed the task {task.title}")
    return Response(status=204, mimetype="application/json")


@task_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    """mark task as incomplete"""
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")


# ================================================================================
#                                 Delete
# ================================================================================


@task_bp.delete("/<task_id>")
def delete_task(task_id):
    """delete task by id"""
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


# ================================================================================
#                           Helper function
# ================================================================================


def validate_task_data(request_body):
    """check if request body is valid"""

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    if request_body["title"] == "" or request_body["description"] == "":
        abort(
            make_response(
                {"details": "Invalid data, title and description cannot be empty"}, 400
            )
        )


def validate_update_task_data(request_body):
    """check if request body is valid"""
    if "title" not in request_body and "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    for field in ("title", "description"):
        if field in request_body and request_body[field] == "":
            abort(
                make_response(
                    {"details": f"Invalid data, {field} cannot be empty"}, 400
                )
            )
