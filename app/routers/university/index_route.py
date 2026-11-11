from fastapi import APIRouter
from app.routers.university.faculty_route import router as faculty_router
router = APIRouter(prefix="/university")

router.include_router(faculty_router)