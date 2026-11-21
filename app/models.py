from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)

    students = relationship("Student", back_populates="faculty")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(30), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    class_code = Column(String(30), nullable=True, default="66CNTT2")
    password_hash = Column(String(255), nullable=True)
    biometric_ref = Column(String(255), nullable=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=True)

    faculty = relationship("Faculty", back_populates="students")
    attendances = relationship("AttendanceLog", back_populates="student")


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_name = Column(String(150), nullable=False, default="Công nghệ Phần mềm")
    method = Column(String(50), nullable=False, default="Khuôn mặt + Vân tay")
    accuracy = Column(String(20), nullable=False, default="99.2%")
    status = Column(String(50), nullable=False, default="Đúng giờ")
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    student = relationship("Student", back_populates="attendances")