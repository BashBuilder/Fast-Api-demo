from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
  title : str
  content: str
  published: bool = True
  rating : int | None = None



@app.get("/")
def root(): 
  return {"message": "Hello World"}
  
@app.get("/posts")
def get_posts():
  return {"data" : "These are the posts"}

@app.post("/posts")
def create_posts(payload: Post):
  print(payload.model_dump())
  return {"data" : f"New post created with title {payload.title}, and content {payload.content}, published {payload.published}, rating {payload.rating}"}