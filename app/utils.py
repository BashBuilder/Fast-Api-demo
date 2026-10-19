from passlib.context import CryptContext
from fastapi import HTTPException, status


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    try: 
        return pwd_context.verify(plain_password, hashed_password)  
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")