from fastapi import APIRouter, HTTPException, Depends, status
from db.database import user_collection
from db.schemas import User, UserDisplay, LoginUser
from pydantic import BaseModel
from datetime import timedelta
from auth.oauth2 import oauth2_schema, get_current_user
from auth.oauth2 import create_access_token
from utils import hash_password, verify_password
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags = ['auth']
)


@router.post('/token')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = user_collection.find_one({'username': form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User or password incorrect'
        )
    if not verify_password(form_data.password,user['password']):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User or password incorrect')
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    
    try:
        user_collection.insert_one(
            {
                'username': user.username,
                'email': user.email,
                'password': hash_password(user.password),
                'is_admin': user.is_admin
            }
        )
        return {
            "status": "success",
            "user": user.username,
            "email": user.email
        }

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))

@router.post('/login')
async def login_user(user_login: LoginUser):
    try:
        user = user_collection.find_one(
            {
                'username': user_login.username,
            }
        )
        if user:
            password = verify_password(user_login.password, user['password'])
            user['_id'] = str(user['_id'])
            if not password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password')
        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User {user_login.username} not found!')
        
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found!')
    
    return  JSONResponse(user)
    