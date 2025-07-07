from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from streamerapp import oauth2
from streamerapp.repository import notificationrepository 
from .. import schemas, database 



router = APIRouter(
    tags=['Notification'],
)

# Router endpoints
@router.post('/createnotification', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseWrapper[schemas.ShowNotification])
async def create_notification(request: schemas.Notification, db: AsyncSession = Depends(database.get_async_db),
                              current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await notificationrepository.createnotification(request, db, current_user)

@router.get('/getlowfuelnotification/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ResponseWrapper[list[schemas.ShowNotification]])
async def get_low_fuel_notification(id, db: AsyncSession = Depends(database.get_async_db),):
    return await notificationrepository.getlowfuelnotification(id, db)

@router.get('/getallnotifications', status_code=status.HTTP_200_OK, response_model=schemas.ResponseWrapper[list[schemas.ShowNotification]])
async def get_all_notifications(db: AsyncSession = Depends(database.get_async_db),):
    return await notificationrepository.getallnotifications(db)

@router.post('/checktanklevels', status_code=status.HTTP_200_OK, response_model=schemas.ResponseWrapper[str])
async def check_tank_levels(db: AsyncSession = Depends(database.get_async_db),):
    return await notificationrepository.checktanklevels(db)