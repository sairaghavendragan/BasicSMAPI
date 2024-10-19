from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime


class postbase(BaseModel):
    title: str
    content: str
    published: bool

    # created_at:datetime
    class config:
        orm_mode = True

    # model_config =  configs


class postinput(postbase):
    pass


class postoutput(postbase):
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

    class config:
        orm_mode = True


class userlogin(BaseModel):
    username: EmailStr
    password: str


class token(BaseModel):
    access_token: str
    token_type: str

class vote(BaseModel):
    post_id: int
    dir: bool    
