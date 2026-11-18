from app.database.database import SessionLocal
from sqlalchemy import text

def seed_faculties():
    db = SessionLocal()

    try:
        sql = text("""
            INSERT INTO faculties
            (id, faculty_code, faculty_name, description, status, created_at, updated_at)
            VALUES
            (1, 'CNTT', 'Khoa Công nghệ thông tin', 'Đào tạo ngành CNTT, Khoa học máy tính và Kỹ thuật phần mềm', 1, NOW(), NOW()),
            (2, 'KHMT', 'Khoa Khoa học máy tính', 'Đào tạo Trí tuệ nhân tạo và Xử lý dữ liệu', 1, NOW(), NOW()),
            (3, 'KT', 'Khoa Kinh tế', 'Đào tạo Quản trị kinh doanh, Tài chính ngân hàng và Kế toán', 1, NOW(), NOW()),
            (4, 'ĐT', 'Khoa Điện - Điện tử', 'Đào tạo Kỹ thuật Điện, Tự động hóa và Viễn thông', 1, NOW(), NOW()),
            (5, 'CK', 'Khoa Cơ khí', 'Đào tạo Kỹ thuật cơ khí và Chế tạo máy', 1, NOW(), NOW()),
            (6, 'XD', 'Khoa Xây dựng', 'Đào tạo Kỹ thuật công trình xây dựng và Hạ tầng', 1, NOW(), NOW()),
            (7, 'NN', 'Khoa Ngoại ngữ', 'Đào tạo Ngôn ngữ Anh và Ngôn ngữ Nhật', 1, NOW(), NOW()),
            (8, 'MT', 'Khoa Môi trường', 'Đào tạo Kỹ thuật môi trường và Quản lý tài nguyên', 1, NOW(), NOW()),
            (9, 'LH', 'Khoa Du lịch & Lữ hành', 'Đào tạo Quản trị dịch vụ du lịch và khách sạn', 1, NOW(), NOW()),
            (10, 'Luat', 'Khoa Luật', 'Đào tạo Luật kinh tế và Luật quốc tế', 1, NOW(), NOW())
        """)

        db.execute(sql)
        db.commit()

        print("Seed faculties successfully!")

    except Exception as e:
        db.rollback()
        print(f"Seeder error: {e}")

    finally:
        db.close()