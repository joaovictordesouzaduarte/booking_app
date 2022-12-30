from fastapi import APIRouter
from db.database import Hotels
from db.schemas import Hotels

router = APIRouter(
    prefix='/hotels',
    tags = ['hotels']
)

@router.post('/')

async def create_hotel(hotels: Hotels):
    
    try:
        result = hotels
        print(result)
    except Exception as ex:
        print(ex)