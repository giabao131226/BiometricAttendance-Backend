from pydantic import BaseModel, ConfigDict

class SubjectBase(BaseModel):
    subject_name: str
    subject_id: str
    credits: int | None

class SubjectCreate(SubjectBase):
    major_id: str

class SubjectUpdate(SubjectBase):
    pass

class SubjectOut(SubjectCreate):
    model_config = ConfigDict(from_attributes=True)