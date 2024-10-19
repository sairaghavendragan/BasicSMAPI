from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import getdb
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.useroutput
)
def createuser(user: schemas.usercreate, db: Session = Depends(getdb)):
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.useroutput)
def getuser(id: int, db: Session = Depends(getdb)):
    query = db.query(models.users).filter(models.users.id == id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
