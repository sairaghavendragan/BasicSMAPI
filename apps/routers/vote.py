from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import getdb
from sqlalchemy.orm import Session
from typing import List,Optional

from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/vote", tags=["votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.vote,
    db: Session = Depends(getdb),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.posts).filter(models.posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    vote_query = db.query(models.votes).filter(
        models.votes.post_id == vote.post_id, models.votes.user_id == current_user 
    )
    found_vote = vote_query.first()  # type: ignore 
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(    
                status_code=status.HTTP_409_CONFLICT,    
                detail=f"user {current_user} has already voted on post {vote.post_id}",    
            )    
        new_vote = models.votes(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()             
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="vote does not exist",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    