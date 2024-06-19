import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine  

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_task(test_client):
    response = test_client.post("/tasks/", json={"title": "Tarefa teste", "description": "teste", "status": "pendente"})
    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa teste"

def test_get_tasks(test_client):
    response = test_client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task(test_client):
    response = test_client.post("/tasks/", json={"title": "Tarefa teste", "description": "teste", "status": "pendente"})
    task_id = response.json()["id"]
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task(test_client):
    response = test_client.post("/tasks/", json={"title": "Tarefa teste", "description": "teste", "status": "pendente"})
    task_id = response.json()["id"]
    response = test_client.put(f"/tasks/{task_id}", json={"title": "tarefa update", "description": "teste", "status": "completed"})
    assert response.status_code == 200
    assert response.json()["title"] == "tarefa update"

def test_delete_task(test_client):
    response = test_client.post("/tasks/", json={"title": "Tarefa teste", "description": "teste", "status": "pendente"})
    task_id = response.json()["id"]
    response = test_client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
