from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.auth_middleware import verify_token

from database.database import get_db
from models.user import User

from utils.security import (
    verify_password,
    create_access_token
)

router = APIRouter()

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    valid_password = verify_password(
        form_data.password,
        db_user.password
    )

    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/protected")
def protected_route(
    current_user: str = Depends(verify_token)
):

    return {
        "message": "Protected route accessed",
        "user": current_user
    }