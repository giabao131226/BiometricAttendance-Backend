
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department_code = Column(String(20), unique=True, nullable=False)
    department_name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    head_of_department = Column(String(150), nullable=True)
    email = Column(String(150), nullable=False)
    phone = Column(String(15), nullable=False)
    status = Column(String(10), default="active", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
