from sqlalchemy.orm import Session
from app.models.task_model import Task

def create_task(db: Session, title: str, description: str, status: str):
    db_task = Task(title=title, description=description, status=status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, title: str, description: str, status: str):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db_task.title = title
    db_task.description = description
    db_task.status = status
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(db_task)
    db.commit()
    return db_task

def get_all_tasks(db: Session):
    return db.query(Task).all()
