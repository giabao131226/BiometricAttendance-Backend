from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import profile as crud
from app.deps import get_current_account, get_db
from app.schemas.profile import ProfileOut

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me", response_model=ProfileOut, response_model_exclude_none=True)
def get_my_profile(
    account=Depends(get_current_account),
    db: Session = Depends(get_db),
):
    if account.role not in ("student", "lecturer"):
        raise HTTPException(403, "Vai trò này chưa có hồ sơ cá nhân")

    profile = crud.get_profile(db, account.account_id, account.role)
    if not profile:
        raise HTTPException(404, "Không tìm thấy hồ sơ cá nhân")
    return profile