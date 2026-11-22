from fastapi import APIRouter
from app.routers.university.faculty_route import router as faculty_router
from app.routers.university.major_route import router as major_router
router = APIRouter(prefix="/university")

router.include_router(faculty_router)
router.include_router(major_router)