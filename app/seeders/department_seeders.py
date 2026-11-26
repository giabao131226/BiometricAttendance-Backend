from app.database.database import SessionLocal
from sqlalchemy import text
from sqlalchemy.orm import Session

def seed_department(db: Session):
    db = SessionLocal()
    try:
        sql = text("""
            INSERT INTO departments (
    department_code,
    department_name,
    description,
    faculty_id,
    head_of_department,
    email,
    phone,
    status,
    deleted
)
VALUES
('BM001', 'Công nghệ phần mềm', 'Bộ môn phụ trách đào tạo và nghiên cứu công nghệ phần mềm', 1, 'Nguyễn Văn An', 'cntpm@university.edu.vn', '0912345001', 'active', FALSE),
('BM002', 'Hệ thống thông tin', 'Bộ môn phụ trách hệ thống thông tin và quản trị dữ liệu', 1, 'Trần Văn Bình', 'httt@university.edu.vn', '0912345002', 'active', FALSE),
('BM003', 'Khoa học máy tính', 'Bộ môn nghiên cứu trí tuệ nhân tạo và khoa học dữ liệu', 1, 'Lê Minh Cường', 'khmt@university.edu.vn', '0912345003', 'active', FALSE),
('BM004', 'Mạng máy tính', 'Bộ môn phụ trách mạng máy tính và an toàn thông tin', 1, 'Phạm Quốc Dũng', 'mmt@university.edu.vn', '0912345004', 'active', FALSE),
('BM005', 'Kỹ thuật xây dựng', 'Bộ môn phụ trách kỹ thuật và công nghệ xây dựng', 2, 'Hoàng Văn Đức', 'ktxd@university.edu.vn', '0912345005', 'active', FALSE),
('BM006', 'Công trình thủy', 'Bộ môn phụ trách thiết kế và xây dựng công trình thủy', 2, 'Đỗ Văn Hải', 'ctt@university.edu.vn', '0912345006', 'active', FALSE),
('BM007', 'Kinh tế xây dựng', 'Bộ môn phụ trách kinh tế và quản lý xây dựng', 3, 'Nguyễn Thị Lan', 'ktxd2@university.edu.vn', '0912345007', 'active', FALSE),
('BM008', 'Kế toán', 'Bộ môn phụ trách đào tạo chuyên ngành kế toán', 3, 'Trần Thị Mai', 'ketoan@university.edu.vn', '0912345008', 'active', FALSE),
('BM009', 'Kỹ thuật môi trường', 'Bộ môn phụ trách công nghệ và quản lý môi trường', 4, 'Phạm Văn Nam', 'ktmt@university.edu.vn', '0912345009', 'active', FALSE),
('BM010', 'Cơ khí', 'Bộ môn phụ trách thiết kế và chế tạo cơ khí', 5, 'Lê Văn Thành', 'cokhi@university.edu.vn', '0912345010', 'active', FALSE);
        """)
        db.execute(sql)
        db.commit()

    except Exception as e: 
        db.rollback()
        print(f"Seeder error: {e}")
        
    finally:
        db.close()
