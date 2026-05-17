from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

SECRET_KEY = "biomedical_secret_key"
ALGORITHM = "HS256"

def verify_token(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return email

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token verification failed"
        )