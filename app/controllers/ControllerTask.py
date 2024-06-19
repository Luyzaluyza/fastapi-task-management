from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import task_service
from app.models.task_schema import Task, TaskCreate, TaskUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_service.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Por favor passe um id valido")
    return db_task

@router.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db=db, title=task.title, description=task.description, status=task.status)

@router.get("/tasks/", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_all_tasks(db=db)
@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db=db, task_id=task_id, title=task.title, description=task.description, status=task.status)

@router.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.delete_task(db=db, task_id=task_id)
