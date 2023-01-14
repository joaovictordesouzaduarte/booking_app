from fastapi import APIRouter, HTTPException, Depends, status, Query
from db.database import user_collection
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from db.schemas import UpdateUser
from auth.oauth2 import  get_current_user


router = APIRouter(
    prefix='/users',
    tags = ['users'],
)


@router.put('/update/{id}')
def update_user(id: str, user: UpdateUser, current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    try:
        if id != current_user['user_id'] and not current_user['is_admin']:
            raise ValueError('You are not authorized to do that')

        user_update = user_collection.find_one_and_update(
                {'_id': ObjectId(id)}, {
                '$set': user.dict(exclude_none=True)
            }, return_document=ReturnDocument.AFTER
        )
        del user_update['_id']
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    
    return user_update

@router.delete('/delete/{id}')
def delete_user(id: str, current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    try:
        if id != current_user['user_id'] and not current_user['is_admin']:
            raise ValueError('You are not authorized to do that')

        user_collection.find_one_and_delete(
                {'_id': ObjectId(id)}, {
            }
        )
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return 'Ok'
@router.get('/all')
def get_user(current_user = Depends(get_current_user)):

    users = []
    try:
        all_users = user_collection.find({})
        for user in all_users:
            del user['_id']
            users.append(user)

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return users
@router.get('/{id}')
def get_user_by_id(id: str, current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    try:

        user = user_collection.find_one(
                {'_id': ObjectId(id)}
        )
        del user['_id']
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return user

