from pydantic import BaseModel
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
