from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.university import faculty_controller

router = APIRouter(prefix="/faculty",tags = ["Faculty"])

@router.get("/")
def list_faculties(db: Session = Depends(get_db)):
    faculties = faculty_controller.get_all_faculties(db);
    return {"success": True,"faculties": faculties}