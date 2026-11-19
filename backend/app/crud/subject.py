from sqlalchemy.orm import Session
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectPatch

def get_all(db: Session):
    return db.query(Subject).all()

def get_by_id(db: Session, subject_id: str):
    return db.get(Subject, subject_id)

def create(db: Session, data: SubjectCreate):
    obj = Subject(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

"""
def update(db: Session, obj: Subject, data:SubjectUpdate):
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj
"""

def patch(db: Session, obj: Subject, data: SubjectPatch):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj: Subject):
    db.delete(obj)
    db.commit()