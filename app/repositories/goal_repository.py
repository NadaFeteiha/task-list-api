from ..models.goal import Goal
from .base_repository import BaseRepository


class GoalRepository(BaseRepository):
    """Database access for goals"""

    model = Goal
