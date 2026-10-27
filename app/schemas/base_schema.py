from ..errors import ValidationError


def validate_title(request_body):
    """Reject a non-object body, or a title that is not a non-empty string"""
    if not isinstance(request_body, dict):
        raise ValidationError("Invalid data")

    if "title" not in request_body:
        return

    title = request_body["title"]
    if not isinstance(title, str) or not title.strip():
        raise ValidationError("Invalid data, title cannot be empty")
