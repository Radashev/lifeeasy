from fastapi import APIRouter, Depends

from app.models.user import User
from app.security.authorization import (
    require_admin,
    require_root,
    require_user,
)

router = APIRouter(
    prefix="/authorization",
    tags=["Authorization"],
)


@router.get("/user")
async def user_endpoint(
    current_user: User = Depends(require_user),
) -> dict:
    return {
        "message": "USER endpoint access granted",
        "email": current_user.email,
        "role": current_user.role,
    }


@router.get("/admin")
async def admin_endpoint(
    current_user: User = Depends(require_admin),
) -> dict:
    return {
        "message": "ADMIN endpoint access granted",
        "email": current_user.email,
        "role": current_user.role,
    }


@router.get("/root")
async def root_endpoint(
    current_user: User = Depends(require_root),
) -> dict:
    return {
        "message": "ROOT endpoint access granted",
        "email": current_user.email,
        "role": current_user.role,
    }
