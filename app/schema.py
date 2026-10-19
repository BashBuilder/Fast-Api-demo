from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
  title : str
  content: str
  
  
class Post(PostBase):
  id: int
  published: bool = True
  created_at: datetime
  owner_id: int
  # owner: User
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
    
class Token(BaseModel):
   access_token: str
   token_type: str
   
class TokenData(BaseModel):
   sub: Optional[str] = None
   user_id: Optional[int] = None
