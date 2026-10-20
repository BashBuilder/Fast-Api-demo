from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schema, utils

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schema.Token)
def login(
  user_crendentials: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(database.get_db),
):
  user = (
    db.query(models.User)
    .filter(models.User.email == user_crendentials.username)
    .first()
  )
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  verify_password = utils.verify_password(
    user_crendentials.password, str(user.password)
  )

  if not verify_password:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )

  # create token
  access_token = oauth2.create_access_token({"sub": user.email, "user_id": user.id})

  return {"access_token": access_token, "token_type": "bearer"}
