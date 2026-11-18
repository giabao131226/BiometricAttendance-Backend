from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.crud import faculty as crud
from app.schemas.faculty import FacultyCreate, FacultyUpdate, FacultyOut

router = APIRouter(prefix="/faculties", tags=["Khoa"])

@router.get("/", response_model=list[FacultyOut])
def list_faculties(db: Session = Depends(get_db)):
    return crud.get_all(db)

@router.get("/{faculty_id}", response_model=FacultyOut)
def get_faculty(faculty_id: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, faculty_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy khoa")
    return obj

@router.post("/", response_model=FacultyOut, status_code=201)
def create_faculty(data: FacultyCreate, db: Session = Depends(get_db)):
    if crud.get_by_id(db, data.faculty_id):
        raise HTTPException(400, "Mã khoa đã tồn tại")
    return crud.create(db, data)

@router.put("/{faculty_id}", response_model=FacultyOut)
def update_faculty(faculty_id: str, data: FacultyUpdate, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, faculty_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy khoa")
    return crud.update(db, obj, data)

@router.delete("/{faculty_id}", status_code=204)
def delete_faculty(faculty_id: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, faculty_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy khoa")
    crud.delete(db, obj)