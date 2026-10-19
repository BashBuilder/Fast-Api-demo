from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Any

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict[str, Any]):
  to_encode = data.copy()
  
  expire = datetime.now() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
  return encoded_jwt

def verify_token(token : str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if email is None:
      return None
    return email
  except JWTError:
    return None
  
  
  
  