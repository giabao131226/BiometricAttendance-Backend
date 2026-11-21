import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
import app.models  # noqa: F401
from app.models import Student

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BioAttend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))


@app.get("/")
def health_check():
    return {"status": "ok", "message": "BioAttend backend is running"}


@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    code = payload.username.strip()
    student = db.query(Student).filter(Student.student_code == code).first()

    if not student:
        raise HTTPException(status_code=401, detail="Mã sinh viên không tồn tại trong hệ thống.")

    # Lần đầu đăng nhập nếu chưa có mật khẩu trong DB thì tự gán mật khẩu mặc định "123456"
    if not student.password_hash:
        student.password_hash = hash_password("123456")
        db.commit()
        db.refresh(student)

    if not verify_password(payload.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Mật khẩu không chính xác.")

    return {
        "message": "Đăng nhập thành công",
        "user": {
            "id": student.id,
            "fullName": student.full_name,
            "studentId": student.student_code,
            "role": "student",
            "classCode": student.class_code or "66CNTT2",
        },
    }