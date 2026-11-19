from sqlalchemy.orm import Session
from app.models.major import Major
from app.schemas.major import MajorCreate, MajorPatch

def get_all(db: Session):
    return db.query(Major).all()

def get_by_id(db: Session, major_id: str):
    return db.get(Major, major_id)

def create(db: Session, data: MajorCreate):
    obj = Major(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

"""
def update(db: Session, obj: Major, data: MajorUpdate):
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj
"""

def patch(db: Session, obj: Major, data: MajorPatch):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj: Major):
    db.delete(obj)
    db.commit()