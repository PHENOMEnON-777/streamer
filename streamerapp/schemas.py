from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User models
class UserBase(BaseModel):
    name: str
    email: EmailStr
    number: int

class User(UserBase):
    password: str
    
    class Config:
        from_attributes = True

class ShowUser(UserBase):
    id: str
    
    class Config:
        from_attributes = True

# Tank models
class TankBase(BaseModel):
    type: str
    level: float
    volume: float
    quantity: float
    temperature: float
    density: float

class Tank(TankBase):
    createdAt: str
    updateAt: str
    
    class Config:
        from_attributes = True

class TankCreate(TankBase):
    pass

class ShowTank(Tank):
    id: str
    station_id: str
    
    class Config:
        from_attributes = True

# StationService models
class StationServiceBase(BaseModel):
    stationservicename: str
    description: str
    location: str

class StationService(StationServiceBase):
    class Config:
        from_attributes = True

class StationServiceCreate(StationServiceBase):
    pass

class ShowStationService(BaseModel):
    id: str
    stationservicename: str
    description: str
    location: str
    owner_id: str
    # tanks: List[ShowTank] = []
    
    class Config:
        from_attributes = True       
        
        
        
class login(BaseModel):
    username:str
    password:str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None    
    id:str | None = None            