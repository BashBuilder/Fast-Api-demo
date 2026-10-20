from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
  title: str
  content: str


class User(BaseModel):
  email: EmailStr
  password: str


class UserResponse(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    from_attributes = True


class Post(PostBase):
  id: int
  published: bool = True
  created_at: datetime
  owner_id: int
  owner: UserResponse

  class Config:
    # orm_mode = True
    from_attributes = True


class PostResponse(BaseModel):
  Post: Post
  votes: int

  class Config:
    from_attributes = True


class CreatePost(PostBase):
  pass


class UpdatePost(CreatePost):
  pass


class RegisterDto(User):
  pass


class LoginDto(BaseModel):
  email: EmailStr
  password: str


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  sub: str | None = None
  user_id: int | None = None


class Vote(BaseModel):
  post_id: int
  dir: Literal[0, 1]
