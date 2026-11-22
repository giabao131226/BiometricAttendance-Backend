
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class Major(Base):
    __tablename__ = "major"

    id = Column(Integer, primary_key=True, index=True)
    major_code = Column(String(20), unique=True, nullable=False)
    major_name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    degree_level = Column(String(50), default="Đại học")
    duration = Column(Integer, nullable=False, default=4)
    status = Column(String(10), default="active", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("duration > 0", name="check_major_duration"),
        CheckConstraint("status IN ('active', 'inactive')", name="check_major_status"),
    )
