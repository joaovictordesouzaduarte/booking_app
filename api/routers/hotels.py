from fastapi import APIRouter, HTTPException, Depends, status, Query
from json import JSONEncoder, dumps
from db.database import hotels_collection
from db.schemas import Hotel, UpdateHotel
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from auth.oauth2 import oauth2_schema, get_current_user

router = APIRouter(
    prefix='/hotels',
    tags = ['hotels']
)
@router.get('/countbycity')
async def get_count_by_cities(cities: str = Query(..., description='Count of cities, like: london, berlin, madrid')): 
                            #current_user: str = Depends(get_current_user)):
    """
    
        Return an array with number of hotels in each city

        **Cities**: String with comma, ie: london, berlin, madrid
    
    """
    
    cities = cities.split(',')
    try:
        number_of_hotels = [hotels_collection.count_documents({'city': city}) for city in cities]
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return number_of_hotels
@router.get('/countbytype')
async def get_count_by_type(types: str = Query(..., description='Hotel types, ie: villa, resort, suits')): 
                            #current_user: str = Depends(get_current_user)):
    """
    
        Return an array with number of hotels types in each city

        **Type**: String with comma, ie: london, berlin, madrid
    
    """
    number_of_type = []
    types = types.split(',')
    try:
        for type in types:
            
            count_by_type = {
                'type': type,
                'count': hotels_collection.count_documents({'type': type})
            }
            number_of_type.append(count_by_type)

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))
        
    return number_of_type
@router.post('/create')
async def create_hotel(hotels: Hotel, current_user: str = Depends(get_current_user)):
    
    try:
        hotels_collection.insert_one(hotels.dict())
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return 'Ok'

@router.put('/update/{id}')
async def update_hotel(id: str, hotel:UpdateHotel, current_user: str = Depends(get_current_user)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    
    try:
        hotels = hotels_collection.find_one_and_update(
            {'_id': ObjectId(id)}, {'$set': hotel.dict(exclude_none = True)}, return_document=ReturnDocument.AFTER
        )
        hotels['_id'] = str(hotels['_id'])
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    
    return hotels
@router.delete('/delete/{id}')
async def delete_hotel(id: str, current_user: str = Depends(get_current_user)):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    try:
        hotels_collection.find_one_and_delete({'_id': ObjectId(id)})
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))
@router.get('/all')
async def get_all_hotels(current_user: str = Depends(get_current_user)):
    hotels = []
    try:
        all_hotels = hotels_collection.find()

        for hotel in all_hotels:
            hotel['_id'] = str(hotel['_id'])
            hotels.append(hotel)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={f'No one hotel was found'})
    return hotels
@router.get('/{id}')
async def get_hotel_by_id(id: str, current_user: str = Depends(get_current_user)):

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")
    hotel = None

    try:
        hotel = hotels_collection.find_one({'_id': ObjectId(id)})
        
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Hotel with id {id} not found')
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    hotel['_id'] = str(hotel['_id'])
    return hotel




