from pydantic import BaseModel, EmailStr
from typing import Generic, List, Optional, TypeVar
from datetime import datetime


T = TypeVar('T')

class ResponseWrapper(BaseModel, Generic[T]):
    data: T
    msg: str
    success: bool

# User models
class UserBase(BaseModel):
    name: str
    email: EmailStr
    number: int
    role:str

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
    # These fields are now sent by RPi, so they are part of the incoming payload
    id: str # RPi generates this
    createdAt: datetime # RPi generates this
    updateAt: datetime # RPi generates this
    station_id: str # RPi sends this

# This schema will be used for incoming data from RPi
class TankReceive(TankBase):
    pass

class Tank(TankBase):
    class Config:
        from_attributes = True

class TankCreate(TankBase): 
    id: Optional[str] = None 
    createdAt: Optional[datetime] = None
    updateAt: Optional[datetime] = None

class ShowTank(TankBase): # For displaying from your main DB
   
    id: str
    station_id: str

    class Config:
        from_attributes = True

class NotificationBase(BaseModel):
    type:str
    message:str
    createdAt: datetime 
    updateAt: datetime  

class Notification(NotificationBase):
    class Config:
        from_attributes = True
               
class ShowNotification(NotificationBase):
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
    # tanks: List[ShowTank] = []
    
    class Config:
        from_attributes = True       
        

class EmailResponse(BaseModel):
    success: bool
    message: str
    messageId: Optional[str] = None

class EmailRequest(BaseModel):
    from_email: EmailStr
    to_email: EmailStr
    subject: str
    message: str
    is_urgent: bool = False        
        
class login(BaseModel):
    username:str
    password:str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None    
    id:str | None = None            