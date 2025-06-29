from typing import Any, Dict, List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models, schemas 

async def save_rpi_tank_readings(db: AsyncSession, tank_readings: List[schemas.TankReceive]) -> Dict[str, Any]: 
    """
    Saves a list of tank readings received from a Raspberry Pi into the database.
    Checks for existing station IDs and handles individual record saving errors.
    """
    successfully_saved_data = [] # To return details of successfully saved records
    failed_to_save_data = []     # To return details of failed records

    try:
        for reading in tank_readings:
            try:
                # 1. Check if station exists
                result = await db.execute(
                    select(models.StationService).where(models.StationService.id == reading.station_id)
                )
                station_exists = result.scalars().first()

                if not station_exists:
                    print(f"Warning: Station with ID {reading.station_id} not found for tank reading {reading.id}. Skipping.")
                    failed_to_save_data.append({"id": reading.id, "reason": "Station ID not found"})
                    continue
                
                # 2. Create a new Tank SQLAlchemy model instance
                db_tank = models.Tank(
                    id=reading.id,
                    type=reading.type,
                    level=reading.level,
                    volume=reading.volume,
                    quantity=reading.quantity,
                    temperature=reading.temperature,
                    density=reading.density,
                    createdAt=reading.createdAt,
                    updateAt=reading.updateAt,
                    station_id=reading.station_id
                )
                
                db.add(db_tank)
                
                # Just use the original reading since it's already a TankReceive schema
                successfully_saved_data.append(reading)
                
                print(f"Prepared tank reading {reading.id} for station {reading.station_id}")

            except Exception as e:
                print(f"Error preparing tank reading {reading.id}: {e}")
                failed_to_save_data.append({"id": reading.id, "reason": str(e)})

        # Commit all successful records at once
        if successfully_saved_data:
            await db.commit()
            print(f"Successfully committed {len(successfully_saved_data)} tank readings to database")
        else:
            print("No records to commit")

    except Exception as e:
        await db.rollback()
        print(f"Error during batch commit: {e}")
        # Move all successfully prepared records to failed
        for saved_item in successfully_saved_data:
            failed_to_save_data.append({"id": saved_item.id, "reason": f"Batch commit failed: {str(e)}"})
        successfully_saved_data = []

    return {
        "successfully_saved": successfully_saved_data,
        "failed_to_save": failed_to_save_data
    }
 
 
async def getuserbystationId(id:str,db:AsyncSession,):
    try:
        result = await db.execute(select(models.StationService).filter(models.StationService.id  == id))
        stationservice=result.scalars().first()
        if not stationservice:
           raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Stationservice with id '{id}' is not Found")
        tanks = await db.execute(select(models.Tank).filter(models.Tank.station_id == id).order_by(models.Tank.updateAt.desc()).limit(1))
        tanksfonud = tanks.scalars().first()
        return schemas.ResponseWrapper(
            data=[tanksfonud],
            msg='Tank found successfully',
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )
        

async def gettankdatabyId(id:str,db:AsyncSession,):
    try:
        result = await db.execute(select(models.StationService).filter(models.StationService.id  == id))
        stationservice=result.scalars().first()
        if not stationservice:
           raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Stationservice with id '{id}' is not Found")
        tanks = await db.execute(select(models.Tank).filter(models.Tank.station_id == id))
        tanksfonud = tanks.scalars().all()
        return schemas.ResponseWrapper(
            data=tanksfonud,
            msg='Tank found successfully',
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )        
    
         