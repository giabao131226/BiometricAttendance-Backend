from app.database.database import SessionLocal
from app.seeders.faculty_seeder import seed_faculties
from app.seeders.major_seeder import seed_majors
from app.seeders.department_seeders import seed_department
from app.seeders.subject_seeder import seed_subjects

def run():
    db = SessionLocal()

    try:
        seed_faculties(db)
        seed_majors(db)
        seed_department(db)
        seed_subjects(db)
    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed dữ liệu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run()