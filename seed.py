from datetime import datetime

from dotenv import load_dotenv

from app import create_app, db
from app.models.task import Task

load_dotenv()

my_app = create_app()
with my_app.app_context():
    db.session.add(Task(title="Water the garden", description="Water all the plants in the backyard", completed_at=None))
    db.session.add(Task(title="Buy groceries", description="Milk, eggs, bread, and coffee", completed_at=None))
    db.session.add(Task(title="Finish project", description="Complete waves 1-3 of the task list API", completed_at=None))
    db.session.add(Task(title="Call mom", description="Weekly check-in call", completed_at=datetime(2026, 10, 15, 18, 30)))
    db.session.add(Task(title="Clean the kitchen", description="Wash dishes and wipe the counters", completed_at=datetime(2026, 10, 17, 9, 0)))
    db.session.add(Task(title="Read a book", description="Read two chapters before bed", completed_at=None))
    db.session.commit()
