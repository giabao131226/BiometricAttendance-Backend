from pydantic import BaseModel, ConfigDict

class FacultyBase(BaseModel):
    faculty_name: str

class FacultyCreate(FacultyBase):
    faculty_id: str

class FacultyUpdate(FacultyBase):
    pass

class FacultyOut(FacultyCreate):
    model_config = ConfigDict(from_attributes=True)