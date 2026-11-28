from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
#cấu hình
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False)


#lớp cha giúp sau này tạo các model kế thừa Base
#(dùng Python để mô tả cấu trúc các bảng và thao tác với dữ liệu trong Database)
class Base(DeclarativeBase):
    pass