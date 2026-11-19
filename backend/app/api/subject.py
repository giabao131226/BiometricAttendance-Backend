from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud import subject as crud
from app.deps import get_db
from app.schemas.subject import SubjectCreate, SubjectOut, SubjectPatch

router = APIRouter(prefix="/subject", tags=["Subject"])


@router.get("/", response_model=list[SubjectOut])
def list_subject(db: Session = Depends(get_db)):
    return crud.get_all(db)


@router.get("/{subject_id}", response_model=SubjectOut)
def get_subject(subject_id: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, subject_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy môn")
    return obj


@router.post("/", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    if crud.get_by_id(db, data.subject_id):
        raise HTTPException(status_code=400, detail="Mã môn đã tồn tại")
    try:
        return crud.create(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Không thể tạo môn học")


@router.patch("/{subject_id}", response_model=SubjectOut)
def patch_subject(subject_id: str, data: SubjectPatch, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, subject_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy môn")

    fields = data.model_dump(exclude_unset=True)
    if "subject_name" in fields and fields["subject_name"] is None:
        raise HTTPException(status_code=400, detail="Tên môn không được để trống")

    return crud.patch(db, obj, data)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, subject_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Không tìm thấy môn")
    try:
        crud.delete(db, obj)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Không thể xóa: môn đang được sử dụng")
    return Response(status_code=status.HTTP_204_NO_CONTENT)