from fastapi import HTTPException,Request
from app.database.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.major import Major
from app.models.faculty import Faculty
from sqlalchemy import and_,or_,collate
from datetime import datetime
import math

def get_all_major(request: Request,db:Session):
    try:
        page = int(request.query_params.get("page") or 1)
        status = request.query_params.get("status")
        keyword = request.query_params.get("keyword", "").strip()
        faculty_filter = request.query_params.get("faculty_id","")

        if page < 1:
            page = 1

        pagination = {
            "limitItem": 10,
        }

        query = db.query(Major,Faculty.faculty_name
        ).join(Faculty,Major.faculty_id == Faculty.id
        ).filter(
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
        print(faculty_filter,"abcabc")
        if faculty_filter is not None and faculty_filter != "" and faculty_filter != "all":
            query = query.filter(
                Major.faculty_id == int(faculty_filter)
            )

        if keyword is not None:
            search = f"%{keyword}%"

            query = query.filter(
                or_(
                    collate(Major.major_code, "utf8mb4_0900_ai_ci").like(search),
                    collate(Major.major_name, "utf8mb4_0900_ai_ci").like(search),
                    collate(Faculty.faculty_name,"utf8mb4_0900_ai_ci").like(search)
                )
            )

        totalPage = math.ceil(cntRows / pagination["limitItem"])

        majors = query.order_by(
            Major.id.asc()
        ).offset(
            (page - 1) * pagination["limitItem"]
        ).limit(
            pagination["limitItem"]
        ).all()

        result = []

        for major, faculty_name in majors:
            result.append({
                "id": major.id,
                "major_code": major.major_code,
                "major_name": major.major_name,
                "faculty_id": major.faculty_id,
                "faculty_name": faculty_name,
                "description": major.description,
                "degree_level": major.degree_level,
                "duration": major.duration,
                "status": major.status,
                "created_at": major.created_at,
                "updated_at": major.updated_at
            })


        return {
            "success": True,
            "currentPage": page,
            "totalPage": totalPage,
            "majors": result,
            "overview": {
                "total": cntRows,
                "cntActive": cntActive,
                "cntInActive": cntInActive
            }
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


async def create_major(request: Request,db: Session):
    try:
        data = await request.json()
        fc = data["major_code"]
        fn = data["major_name"]

        if not fc or not fn:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã ngành và tên ngành không được để trống."
                }
            )
    
        check = db.query(Major).filter(
            and_(
                Major.deleted == False,
                or_(
                    Major.major_code == fc,
                    Major.major_name == fn
                )   
            ) 
        ).first()

        if check is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Ngành đã tồn tại!",
                    "message": "Mã ngành hoặc tên ngành đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                }
            )
    
        major = Major(**data)
        db.add(major); #Đưa đối tượng vào Session để chờ ghi xuống database
        db.commit() #Xác nhận transaction và ghi dữ liệu xuống database
        db.refresh(major)
        return {
            "success": True,
            "title": "Tạo ngành thành công!",
            "message": "Ngành mới đã được thêm vào hệ thống. Bạn có thể tiếp tục quản lý thông tin khoa tại danh sách khoa."
        }
    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể tạo ngành. Vui lòng thử lại sau."
            }
        )

def delete_major(major_id: int,db: Session):
    try:
        id = major_id;

        detailMajor = db.query(Major).filter(
            Major.id == id,
            Major.deleted == False
        ).first()

        if(detailMajor is None):
            raise HTTPException(
                status_code=404,
                detail= "Không tìm thấy ngành có mã là: "+ str(id)
            )

        detailMajor.deleted = True;
        detailMajor.deleted_at = datetime.now();

        db.commit();
        db.refresh(detailMajor);

        return {
            "success": True,
            "title": "Xoá ngành thành công",
            "message": "Ngành đã được chuyển vào danh sách đã xóa. Bạn có thể khôi phục ngành này bất cứ lúc nào nếu cần."
        }
    except HTTPException:
            raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể xoá ngành. Vui lòng thử lại sau."
            }
        )

def detail_major(major_id:int,db:Session):
    try:
        detailMajor = db.query(Major).filter(
            Major.id == major_id,
            Major.deleted == False
        ).first()

        if(detailMajor is None):
            raise HTTPException(
                status_code=404,
                detail= "Không tìm thấy khoa có mã là: "+ str(major_id)
            )

        return {
            "success": True,
            "detail": detailMajor
        }

    except HTTPException:
        raise
    except:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể xoá khoa. Vui lòng thử lại sau."
            }
        )


async def edit_major(id: int, request: Request, db: Session):
    try:
        data = await request.json()

        major_code = data.get("major_code", "").strip()
        major_name = data.get("major_name", "").strip()
        description = (data.get("description") or "").strip()
        status = data.get("status", "active")
        degree_level = data.get("degree_level", "Đại học").strip()
        faculty_id = data.get("faculty_id")
        duration = data.get("duration", 4)

        if not major_code or not major_name:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã ngành và tên ngành không được để trống."
                }
            )

        if len(major_code) > 20 or len(major_name) > 150:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã ngành tối đa 20 ký tự và tên ngành tối đa 150 ký tự."
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

        if not degree_level or len(degree_level) > 50:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Trình độ đào tạo không hợp lệ."
                }
            )

        try:
            faculty_id = int(faculty_id)
            duration = int(duration)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Khoa quản lý và thời gian đào tạo phải có kiểu dữ liệu hợp lệ."
                }
            )

        if duration <= 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Thời gian đào tạo phải là số nguyên dương."
                }
            )

        major = db.query(Major).filter(
            and_(
                Major.id == id,
                Major.deleted == False
            )
        ).first()

        if major is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "title": "Ngành không tồn tại!",
                    "message": f"Không tồn tại ngành có mã ID là {id}. Vui lòng kiểm tra lại."
                }
            )

        check = db.query(Major).filter(
            and_(
                Major.deleted == False,
                Major.id != id,
                or_(
                    Major.major_code == major_code,
                    Major.major_name == major_name
                )
            )
        ).first()

        if check is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Ngành đã tồn tại!",
                    "message": "Mã ngành hoặc tên ngành đã được sử dụng. Vui lòng kiểm tra lại."
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

        major.major_code = major_code
        major.major_name = major_name
        major.description = description
        major.faculty_id = faculty_id
        major.degree_level = degree_level
        major.duration = duration
        major.status = status

        db.commit()
        db.refresh(major)

        return {
            "success": True,
            "title": "Cập nhật ngành thành công!",
            "message": "Thông tin ngành đã được cập nhật thành công."
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        print("LỖI UPDATE MAJOR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể cập nhật thông tin ngành. Vui lòng thử lại sau."
            }
        )
