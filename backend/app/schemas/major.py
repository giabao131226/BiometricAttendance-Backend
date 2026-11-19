from pydantic import BaseModel, ConfigDict

class MajorBase(BaseModel):
    major_name: str
    major_id: str
    faculty_id: str
    duration_years: float | None

class MajorCreate(MajorBase):
    pass

"""
class MajorUpdate(MajorBase):
    pass
"""

class MajorPatch(BaseModel):
    major_name: str | None = None
    faculty_id: str | None = None
    duration_years: float | None = None

class MajorOut(MajorCreate):
    model_config = ConfigDict(from_attributes=True)