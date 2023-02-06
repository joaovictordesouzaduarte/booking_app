from fastapi import APIRouter, HTTPException, Depends, status, Query, Request
from json import JSONEncoder, dumps
from db.database import hotels_collection, room_collection
from db.schemas import Hotel, UpdateHotel
from bson.objectid import ObjectId
from pymongo import ReturnDocument
from auth.oauth2 import oauth2_schema, get_current_user

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("/countbycity")
async def get_count_by_cities(
    cities: str = Query(
        ..., description="Count of cities, like: london, berlin, madrid"
    )
):
    # current_user: str = Depends(get_current_user)):
    """

    Return an array with number of hotels in each city

    **Cities**: String with comma, ie: london, berlin, madrid

    """

    cities = cities.split(",")
    try:
        number_of_hotels = [
            hotels_collection.count_documents({"city": city}) for city in cities
        ]
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return number_of_hotels


@router.get("/countbytype")
async def get_count_by_type(
    types: str = Query(..., description="Hotel types, ie: villa, resort, suits")
):
    # current_user: str = Depends(get_current_user)):
    """

    Return an array with number of hotels types in each city

    **Type**: String with comma, ie: london, berlin, madrid

    """
    number_of_type = []
    types = types.split(",")
    try:
        for type in types:

            count_by_type = {
                "type": type,
                "count": hotels_collection.count_documents({"type": type}),
            }
            number_of_type.append(count_by_type)

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return number_of_type


@router.post("/create")
async def create_hotel(hotels: Hotel, current_user: str = Depends(get_current_user)):

    try:
        hotels_collection.insert_one(hotels.dict())
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return "Ok"


@router.put("/update/{id}")
async def update_hotel(
    id: str, hotel: UpdateHotel, current_user: str = Depends(get_current_user)
):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id {id}"
        )

    try:
        hotels = hotels_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": hotel.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER,
        )
        hotels["_id"] = str(hotels["_id"])
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return hotels


@router.delete("/delete/{id}")
async def delete_hotel(id: str, current_user: str = Depends(get_current_user)):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id {id}"
        )

    try:
        hotels_collection.find_one_and_delete({"_id": ObjectId(id)})
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.get("/all")
async def get_all_hotels(request: Request = Query()):
    hotels = []

    def clean_null_terms(d):
        return {k: v for k, v in d.items() if v is not None}

    def clean_type(d):
        if d == "True":
            return True
        else:
            return False

    try:
        min = {}
        max = {}
        others = {}

        for key in request.query_params.keys():
            if key == "min":
                min[key] = int(request.query_params.get(key))
            elif key == "max":
                max[key] = int(request.query_params.get(key))
            else:
                others[key] = request.query_params.get(key)

        if "featured" in others.keys():
            others["featured"] = clean_type(others["featured"])

        others = clean_null_terms(others)
        cheapest_price = {
            "cheapestPrice": {
                "$gt": min["min"] if min else 1,
                "$lt": max["max"] if max else 99999,
            }
        }
        others = {**cheapest_price, **others}

        if "limit" in others.keys():
            del others["limit"]
            all_hotels = hotels_collection.find(others).limit(
                int(request.query_params.get("limit"))
            )
        else:
            all_hotels = hotels_collection.find(others)
        for hotel in all_hotels:
            hotel["_id"] = str(hotel["_id"])
            hotels.append(hotel)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={f"No one hotel was found"}
        )
    return hotels


@router.get("/{id}")
async def get_hotel_by_id(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id {id}"
        )
    hotel = None

    try:
        hotel = hotels_collection.find_one({"_id": ObjectId(id)})

        if hotel is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hotel with id {id} not found",
            )
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    hotel["_id"] = str(hotel["_id"])
    return hotel


@router.get("/hotelroom/{hotel_id}")
async def get_hotel_rooms(hotel_id: str):
    
    if not ObjectId.is_valid(hotel_id):
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid id {hotel_id}"
       )

    try:
        hotel = hotels_collection.find_one({"_id": ObjectId(hotel_id)})
        list_of_rooms = [room_collection.find_one({'_id': ObjectId(room)}) for room in hotel['rooms'] ]
        for i in list_of_rooms:
            for k, v in i.items():
                if k == '_id':
                    i[k] = str(i[k])
    except Exception as ex:
        raise HTTPException(status_code=404, detail='Error while returning hotel rooms')
    return list_of_rooms