from fastapi import HTTPException,Request
from app.database.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from app.models.department import Department
from sqlalchemy import and_,or_,collate
from datetime import datetime
import math

def get_all_departments(request: Request, db: Session):
    try:
        page = int(request.query_params.get("page") or 1)
        status = request.query_params.get("status")
        keyword = request.query_params.get("keyword", "").strip()
        faculty_id = request.query_params.get("faculty_id","").strip()

        if page < 1:
            page = 1

        pagination = {
            "limitItem": 10,
        }

        query = db.query(Department).filter(
            Department.deleted == False
        )
        cntRows = query.count()
        cntActive = query.filter(
            Department.status == "active",
        ).count()
        cntInActive = query.filter(
            Department.status == "inactive",
        ).count()

        if status is not None and status != "all" and status != "":
            query = query.filter(
                Department.status == status
            )
        if faculty_id is not None and faculty_id != "all" and faculty_id != "":
            query = query.filter(
                Department.faculty_id == faculty_id
            )

        if keyword is not None:
            search = f"%{keyword}%"

            query = query.filter(
                or_(
                    collate(Department.department_code, "utf8mb4_0900_ai_ci").like(search),
                    collate(Department.department_name, "utf8mb4_0900_ai_ci").like(search)
                )
            )

        totalPage = math.ceil(cntRows / pagination["limitItem"])

        departments = query.order_by(
            Department.id.asc()
        ).offset(
            (page - 1) * pagination["limitItem"]
        ).limit(
            pagination["limitItem"]
        ).all()

        return page, totalPage, departments,{
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
                "message": "Không thể lấy dữ liệu Bộ Môn"
            }
        )

async def create_department(request: Request, db: Session):
    try:
        data = await request.json()
        fc = data["department_code"].strip()
        fn = data["department_name"].strip()
        email = data.get("email")
        phone = data.get("phone")

        if not fc or not fn:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã Bộ Môn và tên Bộ Môn không được để trống."
                }
            )

        check = db.query(Department).filter(
            and_(
                Department.deleted == False,
                or_(
                    Department.department_code == fc,
                    Department.department_name == fn
                )
            )
        ).first()

        if check is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Bộ Môn đã tồn tại!",
                    "message": "Mã Bộ Môn hoặc tên Bộ Môn đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                }
            )

        if email and email.strip():
            checkEmail = db.query(Department).filter(
                and_(
                    Department.deleted == False,
                    Department.email == email.strip()
                )
            ).first()

            if checkEmail is not None:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "title": "Tạo Bộ Môn thất bại!",
                        "message": "Email đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                    }
                )

        if phone and phone.strip():
            checkPhone = db.query(Department).filter(
                and_(
                    Department.deleted == False,
                    Department.phone == phone.strip()
                )
            ).first()

            if checkPhone is not None:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "title": "Tạo Bộ Môn thất bại!",
                        "message": "Số điện thoại đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                    }
                )

        data["department_code"] = fc
        data["department_name"] = fn
        data["email"] = email.strip() if email and email.strip() else None
        data["phone"] = phone.strip() if phone and phone.strip() else None

        department = Department(**data)

        db.add(department)
        db.commit()
        db.refresh(department)

        return {
            "success": True,
            "title": "Tạo Bộ Môn thành công!",
            "message": "Bộ Môn mới đã được thêm vào hệ thống. Bạn có thể tiếp tục quản lý thông tin Bộ Môn tại danh sách bộ môn."
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể tạo Bộ Môn. Vui lòng thử lại sau."
            }
        )

def delete_department(department_id: int,db: Session):
    try:
        id = department_id;

        detailDepartment = db.query(Department).filter(
            Department.id == id,
            Department.deleted == False
        ).first()

        if(detailDepartment is None):
            raise HTTPException(
                status_code=404,
                detail= "Không tìm thấy Bộ Môn có mã là: "+ str(id)
            )

        detailDepartment.deleted = True;
        detailDepartment.deleted_at = datetime.now();

        db.commit();
        db.refresh(detailDepartment);

        return {
            "success": True,
            "title": "Xoá Bộ Môn thành công",
            "message": "Bộ Môn đã được chuyển vào danh sách đã xóa. Bạn có thể khôi phục ngành này bất cứ lúc nào nếu cần."
        }
    except HTTPException:
            raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể xoá Bộ Môn. Vui lòng thử lại sau."
            }
        )

