from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
  title : str
  content: str
  
  
class Post(PostBase):
  id: int
  published: bool = True
  created_at: datetime
  class Config:
    # orm_mode = True
    from_attributes = True
  
  
class CreatePost(PostBase):
  pass
  
class UpdatePost(CreatePost):
  pass

class User(BaseModel):
    email: EmailStr
    password: str 
    
class RegisterDto(User):
    pass
  
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
      from_attributes = True
      
class LoginDto(BaseModel):
    email: EmailStr
    password: str
