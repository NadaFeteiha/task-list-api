from ..errors import ValidationError
from .base_schema import validate_title


def validate_goal_create(request_body):
    """Check the body of a create-goal request"""
    validate_title(request_body)


def validate_goal_update(request_body):
    """Check the body of an update-goal request has a title"""
    validate_title(request_body)

    if "title" not in request_body:
        raise ValidationError("Invalid data")


def validate_goal_task_ids(request_body):
    """Check the body has a list of task ids, and return it"""
    if not isinstance(request_body, dict):
        raise ValidationError("Invalid data")

    task_ids = request_body.get("task_ids")
    if not isinstance(task_ids, list):
        raise ValidationError("Invalid data")

    return task_ids
