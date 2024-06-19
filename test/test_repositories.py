import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.task_model import Task
from app.repositories import task_repository

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_task(db_session):
    task = task_repository.create_task(db_session, title="Task teste", description="Test Description", status="pendente")
    assert task.title == "Task teste"

def test_get_task(db_session):
    task = task_repository.create_task(db_session, title="Task teste", description="Test Description", status="pendente")
    fetched_task = task_repository.get_task(db_session, task.id)
    assert fetched_task.id == task.id

def test_update_task(db_session):
    task = task_repository.create_task(db_session, title="Task teste", description="Test Description", status="pendente")
    updated_task = task_repository.update_task(db_session, task.id, title="Updated Task", description="Updated Description", status="completed")
    assert updated_task.title == "Updated Task"

def test_delete_task(db_session):
    task = task_repository.create_task(db_session, title="Task teste", description="Test Description", status="pendente")
    deleted_task = task_repository.delete_task(db_session, task.id)
    assert deleted_task.id == task.id

def test_get_all_tasks(db_session):
    tasks = task_repository.get_all_tasks(db_session)
    assert isinstance(tasks, list)
