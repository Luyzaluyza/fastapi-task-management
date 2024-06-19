from fastapi import FastAPI
from app.controllers import ControllerTask
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ControllerTask.router)


@app.get("/")
def read_root():
    return {"message": "Documentation"}