from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.university import faculty_controller

router = APIRouter(prefix="/faculty",tags = ["Faculty"])

@router.get("/")
def list_faculties(db: Session = Depends(get_db)):
    faculties = faculty_controller.get_all_faculties(db)
    return {"success": True,"faculties": faculties}

@router.post("/create")
async def create_faculty(request: Request,db: Session = Depends(get_db)):
    return await faculty_controller.create_faculty(request,db)

@router.patch("/delete/{faculty_id}")
async def delete_faculty(faculty_id: int,db: Session = Depends(get_db)):
    return await faculty_controller.delete_faculty(faculty_id,db);