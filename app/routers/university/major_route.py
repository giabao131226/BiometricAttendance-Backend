from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.university import major_controller

router = APIRouter(prefix="/major")

@router.get("")
def list_majors(request: Request,db:Session = Depends(get_db)):
    return major_controller.get_all_major(request,db)

@router.post("/create")
async def create_major(request: Request,db: Session = Depends(get_db)):
    return await major_controller.create_major(request,db)

@router.patch("/delete/{major_id}")
def delete_major(major_id: int,db: Session = Depends(get_db)):
    return major_controller.delete_major(major_id,db)

@router.get("/detail/{major_id}")
def detail_faculty(major_id:int,db:Session = Depends(get_db)):
    return major_controller.detail_major(major_id,db)

@router.patch("/edit/{major_id}")
async def edit_faculty(major_id: int,request: Request,db: Session = Depends(get_db)):
    return await major_controller.edit_major(major_id,request,db);
