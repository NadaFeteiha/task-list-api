from flask import Blueprint, make_response, abort, request, Response
from ..models.goal import Goal
from ..db import db

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


# ===============================================================================
#                                 Get
# ===============================================================================


@goal_bp.get("")
def get_goals():
    """Get all goals"""
    query = db.select(Goal)
    goals = db.session.scalars(query).all()

    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())

    return goals_response, 200


@goal_bp.get("/<goal_id>")
def get_specific_goal(goal_id):
    """Get a specific goal by ID"""
    goal = validate_goal(goal_id)

    return goal.to_dict(), 200


# ===============================================================================
#                                 Create
# ===============================================================================


@goal_bp.post("")
def create_goal():
    """Create a new goal"""

    request_body = request.get_json()
    new_goal = validate_goal_data(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dict(), 201


# ===============================================================================
#                                 Update
# ===============================================================================


# ===============================================================================
#                                 Delete
# ===============================================================================


# ===============================================================================
#                               Helper Functions
# ===============================================================================


def validate_goal(goal_id):
    """Validate goal ID and return the corresponding Goal object"""
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"detail": "Invalid goal ID"}, 400))

    goal = db.session.get(Goal, goal_id)

    if not goal:
        abort(make_response({"detail": "Goal not found"}, 404))

    return goal


def validate_goal_data(request_body):
    """Validate the request body for creating or updating a goal"""

    if "title" not in request_body:
        abort(make_response({"detail": "Missing title in request body"}, 400))

    return Goal.from_dict(request_body)
