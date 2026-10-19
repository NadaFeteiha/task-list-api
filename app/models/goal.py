from sqlalchemy.orm import Mapped, mapped_column
from ..db import db


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False, min_length=4, max_length=250)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
        }

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls()
        new_goal.title = goal_data["title"]
        return new_goal
