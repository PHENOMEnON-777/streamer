import uuid
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update ,delete
from .. import schemas,models

# from enum import Enum

async def create_station_service(request:schemas.StationService,db:AsyncSession,current_user:schemas.User):
    try:
        new_station = models.StationService(
        stationservicename=request.stationservicename,
        description=request.description,
        location=request.location,
        owner_id=current_user.id
    )
        db.add(new_station)
        await db.commit()
        await db.refresh(new_station)
        return schemas.ResponseWrapper(
            data=new_station,
            msg='Stations service created successfully',
            success=True
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        ) 
    
async def get_all_station_services(db:AsyncSession):
    try:
         result = await db.execute(select(models.StationService))
         statioinservices = result.unique().scalars().all()  
         return schemas.ResponseWrapper(
            data=statioinservices,
            msg=' got all Stations successfully',
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )
        
        
async def get_all_station_services_by_id(id,db:AsyncSession):
    try:
         result = await db.execute(select(models.StationService).filter(models.StationService.owner_id==id))
         statioinservices = result.unique().scalars().all()  
         return schemas.ResponseWrapper(
            data=statioinservices,
            msg=' got all Stations successfully',
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )         
        
       
        
async def update_station_service(id:str,request:schemas.StationService,db:AsyncSession):
    try:
            result = await db.execute(select(models.StationService).filter(models.StationService.id == id))
            stationservice = result.scalars().first()
            if not stationservice:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="stationservice not Found")
            stmt = (
            update(models.StationService).where(models.StationService.id == id).values(**request.model_dump(exclude_unset=True)))   
            await db.execute(stmt)
            await db.commit()
            updated_result = await db.execute(select(models.StationService).filter(models.StationService.id == id))
            return schemas.ResponseWrapper(
                data=updated_result.scalars().first(),
                msg="updated successfully",
                success=True
            )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        ) 

async def delete_station_service(id:str,db:AsyncSession):
    try:
            result = await db.execute(select(models.StationService).filter(models.StationService.id == id))
            stationservice=result.scalars().first()
            if not stationservice:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Stationservice not Found")   
            stmt=(delete(models.StationService).where(models.StationService.id == id))
            await db.execute(stmt)
            await db.commit()
            user_data = {
           "id": stationservice.id,
           "stationservicename": stationservice.stationservicename,
           "description": stationservice.description,
           "location": stationservice.location
        }
            return schemas.ResponseWrapper(
                data=user_data,
                msg="deleted successfully",
                success=True
            )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )       