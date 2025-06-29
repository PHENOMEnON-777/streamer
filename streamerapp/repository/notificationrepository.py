import uuid
from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update ,delete
from .. import schemas,models


async def createnotification(request:schemas.Notification,db:AsyncSession,current_user:schemas.User):
    result = await db.execute(
    select(models.Tank.id)
    .order_by(models.Tank.createdAt.asc())
    .limit(1)
    )
    tank_id = result.scalar_one_or_none() 

    if not tank_id:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No tank found to associate with notification"
    )
    try:
        new_notification = models.Notification(
        type=request.type,
        message=request.message,
        tank_id = tank_id
    )
        db.add(new_notification)
        await db.commit()
        await db.refresh(new_notification)
        return schemas.ResponseWrapper(
            data=new_notification,
            msg='Notification created successfully',
            success=True
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )
        
async def getlowfuelnotification(id:str,db:AsyncSession):
    try:
        result = await db.execute(select(models.Tank).filter(models.Tank.id == id))
        tankstate = result.scalars().first()
        if not tankstate:
             raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Tank with id '{id}' is not Found")
        value = float(85.77)
        tanks = await db.execute(select(models.Tank).filter(models.Tank.level == value).order_by(models.Tank.createdAt.asc()).limit(1))
        tanksfonud = tanks.scalars().first()
        if not tanksfonud:
            notification_result = await db.execute(select(models.Notification).filter(models.Notification.type == 'Low'))
            notification = notification_result.scalars().all()
            print(tanksfonud)
            return schemas.ResponseWrapper(
            data=notification,
            msg='successfully notified',
            success=True)
        else:
            notification_result = await db.execute(select(models.Notification).filter(models.Notification.type == 'Low'))
            notification = notification_result.scalars().all()
            print(notification)
            return schemas.ResponseWrapper(
                data=[],
                msg='No low fuel tanks found',
                success=True
            )    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        ) 
         
                    