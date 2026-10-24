from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    def to_dict_with_goal(self):
        task_dict = self.to_dict()
        if self.goal is not None:
            task_dict["goal_title"] = self.goal.title
        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls()
        new_task.title = task_data["title"]
        new_task.description = task_data["description"]
        new_task.completed_at = task_data.get("completed_at", None)
        return new_task
