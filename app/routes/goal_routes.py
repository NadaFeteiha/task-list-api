from flask import Blueprint, make_response, abort, request, Response
from ..models.goal import Goal
from ..models.task import Task
from ..db import db
from .route_utilities import (
    validate_model,
    create_model_with_response,
    get_models_with_filters,
)

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


# ===============================================================================
#                                 Get
# ===============================================================================


@goal_bp.get("")
def get_goals():
    """Get all goals"""
    return get_models_with_filters(Goal, request.args), 200


@goal_bp.get("/<goal_id>")
def get_specific_goal(goal_id):
    """Get a specific goal by ID"""
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200


@goal_bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    """Get a specific goal with its associated tasks"""
    goal = validate_model(Goal, goal_id)

    goal_response = goal.to_dict()
    goal_response["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_response, 200


# ===============================================================================
#                                 Create
# ===============================================================================


@goal_bp.post("")
def create_goal():
    """Create a new goal"""

    request_body = request.get_json()
    return create_model_with_response(Goal, request_body)


@goal_bp.post("/<goal_id>/tasks")
def add_tasks_id_to_goal(goal_id):
    """Associate task IDs with a specific goal"""

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body.get("task_ids")
    if not isinstance(task_ids, list):
        abort(make_response({"details": "Invalid data"}, 400))

    # Find each task (404 if one doesn't exist)
    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks.append(task)

    # Replace the goal's old tasks with the new list
    goal.tasks = tasks
    db.session.commit()

    return {"id": goal.id, "task_ids": task_ids}, 200


# ===============================================================================
#                                 Update
# ===============================================================================


@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    """Update an existing goal by ID"""

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# ===============================================================================
#                                 Delete
# ===============================================================================


@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    """Delete a goal by ID"""

    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
