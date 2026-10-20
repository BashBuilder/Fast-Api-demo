from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..schema import RegisterDto, UserResponse
from ..utils import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
  "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def register(payload: RegisterDto, db: Session = Depends(get_db)):
  # hash the password
  hashed_password = hash_password(payload.password)
  payload.password = hashed_password

  user = models.User(**payload.model_dump())

  db.add(user)
  db.commit()
  db.refresh(user)

  return user


@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  return user
