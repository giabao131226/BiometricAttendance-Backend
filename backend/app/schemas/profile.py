from datetime import date
from pydantic import BaseModel


class ProfileOut(BaseModel):
    role: str
    user_id: str
    name: str
    phone: str | None = None
    email: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    status: str | None = None

    # Dùng chung cho sinh viên và giảng viên
    faculty_id: str | None = None
    faculty_name: str | None = None

    # Chỉ sinh viên
    class_id: str | None = None
    class_name: str | None = None
    cohort_name: str | None = None
    major_id: str | None = None
    major_name: str | None = None
    face_count: int | None = None          # chỉ trả số lượng, không trả dữ liệu sinh trắc học
    fingerprint_count: int | None = None

    # Chỉ giảng viên
    degree: str | None = None