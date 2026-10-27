from ..db import db
from ..models.task import Task
from .base_repository import BaseRepository


class TaskRepository(BaseRepository):
    """Database access for tasks"""

    model = Task

    def find_incomplete(self):
        """Return the tasks that have not been completed, ordered by id"""
        query = db.select(Task).where(Task.completed_at.is_(None)).order_by(Task.id)
        return list(db.session.scalars(query))

    def find_by_goal(self, goal_id):
        """Return the tasks that belong to the goal with the given id, ordered by id"""
        query = db.select(Task).where(Task.goal_id == goal_id).order_by(Task.id)
        return list(db.session.scalars(query))
