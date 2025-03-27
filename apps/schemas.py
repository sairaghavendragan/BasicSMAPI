from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime
from typing import Literal


class PostBase(BaseModel):
    title: str
    content: str
    published: bool

    # created_at:datetime
    model_config = ConfigDict(from_attributes=True)

    # model_config =  configs


class postinput(PostBase):
    pass


class postoutput(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    pass

class postvote(BaseModel):
    Posts: postoutput
    vote: int
    model_config = ConfigDict(
        from_attributes=True
    )


class usercreate(BaseModel):
    email: EmailStr
    password: str


class useroutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class userlogin(BaseModel):
    username: EmailStr
    password: str


class token(BaseModel):
    access_token: str
    token_type: str

class VoteSchema(BaseModel): # Renamed for consistency
    post_id: int
    # Direction: 1 for upvote, -1 for downvote, 0 to clear vote
    dir: Literal[1, -1 ]


class VoteResponse(BaseModel):
    message: str
    post_id: int
    current_score: int # Optional: return the new score

class PostWithScore(BaseModel): 
    post: postoutput
    score: int
    model_config = ConfigDict(from_attributes=True)      


 