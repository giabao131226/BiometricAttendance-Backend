from fastapi import HTTPException,Request
from app.database.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.subject import Subject
from sqlalchemy import and_,or_,collate
from datetime import datetime
import math

from app.models.subject import Subject 
def get_all_subjects(request: Request, db: Session):
    try:
        page = int(request.query_params.get("page") or 1)
        status = request.query_params.get("status")
        keyword = request.query_params.get("keyword", "").strip()

        if page < 1:
            page = 1

        pagination = {
            "limitItem": 10,
        }

        query = db.query(Subject).filter(
            Subject.deleted == False
        )
        cntRows = query.count()
        cntActive = query.filter(
            Subject.status == "active",
        ).count()
        cntInActive = query.filter(
            Subject.status == "inactive",
        ).count()

        if status is not None and status != "all" and status != "":
            query = query.filter(
                Subject.status == status
            )

        if keyword is not None:
            search = f"%{keyword}%"

            query = query.filter(
                or_(
                    collate(Subject.Subject_code, "utf8mb4_0900_ai_ci").like(search),
                    collate(Subject.Subject_name, "utf8mb4_0900_ai_ci").like(search)
                )
            )

        totalPage = math.ceil(cntRows / pagination["limitItem"])

        subjects = query.order_by(
            Subject.id.asc()
        ).offset(
            (page - 1) * pagination["limitItem"]
        ).limit(
            pagination["limitItem"]
        ).all()

        return page, totalPage, subjects,{
            "total": cntRows,
            "cntActive": cntActive,
            "cntInActive": cntInActive
        }

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=400,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể lấy dữ liệu Môn Học"
            }
        )
