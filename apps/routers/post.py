from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from ..database import getdb
from sqlalchemy.orm import Session 
from sqlalchemy import func
from typing import List,Optional

from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/posts", tags=["posts"])


# GEt all posts


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.postoutput]
)
def get_posts(
    db: Session = Depends(getdb), current_user: int = Depends(oauth2.get_current_user),limit:int=10,search:Optional[str]=""
):
    posts = db.query(models.posts).filter(models.posts.title.contains(search)).limit(limit).all()
    #posts = db.query(models.posts,func.count(models.votes.post_id)).join(models.votes,models.votes.post_id == models.posts.id, isouter=True).group_by(models.posts.id).filter(models.posts.title.contains(search)).limit(limit).all()  
    
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()

    return posts


# Get specific post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.postvote
)
def get_post(
    id: int,
    db: Session = Depends(getdb),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = [post for post in my_posts if post["id"] == id]
    # cur.execute("SELECT * FROM posts WHERE id = %s",(id,))
    # post = cur.fetchone()
    post = db.query(models.posts).filter(models.posts.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post


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
    print(new_post)
    post_dic = new_post.model_dump()
    post_dic["owner_id"] = current_user
    post = models.posts(**post_dic)
    db.add(post)
    db.commit()
    db.refresh(post)
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
    query = db.query(models.posts).filter(models.posts.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    if post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )
    # my_posts.remove(post)
    query.delete(synchronize_session=False)
    db.commit()

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
    query = db.query(models.posts).filter(models.posts.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    if post.owner_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="not authorized to perform requested action",
        )
    query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post
