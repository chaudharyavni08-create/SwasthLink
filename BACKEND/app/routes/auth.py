from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from app.services.auth_service import (
    login_user,
    register_user,
)
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register_user(
        db=db,
        request=request,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        request=request,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user