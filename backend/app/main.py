from fastapi import FastAPI
from app.api import faculty, major, subject, profile
app = FastAPI(title="Hệ thống điểm danh sinh trắc học")


#connect fe be
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#nơi trỏ các router api cho fe
app.include_router(faculty.router)
app.include_router(major.router)
app.include_router(subject.router)
app.include_router(profile.router)