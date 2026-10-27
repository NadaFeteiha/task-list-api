from flask import Blueprint, request, Response
from ..models.task import Task
from ..schemas.task_schema import validate_task_create, validate_task_update
from ..services.task_service import task_service
from .route_utilities import validate_model, create_model_with_response


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# ================================================================================
#                                 Get
# ================================================================================


@task_bp.get("")
def get_tasks():
    """Get all tasks"""
    tasks = task_service.list_all(request.args)
    return [task.to_dict_with_goal() for task in tasks], 200


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
    validate_task_create(request_body)
    return create_model_with_response(Task, request_body)


# ================================================================================
#                                 Update
# ================================================================================


@task_bp.put("/<task_id>")
def update_task(task_id):
    """update task by id"""
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    validate_task_update(request_body)

    task_service.update(task, request_body)
    return Response(status=204, mimetype="application/json")


@task_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    """mark task as complete"""
    task = validate_model(Task, task_id)
    task_service.mark_complete(task)
    return Response(status=204, mimetype="application/json")


@task_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    """mark task as incomplete"""
    task = validate_model(Task, task_id)
    task_service.mark_incomplete(task)
    return Response(status=204, mimetype="application/json")


# ================================================================================
#                                 Delete
# ================================================================================


@task_bp.delete("/<task_id>")
def delete_task(task_id):
    """delete task by id"""
    task = validate_model(Task, task_id)
    task_service.delete(task)
    return Response(status=204, mimetype="application/json")
