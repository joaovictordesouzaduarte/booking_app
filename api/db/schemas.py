from pydantic import BaseModel
from typing import List

class Hotels(BaseModel):
    name: str
    type: str
    city: str
    address: str
    distance: str
    photos: List[str]
    title: str
    desc: str
    rating: float
    rooms: List[str]
    cheapestPrice: float
    featured: bool