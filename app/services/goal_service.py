from ..repositories.goal_repository import GoalRepository
from .base_service import BaseService
from .task_service import task_service


class GoalService(BaseService):
    """Business operations for goals"""

    updatable_fields = ("title",)

    def __init__(self, repository, task_service):
        super().__init__(repository)
        self.task_service = task_service

    def assign_tasks(self, goal, task_ids):
        """Replace the goal's tasks with the tasks with the given ids"""
        # Find each task first, so a bad id leaves the goal unchanged
        goal.tasks = [self.task_service.get(task_id) for task_id in task_ids]
        self.repository.commit()


goal_service = GoalService(GoalRepository(), task_service)
