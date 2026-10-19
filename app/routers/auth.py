from fastapi import APIRouter, Depends, HTTPException, status
from ..import database, schema, models, utils
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_crendentials: schema.LoginDto, db : Session = Depends(database.get_db)):
   try:
    user = db.query(models.User).filter(models.User.email == user_crendentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
       
    verify_password = utils.verify_password(user_crendentials.password, str(user.password))
     
    if not verify_password:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
     
    # create token
    access_token = oauth2.create_access_token({"sub": user.email, "user_id" : user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
       
      
   except Exception as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))