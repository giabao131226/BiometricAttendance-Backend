from fastapi import FastAPI
from app.api import faculty, major, subject
app = FastAPI(title="Hệ thống điểm danh sinh trắc học")

app.include_router(faculty.router)
app.include_router(major.router)
app.include_router(subject.router)