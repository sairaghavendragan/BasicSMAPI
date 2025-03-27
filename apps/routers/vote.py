from fastapi import FastAPI, HTTPException,   status, Depends, APIRouter
from fastapi.responses import Response
from ..database import getdb
from sqlalchemy.orm import Session
from typing import List,Optional
from sqlalchemy import func,select

from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/vote", tags=["votes"])


def get_post_score(db: Session, post_id: int) -> int:
    score_result = db.execute(
        select(func.sum(models.Vote.dir))
        .where(models.Vote.post_id == post_id)
    ).scalar()
    return score_result or 0

@router.post("/",  responses={status.HTTP_201_CREATED: {"model": schemas.VoteResponse},status.HTTP_204_NO_CONTENT: { "description":"all is welll"},status.HTTP_200_OK: {"model":schemas.VoteResponse}})
def vote(
    vote: schemas.VoteSchema,
    db: Session = Depends(getdb),
    current_user: int = Depends(oauth2.get_current_user),
      
):
    post = db.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    
    stmt = select(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user)
    found_vote = db.execute(stmt).scalar_one_or_none()

    try:
        if found_vote:
            if found_vote.dir == vote.dir:
                db.delete(found_vote)
                db.commit()
                status_code=status.HTTP_204_NO_CONTENT 
                return
            else:
                found_vote.dir = vote.dir
                db.commit()
                status_code=status.HTTP_200_OK
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user, dir=vote.dir)
            db.add(new_vote)
            db.commit()
            status_code=status.HTTP_201_CREATED
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    current_score = get_post_score(db, vote.post_id)
    return schemas.VoteResponse(message="success", post_id=vote.post_id, current_score=current_score)

 