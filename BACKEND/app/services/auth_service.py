from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.utils.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def register_user(
    db: Session,
    request: RegisterRequest,
) -> User:

    email = request.email.strip().lower()

    existing_user = db.execute(
        select(User).where(
            User.email == email
        )
    ).scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        role_id=1,
        name=request.name.strip(),
        email=email,
        password_hash=hash_password(request.password),
        phone=request.phone,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db: Session,
    request: LoginRequest,
) -> dict:

    email = request.email.strip().lower()

    user = db.execute(
        select(User).where(
            User.email == email
        )
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    if not verify_password(
        request.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user_id=user.user_id,
        role_id=user.role_id,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }