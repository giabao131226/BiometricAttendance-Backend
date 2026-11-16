from fastapi import HTTPException,Request
from app.database.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.faculty import Faculty
from sqlalchemy import and_,or_
from datetime import datetime


def get_all_faculties(db:Session):
    try:
        pagination = {
            "limitItem": 10
        }

        return db.query(Faculty).filter(
            Faculty.deleted == False
        ).all();
    except Exception as e:
        raise HTTPException(
                status_code=400,
                detail={
                    "title": "Có lỗi xảy ra!",
                    "message": "Không thể lấy dữ liệu Khoa"
                }
            )
async def create_faculty(request: Request,db: Session):
    try:
        data = await request.json()
        fc = data["faculty_code"]
        fn = data["faculty_name"]

        if not fc or not fn:
            raise HTTPException(
                status_code=400,
                detail={
                    "title": "Dữ liệu không hợp lệ!",
                    "message": "Mã khoa và tên khoa không được để trống."
                }
            )
    
        check = db.query(Faculty).filter(
            and_(
                Faculty.deleted == False,
                or_(
                    Faculty.faculty_code == fc,
                    Faculty.faculty_name == fn
                )   
            ) 
        ).first()

        if check is not None:
            raise HTTPException(
                status_code=409,
                detail={
                    "title": "Khoa đã tồn tại!",
                    "message": "Mã khoa hoặc tên khoa đã được sử dụng trong hệ thống. Vui lòng kiểm tra lại."
                }
            )
    
        faculty = Faculty(**data)
        db.add(faculty); #Đưa đối tượng vào Session để chờ ghi xuống database
        db.commit() #Xác nhận transaction và ghi dữ liệu xuống database
        db.refresh(faculty)
        return {
            "success": True,
            "title": "Tạo khoa thành công!",
            "message": "Khoa mới đã được thêm vào hệ thống. Bạn có thể tiếp tục quản lý thông tin khoa tại danh sách khoa."
        }
    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể tạo khoa. Vui lòng thử lại sau."
            }
        )

async def delete_faculty(faculty_id: int,db: Session):
    try:
        id = faculty_id;

        detailFaculty = db.query(Faculty).filter(
            Faculty.id == id,
            Faculty.deleted == False
        ).first()

        if(detailFaculty is None):
            raise HTTPException(
                status_code=404,
                detail= "Không tìm thấy khoa có mã là: "+ str(id)
            )

        detailFaculty.deleted = True;
        detailFaculty.deleted_at = datetime.now();

        db.commit();
        db.refresh(detailFaculty);

        return {
            "success": True,
            "title": "Xoá khoa thành công",
            "message": "Khoa đã được chuyển vào danh sách đã xóa. Bạn có thể khôi phục khoa này bất cứ lúc nào nếu cần."
        }
    except HTTPException:
            raise
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "title": "Có lỗi xảy ra!",
                "message": "Không thể xoá khoa. Vui lòng thử lại sau."
            }
        )
        
    

