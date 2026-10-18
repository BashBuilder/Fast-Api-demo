from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from time import sleep
from psycopg2 import connect

app = FastAPI()

class Post(BaseModel):
  id: int
  title : str
  content: str
  published: bool = True
  rating : int | None = None
  
  
class CreatePost(BaseModel):
  title : str
  content: str


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

while True:
  try : 
    conn = connect(host="localhost", port=5432, user="postgres", password="postgres", database="fastapi", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connected to database")
    break
  except Exception as error :
    print("Error connecting to database")
    print("Error", error)
    sleep(2)


def find_post(id: int) : 
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
  


  
  
@app.get("/posts")
def get_posts():
  cursor.execute("SELECT * FROM posts")
  posts = cursor.fetchall()
  return {"data" : posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(payload: CreatePost):
  cursor.execute("INSERT INTO posts (title, content ) VALUES (%s, %s) RETURNING *", (payload.title, payload.content))
  post = cursor.fetchone()
  conn.commit()
  return {"data" : post}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    
    return {"data": post}
  
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int): 
  post = find_post(id)
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  
  cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
  conn.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, payload: Post):
  post = find_post(id)
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", (payload.title, payload.content, id))
  conn.commit()
  
  return {"data": post}
      