from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from sqlalchemy import text

def seed_subjects(db: Session):
    db = SessionLocal()
    try:
        sql = text("""INSERT INTO subjects (
    subject_code,
    subject_name,
    description,
    department_id,
    credit,
    theory_hours,
    practice_hours,
    status,
    deleted
)
VALUES
('MH001', 'Lập trình C++', 'Môn học cung cấp kiến thức lập trình cơ bản với ngôn ngữ C++', 1, 3, 30, 15, 'active', FALSE),
('MH002', 'Cấu trúc dữ liệu và giải thuật', 'Nghiên cứu các cấu trúc dữ liệu và thuật toán cơ bản', 1, 3, 30, 15, 'active', FALSE),
('MH003', 'Lập trình hướng đối tượng', 'Cung cấp kiến thức về lập trình hướng đối tượng', 1, 3, 30, 15, 'active', FALSE),
('MH004', 'Cơ sở dữ liệu', 'Giới thiệu mô hình dữ liệu quan hệ và hệ quản trị cơ sở dữ liệu', 2, 3, 30, 15, 'active', FALSE),
('MH005', 'Phân tích thiết kế hệ thống', 'Cung cấp phương pháp phân tích và thiết kế hệ thống thông tin', 2, 3, 30, 15, 'active', FALSE),
('MH006', 'Mạng máy tính', 'Giới thiệu kiến trúc mạng, giao thức và mô hình truyền thông', 4, 3, 30, 15, 'active', FALSE),
('MH007', 'An toàn thông tin', 'Cung cấp kiến thức về bảo mật hệ thống và an toàn dữ liệu', 4, 3, 30, 15, 'active', FALSE),
('MH008', 'Trí tuệ nhân tạo', 'Giới thiệu các thuật toán và ứng dụng trí tuệ nhân tạo', 3, 3, 30, 15, 'active', FALSE),
('MH009', 'Học máy', 'Nghiên cứu các thuật toán học máy và ứng dụng thực tế', 3, 3, 30, 15, 'active', FALSE),
('MH010', 'Khai phá dữ liệu', 'Cung cấp kiến thức về khai phá và phân tích dữ liệu', 3, 3, 30, 15, 'active', FALSE);""")

        db.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"System error: {e}")
    finally:
        db.close()