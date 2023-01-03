from fastapi import APIRouter, HTTPException, Depends, status
from db.database import hotels_collection
from db.schemas import Hotels
from bson.objectid import ObjectId

router = APIRouter(
    prefix='/hotels',
    tags = ['hotels']
)

@router.post('/')
async def create_hotel(hotels: Hotels):
    
    try:
        hotels_collection.insert_one(hotels.dict())
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.put('/{id}')
async def update_hotel(id: str, hotels: Hotels):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid id {id}")

    try:
        update_hotel = hotels_collection.find_one_and_update(
            {'_id': ObjectId(id)}, {'$set': hotels.dict(exclude=None)}
        )
        return update_hotel
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))