from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Student(Base):
    __tablename__ = "student"

    student_id: Mapped[str] = mapped_column(String(20), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default=None)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default=None)
    account_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("account.account_id"),
        unique=True,
        nullable=False,
    )
    admin_class_id: Mapped[Optional[str]] = mapped_column(
        String(20),
        ForeignKey("administrative_class.class_id"),
        nullable=True,
        default=None,
    )
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True, default=None)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default=None)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")