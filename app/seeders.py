from app.database import Base, SessionLocal, engine
import app.models  # noqa: F401
from app.models import Faculty, Student


def seed_faculties(db):
    sample_faculties = [
        {"code": "CNTT", "name": "Công nghệ thông tin"},
        {"code": "CK", "name": "Cơ khí"},
        {"code": "XD", "name": "Công trình"},
        {"code": "KT", "name": "Kinh tế"},
        {"code": "DT", "name": "Điện - Điện tử"},
        {"code": "HH", "name": "Hóa và Môi trường"},
        {"code": "TL", "name": "Thủy lợi"},
        {"code": "NN", "name": "Nông nghiệp"},
        {"code": "QTKD", "name": "Quản trị kinh doanh"},
        {"code": "NNH", "name": "Ngoại ngữ"},
    ]
    for item in sample_faculties:
        exists = db.query(Faculty).filter(Faculty.code == item["code"]).first()
        if not exists:
            db.add(Faculty(**item))
    db.commit()
    print("Seed faculties successfully!")


def seed_students(db):
    cntt = db.query(Faculty).filter(Faculty.code == "CNTT").first()
    sample_students = [
        {
            "student_code": "SV001",
            "full_name": "Nguyễn Văn An",
            "biometric_ref": "face_emb_001",
            "faculty_id": cntt.id if cntt else None,
        },
        {
            "student_code": "SV002",
            "full_name": "Trần Thị Bình",
            "biometric_ref": "fp_tpl_002",
            "faculty_id": cntt.id if cntt else None,
        },
    ]
    for item in sample_students:
        exists = db.query(Student).filter(Student.student_code == item["student_code"]).first()
        if not exists:
            db.add(Student(**item))
    db.commit()
    print("Seed students successfully!")


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_faculties(db)
        seed_students(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()