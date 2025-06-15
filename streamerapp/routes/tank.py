from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from streamerapp import oauth2
from streamerapp.repository import tankrepository 
from .. import schemas, database 



router = APIRouter(
    tags=['Tank'],
    prefix="/tanks" 
)

@router.post("/receive-data", response_model=schemas.ResponseWrapper[List[schemas.TankReceive]], status_code=status.HTTP_200_OK)
async def receive_tank_data_from_rpi(
    tank_readings: List[schemas.TankReceive],
    db: AsyncSession = Depends(database.get_async_db)
):
    """
    Receives tank data sent from the Raspberry Pi and uses the repository
    to save it to the main database.
    """
    if not tank_readings:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No tank readings provided.")

    results = await tankrepository.save_rpi_tank_readings( tank_readings,db)

    successfully_saved = results["successfully_saved"]
    failed_to_save = results["failed_to_save"]

    if failed_to_save:
        msg = (f"Successfully processed {len(successfully_saved)} readings. "
               f"{len(failed_to_save)} readings failed.") 
        return schemas.ResponseWrapper(
            data=successfully_saved, 
            msg=msg,
            success=False 
        )
    return schemas.ResponseWrapper(
        data=successfully_saved,
        msg=f"Successfully received and saved {len(successfully_saved)} tank readings.",
        success=True
    )


@router.get("/gettankbystationId/{id}",response_model=schemas.ResponseWrapper[list[schemas.ShowTank]],status_code=status.HTTP_200_OK)
async def gettankBystationId(id, db: AsyncSession = Depends(database.get_async_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return await tankrepository.getuserbystationId(id ,db,)



@router.get("/gettankdatabyId/{id}",response_model=schemas.ResponseWrapper[list[schemas.ShowTank]],status_code=status.HTTP_200_OK)
async def gettankdatabyId(id, db: AsyncSession = Depends(database.get_async_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return await tankrepository.gettankdatabyId(id ,db,)
    