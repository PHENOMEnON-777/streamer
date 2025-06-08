from typing import Any, Dict, List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import models, schemas 

async def save_rpi_tank_readings( db: AsyncSession, tank_readings: List[schemas.TankReceive] ) -> Dict[str, Any]: 
    # """
    # Saves a list of tank readings received from a Raspberry Pi into the database.
    # Checks for existing station IDs and handles individual record saving errors.
    # """
    successfully_saved_data = [] # To return details of successfully saved records
    failed_to_save_data = []     # To return details of failed records

    for reading in tank_readings:
        try:
            result = await db.execute( select(models.StationService).where(models.StationService.id == reading.station_id))
            station_exists = result.scalars().first()

            if not station_exists:
                print(f"Warning: Station with ID {reading.station_id} not found for tank reading {reading.id}. Skipping.")
                failed_to_save_data.append({"id": reading.id, "reason": "Station ID not found"})
                continue
                #  raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Stationservice not Found") 
            
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
            await db.commit()
            await db.refresh(db_tank)

         
            successfully_saved_data.append(schemas.TankReceive.model_validate(db_tank))

            print(f"Saved tank reading {reading.id} for station {reading.station_id}")

        except Exception as e:
            await db.rollback() # Rollback if an error occurs for this specific record
            print(f"Error saving tank reading {reading.id}: {e}")
            failed_to_save_data.append({"id": reading.id, "reason": str(e)})

    # This function now returns the raw lists, not a ResponseWrapper
    return {
        "successfully_saved": successfully_saved_data,
        "failed_to_save": failed_to_save_data
    }