from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Any
from . import schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import database, models
from sqlalchemy.orm import Session

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict[str, Any]):
  to_encode = data.copy()
  
  expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
  return encoded_jwt

def verify_token(token : str, credentials_exception : Any):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    id = payload.get("user_id")
    if not email or not id:
      raise credentials_exception
    
    token_data = schema.TokenData(sub=email, user_id=id)
    return token_data
  except JWTError:
    raise credentials_exception
  
def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)) -> models.User:
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  
  tokenData : schema.TokenData = verify_token(token, credentials_exception)
  
  user = db.query(models.User).filter(models.User.id == tokenData.user_id).first()
  if not user:
    raise credentials_exception
    
  return user
  
  
  
  
  
  