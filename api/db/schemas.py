from pydantic import BaseModel, Field, constr
from datetime import datetime
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


class User(BaseModel):
    username: str
    email: str
    password: str
    is_admin: Optional[bool] = False

class UpdateUser(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_admin: Optional[bool]


class UserDisplay(BaseModel):
    username: str
    email: str

class LoginUser(BaseModel):
    username: str
    password: constr(max_length=8)
class RoomNumbers(BaseModel):
    number: int
    unavaliable_dates: Optional[List[datetime]]
    
class Room(BaseModel):
    title: str
    price: float
    max_people: int
    desc: str
    room_numbers: List[RoomNumbers]