from pydantic import BaseModel, ConfigDict

class MajorBase(BaseModel):
    faculty_name: str
    faculty_id: str
    duration_years: float | None

class MajorCreate(MajorBase):
    major_id: str

class MajorUpdate(MajorBase):
    pass

class MajorOut(MajorCreate):
    model_config = ConfigDict(from_attributes=True)