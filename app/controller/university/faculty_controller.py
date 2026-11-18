from fastapi import HTTPException
from app.database.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.faculty import Faculty

def get_all_faculties(db:Session):
    return db.query(Faculty).all();

