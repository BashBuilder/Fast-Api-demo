from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schema
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
  vote: schema.Vote,
  db: Session = Depends(get_db),
  user: models.User = Depends(get_current_user),
):
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  vote_query = (
    db.query(models.Vote)
    .filter(models.Vote.post_id == vote.post_id)
    .filter(models.Vote.user_id == user.id)
  )
  found_vote = vote_query.first()

  if vote.dir == 1:
    if found_vote:
      raise HTTPException(status_code=400, detail="You already voted for this post")

    new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "You have voted for this post"}

  else:
    if not found_vote:
      raise HTTPException(status_code=400, detail="You have not voted for this post")

    db.delete(found_vote)
    db.commit()
    return {"message": "You have removed your vote for this post"}
