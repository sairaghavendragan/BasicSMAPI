from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import getdb
from sqlalchemy.orm import Session 
from sqlalchemy import func
from sqlalchemy import select
from typing import List,Optional

from .. import models, schemas, utils, oauth2
from . import vote

router = APIRouter(prefix="/posts", tags=["posts"])


# GEt all posts


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostWithScore]
)
def get_posts(
    db: Session = Depends(getdb), current_user: int = Depends(oauth2.get_current_user),limit:int=10,search:Optional[str]=""
):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    stmt = select(models.Post).filter(models.Post.title.contains(search)).limit(limit) 
    posts = db.execute(stmt).scalars().all()
    for post in posts:
        setattr (post,"post",post)
        setattr (post,"score",vote.get_post_score(db,post.id))
        #post.score = num_votes
    #posts = db.query(models.posts,func.count(models.votes.post_id)).join(models.votes,models.votes.post_id == models.posts.id, isouter=True).group_by(models.posts.id).filter(models.posts.title.contains(search)).limit(limit).all()  
    
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()

    return posts


# Get specific post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostWithScore
)
def get_post(
    id: int,
    db: Session = Depends(getdb),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = [post for post in my_posts if post["id"] == id]
    # cur.execute("SELECT * FROM posts WHERE id = %s",(id,))
    # post = cur.fetchone()
    stmt = select(models.Post).filter(models.Post.id == id)
    post = db.execute(stmt).scalar_one_or_none()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return schemas.PostWithScore(post=post,score=vote.get_post_score(db,id))


"""@app.get("/posts/latest")
def get_latest_post():
    post  = my_posts[-1]
    return {"data":post}"""

# create route


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.postoutput
)
def create_posts(
    new_post: schemas.postinput,
    db: Session = Depends(getdb),
    current_user: int = Depends(oauth2.get_current_user),
):
    #print(new_post)
    post_dict = new_post.model_dump()
    post_dict["owner_id"] = current_user
    post = models.Post(**post_dict)
    try:
        db.add(post)
        db.commit()
        db.refresh(post)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
     
    #
    # cur.commit()
    # post_dic["id"] = random.randrange(0,1000000)

    # my_posts.append(post_dic)

    return post


# Delete Operation


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(
    id: int,
    db: Session = Depends(getdb),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = [post for post in my_posts if post["id"] == id]
    # cur.execute("DELETE FROM posts WHERE id = %s returning *"  ,(str(id),))
    # post = cur.fetchone()
    # conn.commit()
    # post = cur.fetchone()
    stmt = select(models.Post).filter(models.Post.id == id)
    post = db.execute(stmt).scalar_one_or_none()
    #query = db.query(models.Post).filter(models.Post.id == id)
    #post = query.first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )
    # my_posts.remove(post)
    try:

        db.delete(post)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting post: {str(e)}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update operation


@router.put("/{id}", response_model=schemas.postoutput)
def update_posts(
    id: int,
    new_post: schemas.postinput,
    db: Session = Depends(getdb),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = [post for post in my_posts if post["id"] == id]
    # cur.execute("UPDATE posts SET title = %s, content = %s, is_published = %s WHERE id = %s returning *"  ,
    # (new_post.title, new_post.content, new_post.published, str(id)))
    # post = cur.fetchone()
    # conn.commit()
    # post = cur.fetchone()
    stmt = select(models.Post).filter(models.Post.id == id)
    post = db.execute(stmt).scalar_one_or_none()
    #query = db.query(models.Post).filter(models.Post.id == id)
    #post = query.first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )
    for key,value in new_post.model_dump().items():
        setattr(post,key,value)
    try:

         
        db.commit()
        db.refresh(post)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating post: {str(e)}")
    return post
