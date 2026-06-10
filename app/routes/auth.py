from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from app.services.auth_service import (
    register_user,
    login_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):

    try:
        return register_user(
            db,
            user_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):

    try:
        return login_user(
            db,
            user_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
