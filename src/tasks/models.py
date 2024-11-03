from sqlalchemy import Column, String, Boolean, Integer, ForeignKey,MetaData
from sqlalchemy.orm import relationship
from src.database import Base

# from src.users.models import User

metadata = MetaData()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_active = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")


    