from fastapi import APIRouter
from app.routers.university.faculty_route import router as faculty_router
from app.routers.university.major_route import router as major_router
from app.routers.university.department_route import router as department_router
from app.routers.university.subject_route import router as subject_router
router = APIRouter(prefix="/university")

router.include_router(faculty_router)
router.include_router(major_router)
router.include_router(department_router)
router.include_router(subject_router)