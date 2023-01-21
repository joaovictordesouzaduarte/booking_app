from fastapi import APIRouter, HTTPException, Depends, status
from db.database import room_collection, hotels_collection
from db.schemas import Room
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from auth.oauth2 import oauth2_schema, get_current_user

router = APIRouter(
    prefix='/rooms',
    tags = ['rooms']
)

@router.post('/create/{hotel_id}')
async def create_new_room(hotel_id: str, room: Room, current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(hotel_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id {hotel_id}")
    try:
        saved_room = room_collection.insert_one(room.dict(exclude_none=True))
        try:
            hotels_collection.find_one_and_update(
                {'_id': ObjectId(hotel_id)},
                {'$push': {'rooms': str(saved_room.inserted_id)}}
            )
        except Exception as ex:
            raise HTTPException(status_code=404, detail='Error while insert room')
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))

    return 'Ok'
    

@router.delete('/delete/{room_id}/{hotel_id}')
async def delete_room(room_id: str, hotel_id: str, current_user = Depends(get_current_user)):

    if not ObjectId.is_valid(hotel_id) or not ObjectId.is_valid(room_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid hotel id {hotel_id} or room id {room_id}")
    try:
        room_collection.find_one_and_delete(
           {'_id': ObjectId(room_id)}
        )
        try:
            hotels_collection.find_one_and_update(
                {'_id': ObjectId(hotel_id)},
                {'$pull': {'rooms': room_id}}
            )
        except Exception as ex:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error while insert room')
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))

    return 'Room has been deleted'