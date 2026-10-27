from datetime import datetime
from ..repositories.task_repository import TaskRepository
from .base_service import BaseService
from .slack import send_slack_notification


class TaskService(BaseService):
    """Business operations for tasks"""

    updatable_fields = ("title", "description")

    def mark_complete(self, task):
        """Mark the task complete and announce it on Slack"""
        task.completed_at = datetime.now()
        self.repository.commit()

        send_slack_notification(f"Someone just completed the task {task.title}")

    def mark_incomplete(self, task):
        """Mark the task incomplete"""
        task.completed_at = None
        self.repository.commit()


task_service = TaskService(TaskRepository())
