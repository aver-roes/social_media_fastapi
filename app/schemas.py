# NOTE: this file is userd to define the schemas

from pydantic import BaseModel
from pydantic import EmailStr
from datetime import datetime
from typing import Optional


# NOTE: this is the schemas for the data that we are going to send to the database (we receive from the client)


# post schema
class Post(BaseModel):
    title: str
    content: str
    published: bool

    class config:
        orm_mode = True


# create post schema
class PostCreate(Post):
    pass


# crete user schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# login user schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# token schema
class Token(BaseModel):
    access_token: str
    token_type: str


# token data schema
class TokenData(BaseModel):
    id: Optional[str] = None


# like schema
class Like(BaseModel):
    post_id: int
    dir: int


class CreateComment(BaseModel):
    com_post_id: int
    content: str

    class config:
        orm_mode = True


# NOTE: this is the schemas for the data that we are going to receive from the database and send to the client


# user response schema
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# post response schema
class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True  # this is to tell pydantic that we are going to use the ORM to map the data


# comment response schema
class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    com_owner_id: int
    com_post_id: int
    com_owner: Optional[UserResponse]  # NOTE: use optional just for testing

    class Config:
        orm_mode = True


# post with number of likes schema
class PostLikeResponse(BaseModel):
    Post: PostResponse
    likes: int

    class config:
        orm_mode = True


# token response schema
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
