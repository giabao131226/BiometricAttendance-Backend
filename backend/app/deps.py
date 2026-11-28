from types import SimpleNamespace

from fastapi import Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_account(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    data = decode_access_token(token) if token else None
    if not data:
        raise HTTPException(401, "Chưa đăng nhập hoặc phiên đã hết hạn")

    row = db.execute(
        text("SELECT account_id, role, status FROM account WHERE account_id = :a"),
        {"a": data["sub"]},
    ).mappings().first()
    if not row or row["status"] != "active":
        raise HTTPException(401, "Tài khoản không hợp lệ")

    return SimpleNamespace(**row)