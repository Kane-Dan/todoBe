from sqlalchemy import Column, MetaData, String, Boolean, Integer
from src.database import Base
from sqlalchemy.orm import relationship
from src.tasks.models import Task

metadata = MetaData()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    number = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    
    tasks = relationship("Task", back_populates="user")