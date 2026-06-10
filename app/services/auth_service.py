from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def register_user(
    db: Session,
    user_data: UserRegister,
):

    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db: Session,
    user_data: UserLogin,
):

    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise ValueError("Invalid credentials")

    token = create_access_token(
        {
            "sub": str(user.id),
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
