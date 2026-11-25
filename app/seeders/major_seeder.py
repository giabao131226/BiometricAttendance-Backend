
from app.models.major import Major
from app.models.faculty import Faculty
from sqlalchemy.orm import Session

def seed_majors(db: Session):
    faculties = db.query(Faculty).filter(
        Faculty.deleted == False
    ).order_by(Faculty.id.asc()).all()

    if not faculties:
        print("Chưa có dữ liệu khoa. Vui lòng seed Faculty trước.")
        return

    major_data = [
        {
            "major_code": "7480201",
            "major_name": "Công nghệ thông tin",
            "description": "Đào tạo kiến thức về phát triển phần mềm, hệ thống thông tin và công nghệ máy tính.",
            "degree_level": "Đại học",
            "duration": 4
        },
        {
            "major_code": "7480101",
            "major_name": "Khoa học máy tính",
            "description": "Nghiên cứu thuật toán, trí tuệ nhân tạo, khoa học dữ liệu và hệ thống máy tính.",
            "degree_level": "Đại học",
            "duration": 4
        },
        {
            "major_code": "7480103",
            "major_name": "Kỹ thuật phần mềm",
            "description": "Đào tạo quy trình phân tích, thiết kế, phát triển và kiểm thử phần mềm.",
            "degree_level": "Đại học",
            "duration": 4
        },
        {
            "major_code": "7480102",
            "major_name": "Mạng máy tính và truyền thông dữ liệu",
            "description": "Đào tạo về mạng máy tính, quản trị hệ thống và an toàn thông tin.",
            "degree_level": "Đại học",
            "duration": 4
        },
        {
            "major_code": "7520103",
            "major_name": "Kỹ thuật cơ khí",
            "description": "Đào tạo thiết kế, chế tạo và vận hành các hệ thống cơ khí.",
            "degree_level": "Đại học",
            "duration": 4
        },
        {
            "major_code": "7580201",
            "major_name": "Kỹ thuật xây dựng",
            "description": "Đào tạo kiến thức thiết kế, thi công và quản lý công trình xây dựng.",
            "degree_level": "Đại học",
            "duration": 4
        },
        {
            "major_code": "7340101",
            "major_name": "Quản trị kinh doanh",
            "description": "Đào tạo kiến thức quản trị, điều hành và phát triển hoạt động kinh doanh.",
            "degree_level": "Đại học",
            "duration": 4
        },
        {
            "major_code": "7340301",
            "major_name": "Kế toán",
            "description": "Đào tạo kiến thức kế toán, kiểm toán và quản lý tài chính doanh nghiệp.",
            "degree_level": "Đại học",
            "duration": 4
        }
    ]

    try:
        for index, item in enumerate(major_data):
            exists = db.query(Major).filter(
                Major.major_code == item["major_code"]
            ).first()

            if exists:
                continue

            faculty = faculties[index % len(faculties)]

            major = Major(
                **item,
                faculty_id=faculty.id,
                status="active",
                deleted=False
            )

            db.add(major)

        db.commit()
        print("Seed dữ liệu ngành học thành công!")

    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed ngành học: {e}")
