from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from dotenv import load_dotenv, find_dotenv
from jose import jwt, JWTError
import os
from fastapi import Depends, HTTPException, status
from db.database import user_collection


oauth2_schema = OAuth2PasswordBearer(tokenUrl='token') 
load_dotenv(find_dotenv())
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_collection.find_one({'username': username})
    if user is None:
        raise credentials_exception
    return {'access_token': token, 'username': user['username'], "token_type": "bearer"}