def detail_department(department_id:int,db:Session):
    try:
        detailDepartment = db.query(Department).filter(
            Department.id == department_id,
            Department.deleted == False
        ).first()

        if(detailDepartment is None):
            raise HTTPException(
                status_code=404,
                detail= "Không tìm thấy Bộ Môn có mã là: "+ str(department_id)
            )

        return {
            "success": True,
            "detail": detailDepartment
        }
    except HTTPException:
        raise
    except:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể xoá Bộ Môn. Vui lòng thử lại sau."
            }
        )


async def edit_department(id: int, request: Request, db: Session):
    try:
        data = await request.json()

        department_code = data.get("department_code", "").strip()
        department_name = data.get("department_name", "").strip()
        description = (data.get("description") or "").strip()
        status = data.get("status", "active")
        faculty_id = data.get("faculty_id")
        email = (data.get("email") or "").strip()
        phone = (data.get("phone") or "").strip()
        head_of_department = (data.get("head_of_department") or "").strip()

        if not department_code or not department_name:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã Bộ Môn và tên Bộ Môn không được để trống."
                }
            )

        if len(department_code) > 20 or len(department_name) > 150:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã Bộ Môn tối đa 20 ký tự và tên Bộ Môn tối đa 150 ký tự."
                }
            )

        if len(head_of_department) > 150:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Tên trưởng bộ môn không được vượt quá 150 ký tự."
                }
            )

        if not email:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Email không được để trống."
                }
            )

        if len(email) > 150:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Email không được vượt quá 150 ký tự."
                }
            )

        if not phone:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Số điện thoại không được để trống."
                }
            )

        if len(phone) > 15:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Số điện thoại không được vượt quá 15 ký tự."
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
            faculty_id = int(faculty_id)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Khoa quản lý phải có kiểu dữ liệu hợp lệ."
                }
            )

        department = db.query(Department).filter(
            and_(
                Department.id == id,
                Department.deleted == False
            )
        ).first()

        if department is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Bộ Môn không tồn tại!",
                    "message": f"Không tồn tại Bộ Môn có mã ID là {id}. Vui lòng kiểm tra lại."
                }
            )

        check = db.query(Department).filter(
            and_(
                Department.deleted == False,
                Department.id != id,
                or_(
                    Department.department_code == department_code,
                    Department.department_name == department_name
                )
            )
        ).first()

        if check is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Bộ Môn đã tồn tại!",
                    "message": "Mã Bộ Môn hoặc tên Bộ Môn đã được sử dụng. Vui lòng kiểm tra lại."
                }
            )

        checkEmail = db.query(Department).filter(
            and_(
                Department.deleted == False,
                Department.id != id,
                Department.email == email
            )
        ).first()

        if checkEmail is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Cập nhật Bộ Môn thất bại!",
                    "message": "Email đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                }
            )

        checkPhone = db.query(Department).filter(
            and_(
                Department.deleted == False,
                Department.id != id,
                Department.phone == phone
            )
        ).first()

        if checkPhone is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Cập nhật Bộ Môn thất bại!",
                    "message": "Số điện thoại đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                }
            )

        faculty = db.query(Faculty).filter(
            and_(
                Faculty.id == faculty_id,
                Faculty.deleted == False
            )
        ).first()

        if faculty is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Khoa không tồn tại!",
                    "message": "Khoa được chọn không tồn tại hoặc đã bị xóa."
                }
            )

        department.department_code = department_code
        department.department_name = department_name
        department.description = description
        department.faculty_id = faculty_id
        department.email = email
        department.phone = phone
        department.status = status
        department.head_of_department = head_of_department

        db.commit()
        db.refresh(department)

        return {
            "success": True,
            "title": "Cập nhật Bộ Môn thành công!",
            "message": "Thông tin Bộ Môn đã được cập nhật thành công."
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        print("LỖI UPDATE Department:", repr(e))
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể cập nhật thông tin Bộ Môn. Vui lòng thử lại sau."
            }
        )
