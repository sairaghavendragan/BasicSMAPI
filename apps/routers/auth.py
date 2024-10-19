from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import getdb
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2

router = APIRouter(tags=["auth"])


@router.post("/login")
def login(
    user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getdb)
):
    query = db.query(models.users).filter(models.users.email == user_cred.username)
    user = query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    if not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )

    access_token = oauth2.encode({"id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
