from fastapi import FastAPI, status, HTTPException, Response, Depends
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session
from .schema import CreatePost, UpdatePost, Post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

  
@app.get("/posts", response_model=list[Post])
def get_posts(db : Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  return posts



@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(payload: CreatePost, db : Session = Depends(get_db)):
  post = models.Post(**payload.model_dump())
  
  db.add(post)
  db.commit()
  db.refresh(post)
  
  return post


@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post

  
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  
  db.delete(post)
  db.commit()
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=Post)
def update_post(id: int, payload: UpdatePost, db : Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id)
  
  if not post.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  post.update(payload.model_dump(), synchronize_session=False)  # type: ignore

  db.commit()
  
  return post.first()
      