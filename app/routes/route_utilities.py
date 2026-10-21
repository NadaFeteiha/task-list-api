from flask import abort, make_response
from ..db import db

# ===============================================================================
#                                 Helpers
# ===============================================================================


def validate_model(cls, model_id):
    """Return the model instance with the given id, or abort with 400/404"""
    try:
        model_id = int(model_id)
    except ValueError:
        abort(
            make_response(
                {"details": f"Invalid {cls.__name__.lower()} id: {model_id}"}, 400
            )
        )

    model = db.session.get(cls, model_id)

    if not model:
        abort(
            make_response(
                {"details": f"{cls.__name__} with id = {model_id} not found"}, 404
            )
        )

    return model


def create_model(cls, model_data):
    """Create and save a new model instance from request data"""
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201
