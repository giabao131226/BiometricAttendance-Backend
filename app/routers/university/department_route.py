from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controller.university import department_controller

router = APIRouter(prefix="/department",tags=["Department"])

@router.get("")
def get_all_deparments(request: Request, db: Session = Depends(get_db)):
    currentPage, totalPage, departments,overview =  department_controller.get_all_departments(request,db)
    return {
        "success": True,
        "currentPage": currentPage,
        "totalPage": totalPage,
        "departments": departments,
        "overview": overview
    }

@router.post("/create")
async def create_department(request: Request,db: Session = Depends(get_db)):
    return await department_controller.create_department(request,db)

@router.patch("/delete/{department_id}")
def delete_department(department_id: int,db: Session = Depends(get_db)):
    return department_controller.delete_department(department_id,db)

@router.get("/detail/{department_id}")
def detail_department(department_id:int,db:Session = Depends(get_db)):
    return department_controller.detail_department(department_id,db)

@router.patch("/edit/{department_id}")
async def edit_department(department_id: int,request: Request,db: Session = Depends(get_db)):
    return await department_controller.edit_department(department_id,request,db);