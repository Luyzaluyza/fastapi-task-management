from sqlalchemy.orm import Session
from app.repositories import task_repository
from app.models.task_schema import Task

def create_task(db: Session, title: str, description: str, status: str) -> Task:
    return task_repository.create_task(db, title=title, description=description, status=status)

def get_task(db: Session, task_id: int) -> Task:
    return task_repository.get_task(db, task_id)

def update_task(db: Session, task_id: int, title: str, description: str, status: str) -> Task:
    return task_repository.update_task(db, task_id, title=title, description=description, status=status)

def delete_task(db: Session, task_id: int) -> Task:
    return task_repository.delete_task(db, task_id)

def get_all_tasks(db: Session) -> list[Task]:
    return task_repository.get_all_tasks(db)
