from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.university import major_controller

router = APIRouter(prefix="/major")

@router.get("")
def list_majors(request: Request,db:Session = Depends(get_db)):
    return major_controller.get_all_major(request,db);

