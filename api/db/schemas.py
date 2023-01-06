from pydantic import BaseModel, Field
from typing import List, Optional

class Hotel(BaseModel):
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

class UpdateHotel(BaseModel):
    name: Optional[str]=None
    type: Optional[str]=None
    city: Optional[str]=None
    address: Optional[str]=None
    distance: Optional[str]=None
    photos: Optional[List[str]]=None
    title: Optional[str]=None
    desc: Optional[str]=None
    rating: int = Field(None, gt=0, le=5)
    rooms: Optional[List[str]]=None
    cheapestPrice: Optional[int]=None
    featured: Optional[bool]=None