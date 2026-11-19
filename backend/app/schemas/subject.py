from pydantic import BaseModel, ConfigDict

class SubjectBase(BaseModel):
    subject_name: str
    subject_id: str
    credits: int | None

class SubjectCreate(SubjectBase):
    pass

"""
class SubjectUpdate(SubjectBase):
    pass
"""

class SubjectPatch(BaseModel):
    subject_name: str | None = None
    subject_id: str | None = None
    credits: int | None = None

class SubjectOut(SubjectCreate):
    model_config = ConfigDict(from_attributes=True)