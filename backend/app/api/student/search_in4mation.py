from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.student import Student
from app.schemas.student import StudentOut

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/{student_id}", response_model=StudentOut)
def get_student_information(student_id: str, db: Session = Depends(get_db)):
    sid = student_id.strip()
    record = db.query(Student).filter(Student.student_id == sid).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy thông tin sinh viên với mã này.",
        )

    return record