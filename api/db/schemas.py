from pydantic import BaseModel, Field
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
    rating: int = Field(..., gt=0, le=5)
    rooms: List[str]
    cheapestPrice: int
    featured: bool