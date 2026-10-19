from flask import Blueprint, make_response, abort, request, Response
from ..models.task import Task
from ..db import db


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# ================================================================================
#                                 Get
# ================================================================================


@task_bp.get("")
def get_tasks():
    """Get all tasks"""
    query = db.select(Task)

    named_tasks = request.args.get("sort")
    if named_tasks == "asc":
        query = query.order_by(Task.title.asc())
    elif named_tasks == "desc":
        query = query.order_by(Task.title.desc())
    tasks = db.session.scalars(query).all()

    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response, 200


@task_bp.get("/<task_id>")
def get_task(task_id):
    """Get task by id"""
    task_response = validate_task(task_id).to_dict()
    return task_response, 200


# ================================================================================
#                                 Create
# ================================================================================


@task_bp.post("")
def create_tasks():
    """create new task"""
    request_body = request.get_json()
    new_task = validate_task_data(request_body)

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201


# ================================================================================
#                                 Update
# ================================================================================


@task_bp.put("/<task_id>")
def update_task(task_id):
    """update task by id"""
    task = validate_task(task_id)

    request_body = request.get_json()
    validate_update_task_data(request_body)

    if "title" in request_body:
        task.title = request_body["title"]

    if "description" in request_body:
        task.description = request_body["description"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


# ================================================================================
#                                 Delete
# ================================================================================


@task_bp.delete("/<task_id>")
def delete_task(task_id):
    """delete task by id"""
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


# ================================================================================
#                           Helper function
# ================================================================================


def validate_task(task_id):
    """check if id is valid"""
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"details": f"Invalid task id: {task_id}"}, 400))

    task = db.session.get(Task, task_id)

    if not task:
        abort(make_response({"details": f"Task with id = {task_id} not found"}, 404))

    return task


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

    if len(request_body["title"]) < 4 or len(request_body["description"]) < 4:
        abort(
            make_response(
                {
                    "details": "Invalid data, title and description must be at least 4 characters long"
                },
                400,
            )
        )
    return Task.from_dict(request_body)


def validate_update_task_data(request_body):
    """check if request body is valid"""
    if "title" not in request_body and "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    for field in ("title", "description"):
        if field in request_body and len(request_body[field]) < 4:
            abort(
                make_response(
                    {
                        "details": f"Invalid data, {field} must be at least 4 characters long"
                    },
                    400,
                )
            )
