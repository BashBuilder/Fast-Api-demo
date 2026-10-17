from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
  id: int
  title : str
  content: str
  published: bool = True
  rating : int | None = None


my_post : list[Post] = [
  Post.model_validate({
    "id": 1,
    "title": "My First Post",
    "content": "This is my first post",
    "published": True,
    "rating": 5
  }),
  Post.model_validate( {
    "id": 2,
    "title": "My Second Post",
    "content": "This is my second post",
    "published": False,
    "rating": 3 
  }),
  Post.model_validate( {
    "id": 3,
    "title": "My Third Post",
    "content": "This is my third post",
    "published": True,
    "rating": 4
  })
]

def find_post(id: int) : 
  found_post = None
  for post in my_post:
    if post.id == id:
      found_post = post
      break
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  
  return found_post


@app.get("/")
def root(): 
  return {"message": "Hello World"}
  
  
@app.get("/posts")
def get_posts():
  return {"data" : my_post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: Post):
  print(payload)
  length = len(my_post)
  payload.id = length + 1
  
  my_post.append(payload)
  return {"data" : my_post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    
    return {"data": post}
  
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int): 
  post = find_post(id)
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  my_post.remove(post)
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
  post = find_post(id)
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  
  post.title = payload.title
  post.content = payload.content
  post.published = payload.published
  
  my_post.remove(post)
  my_post.append(post)
  
  return {"data": post}
      