from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.university import faculty_controller

router = APIRouter(prefix="/faculty",tags = ["Faculty"])

@router.get("")
def list_faculties(request: Request,db: Session = Depends(get_db)):
    currentPage,totalPage,faculties,overview = faculty_controller.get_all_faculties(request,db)
    return {
        "success": True,
        "faculties": faculties,
        "currentPage": currentPage,
        "totalPage": totalPage,
        "overview": overview
    }

@router.post("/create")
async def create_faculty(request: Request,db: Session = Depends(get_db)):
    return await faculty_controller.create_faculty(request,db)

@router.patch("/delete/{faculty_id}")
def delete_faculty(faculty_id: int,db: Session = Depends(get_db)):
    return faculty_controller.delete_faculty(faculty_id,db)

@router.get("/detail/{faculty_id}")
def detail_faculty(faculty_id:int,db:Session = Depends(get_db)):
    return faculty_controller.detail_faculty(faculty_id,db)

@router.patch("/edit/{faculty_id}")
async def edit_faculty(faculty_id: int,request: Request,db: Session = Depends(get_db)):
    return await faculty_controller.edit_faculty(faculty_id,request,db);