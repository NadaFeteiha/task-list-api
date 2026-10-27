from ..errors import NotFoundError, ValidationError


class BaseService:
    """Business operations shared by every model, built on a repository"""

    updatable_fields = ()

    def __init__(self, repository):
        self.repository = repository

    @property
    def model_name(self):
        return self.repository.model.__name__

    def get(self, model_id):
        """Return the record with the given id, or raise ValidationError/NotFoundError"""
        try:
            if isinstance(model_id, bool):
                raise ValueError
            model_id = int(model_id)
        except (TypeError, ValueError):
            raise ValidationError(f"Invalid {self.model_name.lower()} id: {model_id}")

        model = self.repository.get_by_id(model_id)

        if not model:
            raise NotFoundError(f"{self.model_name} with id = {model_id} not found")

        return model

    def list_all(self, filters=None):
        """Return all records matching the filters; a "sort" filter orders by title"""
        filters = dict(filters or {})
        sort = filters.pop("sort", None)
        return self.repository.find_all(filters, sort)

    def create(self, model_data):
        """Build a record from request data and save it"""
        try:
            new_model = self.repository.model.from_dict(model_data)
        except KeyError:
            raise ValidationError("Invalid data")

        self.repository.add(new_model)
        self.repository.commit()
        return new_model

    def update(self, model, model_data):
        """Copy the updatable fields present in the request data onto the record"""
        for field in self.updatable_fields:
            if field in model_data:
                setattr(model, field, model_data[field])

        self.repository.commit()

    def delete(self, model):
        """Delete the record"""
        self.repository.delete(model)
        self.repository.commit()
