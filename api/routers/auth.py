from fastapi import APIRouter, HTTPException, Depends, status
from db.database import user_collection
from db.schemas import User, UserDisplay, LoginUser
from auth.oauth2 import oauth2_schema
from utils import hash_password, verify_password
from fastapi.responses import JSONResponse



router = APIRouter(
    prefix='/auth',
    tags = ['auth']
)

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserDisplay)
async def create_user(user: User):
    
    try:
        user_collection.insert_one(
            {
                'username': user.username,
                'email': user.email,
                'password': hash_password(user.password)
            }
        )
        return {
            "status": "success",
            "user": user.username
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

            if not password:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password')

        else:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User {user_login.username} not found!')
        
        del user['_id']
        del user['password']
        return JSONResponse(user)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'User not found!'})