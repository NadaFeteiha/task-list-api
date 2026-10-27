from ..errors import ValidationError
from .base_schema import validate_title


def validate_task_create(request_body):
    """Check the body of a create-task request"""
    validate_title(request_body)


def validate_task_update(request_body):
    """Check the body of an update-task request has a title or description"""
    validate_title(request_body)

    if "title" not in request_body and "description" not in request_body:
        raise ValidationError("Invalid data")
