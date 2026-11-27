from fastapi import HTTPException,Request
from app.database.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.subject import Subject
from sqlalchemy import and_,or_,collate
from datetime import datetime
import math

from app.models.subject import Subject 
from app.models.faculty import Faculty
from app.models.department import Department

def get_all_subjects(request: Request, db: Session):
    try:
        page = int(request.query_params.get("page") or 1)
        status = request.query_params.get("status")
        keyword = request.query_params.get("keyword", "").strip()
        department_id = request.query_params.get("department_id").strip()

        if page < 1:
            page = 1

        pagination = {
            "limitItem": 10,
        }

        query = db.query(Department.department_name,Subject).join(
            Department,
            Department.id == Subject.department_id
        ).filter(
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

        if department_id is not None and department_id != "" and department_id != "all":
            query = query.filter(
                Subject.department_id == department_id
            )

        if keyword is not None:
            search = f"%{keyword}%"

            query = query.filter(
                or_(
                    collate(Subject.subject_code, "utf8mb4_0900_ai_ci").like(search),
                    collate(Subject.subject_name, "utf8mb4_0900_ai_ci").like(search)
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
        data = []
        for department_name,subject_data in subjects:
            data.append({
                "id": subject_data.id,
                "subject_name": subject_data.subject_name,
                "subject_code": subject_data.subject_code,
                "description": subject_data.description,
                "department_id": subject_data.department_id,
                "credit": subject_data.credit,
                "theory_hours": subject_data.theory_hours,
                "practice_hours": subject_data.practice_hours,
                "status": subject_data.status,
                "created_at": subject_data.created_at,
                "updated_at": subject_data.updated_at,
                "deleted": subject_data.deleted,
                "deleted_at": subject_data.deleted_at,
                "department_name": department_name
            })

        return page, totalPage, data,{
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


async def create_subject(request: Request, db: Session):
    try:
        data = await request.json()

        fc = data["subject_code"].strip()
        fn = data["subject_name"].strip()
        department_id = int(data["department_id"])

        if not fc or not fn:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã môn học và tên môn học không được để trống."
                }
            )

        check = db.query(Subject).filter(
            and_(
                Subject.deleted == False,
                or_(
                    Subject.subject_code == fc,
                    Subject.subject_name == fn
                )
            )
        ).first()

        if check is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Môn học đã tồn tại!",
                    "message": "Mã môn học hoặc tên môn học đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                }
            )

        detailDepartment = db.query(Department).filter(
            Department.id == department_id,
            Department.deleted == False
        ).first()

        if detailDepartment is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Không tìm thấy bộ môn!",
                    "message": "Không tìm thấy bộ môn hoặc bộ môn đã bị xóa."
                }
            )

        subject = Subject(
            subject_code=fc,
            subject_name=fn,
            description=data.get("description"),
            department_id=department_id,
            credit=int(data["credit"]),
            theory_hours=int(data.get("theory_hours", 0)),
            practice_hours=int(data.get("practice_hours", 0)),
            status=data.get("status", "active")
        )

        db.add(subject)
        db.commit()
        db.refresh(subject)

        return {
            "success": True,
            "title": "Tạo môn học thành công!",
            "message": "Môn học mới đã được thêm vào hệ thống."
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        print(repr(e))
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể tạo môn học. Vui lòng thử lại sau."
            }
        )


def delete_subject(subject_id: int,db: Session):
    try:
        id = subject_id;

        detailSubject = db.query(Subject).filter(
            Subject.id == id,
            Subject.deleted == False
        ).first()

        if(detailSubject is None):
            raise HTTPException(
                status_code=404,
                detail= "Không tìm thấy Môn Học có mã là: "+ str(id)
            )

        detailSubject.deleted = True;
        detailSubject.deleted_at = datetime.now();

        db.commit();
        db.refresh(detailSubject);

        return {
            "success": True,
            "title": "Xoá Môn Học thành công",
            "message": "Môn Học đã được chuyển vào danh sách đã xóa. Bạn có thể khôi phục ngành này bất cứ lúc nào nếu cần."
        }
    except HTTPException:
            raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể xoá Môn Học. Vui lòng thử lại sau."
            }
        )

def detail_subject(subject_id:int,db:Session):
    try:
        detailSubject = db.query(Subject).filter(
            Subject.id == subject_id,
            Subject.deleted == False
        ).first()

        if(detailSubject is None):
            raise HTTPException(
                status_code=404,
                detail= "Không tìm thấy Môn Học có mã là: "+ str(subject_id)
            )

        return {
            "success": True,
            "detail": detailSubject
        }
    except HTTPException:
        raise
    except:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể lấy thông tin Môn Học. Vui lòng thử lại sau."
            }
        )


async def edit_subject(id: int, request: Request, db: Session):
    try:
        data = await request.json()

        subject_code = (data.get("subject_code") or "").strip()
        subject_name = (data.get("subject_name") or "").strip()
        description = (data.get("description") or "").strip()
        status = data.get("status", "active")
        department_id = data.get("department_id")
        credit = data.get("credit")
        theory_hours = data.get("theory_hours")
        practice_hours = data.get("practice_hours")

        if not subject_code or not subject_name:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã môn học và tên môn học không được để trống."
                }
            )

        if len(subject_code) > 20 or len(subject_name) > 150:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã môn học tối đa 20 ký tự và tên môn học tối đa 150 ký tự."
                }
            )

        if any(char.isspace() for char in subject_code):
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Mã môn học không hợp lệ!",
                    "message": "Mã môn học không được chứa khoảng trắng."
                }
            )

        if status not in ["active", "inactive"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Trạng thái không hợp lệ!",
                    "message": "Trạng thái chỉ được là active hoặc inactive."
                }
            )

        try:
            department_id = int(department_id)
            credit = int(credit)
            theory_hours = int(theory_hours)
            practice_hours = int(practice_hours)

            if credit <= 0:
                raise ValueError()

            if theory_hours < 0 or practice_hours < 0:
                raise ValueError()

        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Số tín chỉ phải lớn hơn 0, số tiết lý thuyết và thực hành phải là số nguyên không âm."
                }
            )

        subject = db.query(Subject).filter(
            Subject.id == id,
            Subject.deleted == False
        ).first()

        if subject is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Môn học không tồn tại!",
                    "message": f"Không tồn tại môn học có mã ID là {id}. Vui lòng kiểm tra lại."
                }
            )

        department = db.query(Department).filter(
            Department.id == department_id,
            Department.deleted == False
        ).first()

        if department is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Bộ môn không tồn tại!",
                    "message": f"Không tồn tại bộ môn có mã ID là {department_id}. Vui lòng kiểm tra lại."
                }
            )

        check = db.query(Subject).filter(
            and_(
                Subject.deleted == False,
                Subject.id != id,
                or_(
                    Subject.subject_code == subject_code,
                    Subject.subject_name == subject_name
                )
            )
        ).first()

        if check is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Môn học đã tồn tại!",
                    "message": "Mã môn học hoặc tên môn học đã được sử dụng. Vui lòng kiểm tra lại."
                }
            )

        subject.subject_code = subject_code
        subject.subject_name = subject_name
        subject.description = description
        subject.department_id = department_id
        subject.credit = credit
        subject.theory_hours = theory_hours
        subject.practice_hours = practice_hours
        subject.status = status

        db.commit()
        db.refresh(subject)

        return {
            "success": True,
            "title": "Cập nhật môn học thành công!",
            "message": "Thông tin môn học đã được cập nhật thành công."
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        print("LỖI UPDATE SUBJECT:", repr(e))
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể cập nhật thông tin môn học. Vui lòng thử lại sau."
            }
        )
