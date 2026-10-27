from flask import abort, make_response
from ..errors import NotFoundError, ServiceError
from ..models.goal import Goal
from ..models.task import Task
from ..services.goal_service import goal_service
from ..services.task_service import task_service

SERVICES = {Task: task_service, Goal: goal_service}

# ===============================================================================
#                                 Helpers
# ===============================================================================


def error_response(error):
    """Turn a service-layer error into a JSON response with 404 or 400"""
    status = 404 if isinstance(error, NotFoundError) else 400
    return make_response({"details": error.message}, status)


def validate_model(cls, model_id):
    """Return the model instance with the given id, or abort with 400/404"""
    try:
        return SERVICES[cls].get(model_id)
    except ServiceError as error:
        abort(error_response(error))


def create_model_with_response(cls, model_data):
    """Create and save a new model instance from request data"""
    try:
        new_model = SERVICES[cls].create(model_data)
    except ServiceError as error:
        abort(error_response(error))

    return new_model.to_dict(), 201
