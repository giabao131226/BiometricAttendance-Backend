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

@router.post("/create")
async def create_subject(request: Request,db: Session = Depends(get_db)):
    return await subject_controller.create_subject(request,db)

@router.patch("/delete/{subject_id}")
def delete_major(subject_id: int,db: Session = Depends(get_db)):
    return subject_controller.delete_subject(subject_id,db)

@router.get("/detail/{subject_id}")
def detail_subject(subject_id:int,db:Session = Depends(get_db)):
    return subject_controller.detail_subject(subject_id,db)

@router.patch("/edit/{subject_id}")
async def edit_subject(subject_id: int,request: Request,db: Session = Depends(get_db)):
    return await subject_controller.edit_subject(subject_id,request,db)
