from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.crud import subject as crud
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectOut

from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/subject", tags=["Subject"])

@router.get("/", response_model=list[SubjectOut])
def list_subject(db: Session = Depends(get_db)):
    return crud.get_all(db)

@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, subject_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy môn")
    return obj

@router.post("/", response_model=SubjectOut, status_code=201)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    if not crud_subject.get_by_id(db, data.subject_id):
        raise HTTPException(400, "Mã môn không tồn tại")
    if crud.get_by_id(db, data.subject_id):
        raise HTTPException(400, "Mã môn đã tồn tại")
    return crud.create(db, data)


@router.put("/{subject_id}", response_model=SubjectOut)
def update_subject(subject_id: str, data: SubjectUpdate, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, subject_id)                    # 1. môn có tồn tại không?
    if not obj:
        raise HTTPException(404, "Không tìm thấy môn")
    return crud.update(db, obj, data)                     # 3. mới sửa



@router.delete("/{subject_id}", status_code=204)
def delete_subject(subject: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, subject_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy môn")
    try:
        crud.delete(db, obj)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Không thể xóa: môn đang được sử dụng")