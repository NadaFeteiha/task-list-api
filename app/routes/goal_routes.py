from flask import Blueprint, request, Response
from ..models.goal import Goal
from ..schemas.goal_schema import (
    validate_goal_create,
    validate_goal_task_ids,
    validate_goal_update,
)
from ..services.goal_service import goal_service
from .route_utilities import validate_model, create_model_with_response

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


# ===============================================================================
#                                 Get
# ===============================================================================


@goal_bp.get("")
def get_goals():
    """Get all goals with their tasks"""
    goals = goal_service.list_all(request.args)
    return [goal.to_dict(include_tasks=True) for goal in goals], 200


@goal_bp.get("/<goal_id>")
def get_specific_goal(goal_id):
    """Get a specific goal by ID"""
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200


@goal_bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    """Get a specific goal with its associated tasks"""
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(include_tasks=True), 200


# ===============================================================================
#                                 Create
# ===============================================================================


@goal_bp.post("")
def create_goal():
    """Create a new goal"""

    request_body = request.get_json()
    validate_goal_create(request_body)
    return create_model_with_response(Goal, request_body)


@goal_bp.post("/<goal_id>/tasks")
def add_tasks_id_to_goal(goal_id):
    """Associate task IDs with a specific goal"""

    goal = validate_model(Goal, goal_id)
    task_ids = validate_goal_task_ids(request.get_json())

    goal_service.assign_tasks(goal, task_ids)

    return {"id": goal.id, "task_ids": task_ids}, 200


# ===============================================================================
#                                 Update
# ===============================================================================


@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    """Update an existing goal by ID"""

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    validate_goal_update(request_body)

    goal_service.update(goal, request_body)

    return Response(status=204, mimetype="application/json")


# ===============================================================================
#                                 Delete
# ===============================================================================


@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    """Delete a goal by ID"""

    goal = validate_model(Goal, goal_id)

    goal_service.delete(goal)

    return Response(status=204, mimetype="application/json")
