from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.database import engine, Base, get_db
from app.routers.university.index_route import router as UniversityRouter

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(UniversityRouter,prefix="/api/v1")
