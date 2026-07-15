from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db import Base  

class User(Base):
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    reports = relationship("Reports", back_populates="user")


class Reports(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_text = Column(Text)
    result = Column(Text)

    user = relationship("User", back_populates="reports")