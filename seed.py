from datetime import datetime

from dotenv import load_dotenv

from app import create_app, db
from app.models.goal import Goal
from app.models.task import Task

load_dotenv()

GOALS = {
    "Keep a healthy home": [
        ("Water the garden", "Water all the plants in the backyard", None),
        ("Buy groceries", "Milk, eggs, bread, and coffee", None),
        ("Clean the kitchen", "Wash dishes and wipe the counters", datetime(2026, 10, 17, 9, 0)),
    ],
    "Finish the Ada program": [
        ("Finish project", "Complete waves 1-3 of the task list API", None),
        ("Deploy to Render", "Deploy the task list API to production", None),
    ],
    "Take care of myself": [
        ("Call mom", "Weekly check-in call", datetime(2026, 10, 15, 18, 30)),
        ("Read a book", "Read two chapters before bed", None),
        ("Go for a walk", "30 minutes outside", None),
    ],
}


def get_or_create(cls, title, **fields):
    """Return the row with this title, creating it if it doesn't exist yet"""
    model = db.session.scalar(db.select(cls).where(cls.title == title))
    if model is None:
        model = cls(title=title, **fields)
        db.session.add(model)
    return model


my_app = create_app()
with my_app.app_context():
    for goal_title, tasks in GOALS.items():
        goal = get_or_create(Goal, goal_title)
        for title, description, completed_at in tasks:
            task = get_or_create(
                Task, title, description=description, completed_at=completed_at
            )
            task.goal = goal

    get_or_create(Task, "Plan the weekend", description="No goal for this one", completed_at=None)

    db.session.commit()
    print(
        f"Seeded: {db.session.query(Goal).count()} goals, "
        f"{db.session.query(Task).count()} tasks"
    )
