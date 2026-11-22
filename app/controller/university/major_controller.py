from fastapi import HTTPException,Request
from app.database.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.major import Major
from sqlalchemy import and_,or_,collate
from datetime import datetime
import math

def get_all_major(request: Request,db:Session):
    try:
        page = int(request.query_params.get("page") or 1)
        status = request.query_params.get("status")
        keyword = request.query_params.get("keyword", "").strip()

        if page < 1:
            page = 1

        pagination = {
            "limitItem": 10,
        }

        query = db.query(Major).filter(
            Major.deleted == False
        )
        cntRows = query.count()
        cntActive = query.filter(
            Major.status == "active",
        ).count()
        cntInActive = query.filter(
            Major.status == "inactive",
        ).count()

        if status is not None and status != "all" and status != "":
            query = query.filter(
                Major.status == status
            )

        if keyword is not None:
            search = f"%{keyword}%"

            query = query.filter(
                or_(
                    collate(Major.major_code, "utf8mb4_0900_ai_ci").like(search),
                    collate(Major.major_name, "utf8mb4_0900_ai_ci").like(search)
                )
            )

        totalPage = math.ceil(cntRows / pagination["limitItem"])

        faculties = query.order_by(
            Major.id.asc()
        ).offset(
            (page - 1) * pagination["limitItem"]
        ).limit(
            pagination["limitItem"]
        ).all()

        return page, totalPage, faculties,{
            "total": cntRows,
            "cntActive": cntActive,
            "cntInActive": cntInActive
        }
        
           
    except HTTPException:
        raise
    except Exception as e:
        print(str(e));
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Có lỗi xảy ra",
                "message": "Không thể lấy dữ liệu Ngành"
            }
        )