from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError
from ..db import db
from ..errors import PersistenceError


class BaseRepository:
    """Database access for a single model class"""

    model = None

    def get_by_id(self, model_id):
        """Return the record with the given id, or None"""
        return db.session.get(self.model, model_id)

    def find_all(self, filters=None, sort=None):
        """Return records matching the string filters, optionally sorted by title"""
        query = db.select(self.model)

        for attribute, value in (filters or {}).items():
            column = getattr(self.model, attribute, None)
            if isinstance(getattr(column, "type", None), String):
                query = query.where(column.ilike(f"%{value}%"))

        if sort == "asc":
            query = query.order_by(self.model.title.asc(), self.model.id)
        elif sort == "desc":
            query = query.order_by(self.model.title.desc(), self.model.id)
        else:
            query = query.order_by(self.model.id)

        return list(db.session.scalars(query))

    def add(self, model):
        """Stage a new record to be saved on the next commit"""
        db.session.add(model)

    def delete(self, model):
        """Stage a record to be deleted on the next commit"""
        db.session.delete(model)

    def commit(self):
        """Save staged changes, or roll back and raise PersistenceError"""
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise PersistenceError("Invalid data")
