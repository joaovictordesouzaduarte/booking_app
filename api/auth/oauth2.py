from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from dotenv import load_dotenv, find_dotenv
from jose import jwt
import os


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