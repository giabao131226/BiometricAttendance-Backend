from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.university import subject_controller

router = APIRouter(prefix="/subjects",tags=["Subject"])

@router.get("")
def get_all_subjects(request: Request,db: Session = Depends(get_db)):
    currentPage, totalPage, subjects,overview = subject_controller.get_all_subjects(request,db)
    return {
        "success": True,
        "currentPage": currentPage,
        "totalPage": totalPage,
        "subjects": subjects,
        "overview": overview
    }