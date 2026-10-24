from flask import abort, make_response
from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError
from ..db import db

# ===============================================================================
#                                 Helpers
# ===============================================================================


def validate_model(cls, model_id):
    """Return the model instance with the given id, or abort with 400/404"""
    try:
        if isinstance(model_id, bool):
            raise ValueError
        model_id = int(model_id)
    except (TypeError, ValueError):
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


def create_model_with_response(cls, model_data):
    """Create and save a new model instance from request data"""
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_model)
    commit_or_abort()

    return new_model.to_dict(), 201


def update_model(model, model_data, allowed_fields):
    """Update the allowed attributes of a model instance from request data"""
    for field in allowed_fields:
        if field in model_data and hasattr(model, field):
            setattr(model, field, model_data[field])

    commit_or_abort()


def get_models_with_filters(cls, filters=None, serialize=None):
    """Return all model instances as dicts, using serialize (default: to_dict)"""
    serialize = serialize or cls.to_dict
    query = db.select(cls)
    filters = dict(filters or {})

    sort = filters.pop("sort", None)

    for attribute, value in filters.items():
        if not hasattr(cls, attribute):
            continue
        column = getattr(cls, attribute)
        if isinstance(getattr(column, "type", None), String):
            query = query.where(column.ilike(f"%{value}%"))

    title = getattr(cls, "title")
    if sort == "asc":
        query = query.order_by(title.asc(), getattr(cls, "id"))
    elif sort == "desc":
        query = query.order_by(title.desc(), getattr(cls, "id"))
    else:
        query = query.order_by(getattr(cls, "id"))

    models = db.session.scalars(query)
    return [serialize(model) for model in models]


def commit_or_abort():
    """Commit the session, or roll it back and abort with 400 on a database error"""
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(make_response({"details": "Invalid data"}, 400))


def validate_title(request_body):
    """Reject a non-object body, or a title that is not a non-empty string"""
    if not isinstance(request_body, dict):
        abort(make_response({"details": "Invalid data"}, 400))

    if "title" not in request_body:
        return

    title = request_body["title"]
    if not isinstance(title, str) or not title.strip():
        abort(make_response({"details": "Invalid data, title cannot be empty"}, 400))
