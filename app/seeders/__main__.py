from app.database.database import SessionLocal
from app.seeders.faculty_seeder import seed_faculties
from app.seeders.major_seeder import seed_majors

def run():
    db = SessionLocal()

    try:
        seed_faculties(db)
        seed_majors(db)
    except Exception as e:
        db.rollback()
        print(f"Lỗi khi seed dữ liệu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run()