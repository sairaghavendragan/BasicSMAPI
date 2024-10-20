from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .config import settings


oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

Secret_key = settings.secret_key

algorithm = settings.algorithm
expiretimein_minutes = 30


def encode(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiretimein_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Secret_key, algorithm=algorithm)

    return encoded_jwt


def verifyaccess(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, Secret_key, algorithms=[algorithm])
        id = payload.get("id")
        return id

    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"could not validate",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verifyaccess(token, credentials_exception)
