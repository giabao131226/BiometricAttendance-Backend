git add appfrom sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyCreate, FacultyUpdate

def get_all(db: Session):
    return db.query(Faculty).all()

def get_by_id(db: Session, faculty_id: str):
    return db.get(Faculty, faculty_id)

def create(db: Session, data: FacultyCreate):
    obj = Faculty(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, obj: Faculty, data: FacultyUpdate):
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, obj: Faculty):
    db.delete(obj)
    db.commit()