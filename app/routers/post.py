from fastapi import APIRouter, Depends, HTTPException, status, Response
from ..database import get_db
from ..schema import CreatePost, UpdatePost, Post, PostResponse
from .. import models, oauth2
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func

router = APIRouter( prefix="/posts", tags=["Posts"])

# @router.get("/", response_model=list[Post])
@router.get("/", response_model=list[PostResponse])
def get_posts(db : Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
  results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id, isouter=True ).group_by(models.Post.id).filter(models.Post.title.contains(search)).order_by(models.Post.created_at.desc()).limit(limit).offset(skip).all()
  
  print(results)
  
  # return posts
  return results



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(payload: CreatePost, db : Session = Depends(get_db),  user : models.User = Depends(oauth2.get_current_user)):
  post = models.Post(owner_id=user.id, **payload.model_dump())
  
  db.add(post)
  db.commit()
  db.refresh(post)
  
  return post


@router.get("/{id}", response_model=PostResponse)
def get_post(id: int, db : Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id, isouter=True ).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return post

  
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), user : models.User = Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  
  if str(post.owner_id) != str(user.id):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")
  
  db.delete(post)
  db.commit()
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post)
def update_post(id: int, payload: UpdatePost, db : Session = Depends(get_db), user : models.User = Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == id)
  new_post = post.first()
  
  if not new_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  
  
  if str(new_post.owner_id) != str(user.id):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this post")

  post.update(payload.model_dump(), synchronize_session=False)  # type: ignore

  db.commit()
  
  return post.first()