from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.crud import major as crud
from app.schemas.major import MajorCreate, MajorPatch, MajorOut

from sqlalchemy.exc import IntegrityError
from app.crud import faculty as crud_faculty

router = APIRouter(prefix="/majors", tags=["Major"])

@router.get("/", response_model=list[MajorOut])
def list_majors(db: Session = Depends(get_db)):
    return crud.get_all(db)

@router.get("/{major_id}", response_model=MajorOut)
def get_major(major_id: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, major_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy ngành")
    return obj

@router.post("/", response_model=MajorOut, status_code=201)
def create_major(data: MajorCreate, db: Session = Depends(get_db)):
    # Đã sửa data.major_id thành data.faculty_id để check đúng mã khoa
    if not crud_faculty.get_by_id(db, data.faculty_id):
        raise HTTPException(400, "Mã khoa không tồn tại")
    if crud.get_by_id(db, data.major_id):
        raise HTTPException(400, "Mã ngành đã tồn tại")
    return crud.create(db, data)

"""
@router.put("/{major_id}", response_model=MajorOut)
def update_major(major_id: str, data: MajorUpdate, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, major_id)                    # 1. ngành có tồn tại không?
    if not obj:
        raise HTTPException(404, "Không tìm thấy ngành")
    
    # Kiểm tra khoa mới có tồn tại không (nếu schema MajorUpdate có truyền faculty_id)
    if data.faculty_id and not crud_faculty.get_by_id(db, data.faculty_id):   # 2. khoa mới có tồn tại không?
        raise HTTPException(400, "Mã khoa không tồn tại")
        
    return crud.update(db, obj, data)                     # 3. mới sửa
"""

from app.schemas.major import MajorPatch

@router.patch("/{major_id}", response_model=MajorOut)
def patch_major(major_id: str, data: MajorPatch, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, major_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy ngành")

    fields = data.model_dump(exclude_unset=True)
    if "major_name" in fields and fields["major_name"] is None:
        raise HTTPException(400, "Tên ngành không được để trống")
    if "faculty_id" in fields:
        if fields["faculty_id"] is None or not crud_faculty.get_by_id(db, fields["faculty_id"]):
            raise HTTPException(400, "Mã khoa không tồn tại")

    return crud.patch(db, obj, data)


@router.delete("/{major_id}", status_code=204)
def delete_major(major_id: str, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, major_id)
    if not obj:
        raise HTTPException(404, "Không tìm thấy ngành")
    try:
        crud.delete(db, obj)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Không thể xóa: ngành đang được sử dụng")