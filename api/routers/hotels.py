from fastapi import APIRouter, HTTPException, Depends, status
from db.database import hotels_collection
from db.schemas import Hotel, UpdateHotel
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from auth.oauth2 import oauth2_schema

router = APIRouter(
    prefix='/hotels',
    tags = ['hotels']
)

@router.post('/')
async def create_hotel(hotels: Hotel):
    
    try:
        hotels_collection.insert_one(hotels.dict())
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.put('/{id}')
async def update_hotel(id: str, hotel:UpdateHotel):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    try:
        hotels = hotels_collection.find_one_and_update(
            {'_id': ObjectId(id)}, {'$set': hotel.dict(exclude_none = True)}, return_document=ReturnDocument.AFTER
        )
        del hotels['_id']
        return hotels
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete('/{id}')
async def delete_hotel(id: str):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    try:
        hotels_collection.find_one_and_delete({'_id': ObjectId(id)})
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.get('/{id}')
async def get_hotel_by_id(id: str):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")
    hotel = None
    try:
        hotel = hotels_collection.find_one({'_id': ObjectId(id)})
        del hotel['_id']
        return hotel
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.get('/')
async def get_hotels():

    hotels = {}
    try:
        data = hotels_collection.find()
        for hotel in data:
            hotels.update(hotel)

        del hotels['_id']
        return hotels
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))
