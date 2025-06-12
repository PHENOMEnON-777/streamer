from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, database, oauth2
from ..repository import stationservicerepository
from typing import List

router = APIRouter(
    tags=['StationService']
)

@router.post('/createStationService', status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseWrapper[schemas.ShowStationService])
async def create_station_service(request: schemas.StationService, db: AsyncSession = Depends(database.get_async_db), 
                              current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await stationservicerepository.create_station_service(request, db, current_user)


@router.get('/allStationServices', status_code=status.HTTP_200_OK,response_model=schemas.ResponseWrapper[list[schemas.ShowStationService]])
async def get_station_services(db: AsyncSession = Depends(database.get_async_db),
                            current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await stationservicerepository.get_all_station_services(db)

@router.get('/allStationServicesbyId/{id}', status_code=status.HTTP_200_OK,response_model=schemas.ResponseWrapper[list[schemas.ShowStationService]])
async def get_station_services_by_id(id,db: AsyncSession = Depends(database.get_async_db),
                            current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await stationservicerepository.get_all_station_services_by_id(id,db)


@router.put('/updateStationService/{id}', status_code=status.HTTP_200_OK,response_model=schemas.ResponseWrapper[schemas.ShowStationService])
async def update_station_service(id, request: schemas.StationService, db: AsyncSession = Depends(database.get_async_db),
                              current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await stationservicerepository.update_station_service(id, request, db) 


@router.delete('/stationService/{id}', status_code=status.HTTP_200_OK,response_model=schemas.ResponseWrapper[schemas.ShowStationService])
async def delete_station_service_by_id(id, db: AsyncSession = Depends(database.get_async_db),
                                    current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await stationservicerepository.delete_station_service(id, db)