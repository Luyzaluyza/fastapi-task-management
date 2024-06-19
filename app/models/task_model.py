from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime, timezone, timedelta

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="Pendente")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=-3))))


