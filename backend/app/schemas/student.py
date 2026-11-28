from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    account_id: str
    admin_class_id: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    status: str = "active"


class StudentCreate(StudentBase):
    student_id: str


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    admin_class_id: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    status: Optional[str] = None


class StudentOut(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    student_id: str