from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, desc
from .. import schemas, models
from datetime import datetime, timedelta


async def createnotification(request: schemas.Notification, db: AsyncSession, current_user: schemas.User):
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
            tank_id=tank_id
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


async def getlowfuelnotification(id: str, db: AsyncSession):
    try:
        # Check if tank exists
        result = await db.execute(select(models.Tank).filter(models.Tank.id == id))
        tank = result.scalars().first()
        if not tank:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Tank with id '{id}' is not found"
            )
        
        # Check if tank level is below 30
        if tank.level < 30:
            # Get low fuel notifications for this tank
            notification_result = await db.execute(
                select(models.Notification)
                .filter(models.Notification.type == 'Low')
                .filter(models.Notification.tank_id == id)
                .order_by(models.Notification.createdAt.desc())
            )
            notifications = notification_result.scalars().all()
            
            return schemas.ResponseWrapper(
                data=notifications,
                msg=f'Low fuel alert: Tank level is {tank.level}%',
                success=True
            )
        else:
            return schemas.ResponseWrapper(
                data=[],
                msg=f'Tank level is sufficient: {tank.level}%',
                success=True
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred: {str(e)}"
        )


async def getallnotifications(db: AsyncSession):
    try:
        result = await db.execute(
            select(models.Notification)
            .order_by(models.Notification.createdAt.desc())
        )
        notifications = result.scalars().all()
        
        return schemas.ResponseWrapper(
            data=notifications,
            msg='All notifications retrieved successfully',
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred: {str(e)}"
        )


async def checktanklevels(db: AsyncSession):
    """
    Check all tanks and generate notifications for:
    1. Low fuel (level < 30)
    2. Fuel increase (level increased from previous reading)
    """
    try:
        # Get all tanks
        tanks_result = await db.execute(select(models.Tank))
        tanks = tanks_result.scalars().all()
        
        notifications_created = 0
        
        for tank in tanks:
            # Check for low fuel
            if tank.level < 30:
                # Check if we already have a recent low fuel notification for this tank
                recent_low_notification = await db.execute(
                    select(models.Notification)
                    .filter(models.Notification.tank_id == tank.id)
                    .filter(models.Notification.type == 'Low')
                    .filter(models.Notification.createdAt >= datetime.now() - timedelta(hours=1))
                    .order_by(models.Notification.createdAt.desc())
                    .limit(1)
                )
                
                if not recent_low_notification.scalars().first():
                    # Create low fuel notification
                    low_notification = models.Notification(
                        type='Low',
                        message=f'Low fuel alert: Tank {tank.id} level is {tank.level}%',
                        tank_id=tank.id
                    )
                    db.add(low_notification)
                    notifications_created += 1
            
            # Check for fuel increase
            # Get the second most recent tank reading to compare
            previous_readings = await db.execute(
                select(models.Tank)
                .filter(models.Tank.id == tank.id)
                .order_by(models.Tank.createdAt.desc())
                .limit(2)
            )
            readings = previous_readings.scalars().all()
            
            if len(readings) > 1:
                current_level = readings[0].level
                previous_level = readings[1].level
                
                if current_level > previous_level:
                    # Check if we already have a recent increase notification
                    recent_increase_notification = await db.execute(
                        select(models.Notification)
                        .filter(models.Notification.tank_id == tank.id)
                        .filter(models.Notification.type == 'Increase')
                        .filter(models.Notification.createdAt >= datetime.now() - timedelta(hours=1))
                        .order_by(models.Notification.createdAt.desc())
                        .limit(1)
                    )
                    
                    if not recent_increase_notification.scalars().first():
                        # Create fuel increase notification
                        increase_notification = models.Notification(
                            type='Increase',
                            message=f'Fuel level increased: Tank {tank.id} from {previous_level}% to {current_level}%',
                            tank_id=tank.id
                        )
                        db.add(increase_notification)
                        notifications_created += 1
        
        await db.commit()
        
        return schemas.ResponseWrapper(
            data=f"{notifications_created} notifications created",
            msg='Tank levels checked and notifications generated',
            success=True
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred: {str(e)}"
        )


# Alternative function to automatically check and create notifications when tank data is updated
async def auto_generate_notifications(tank_id: str, new_level: float, db: AsyncSession):
    """
    This function can be called whenever tank data is updated to automatically generate notifications
    """
    try:
        # Check for low fuel
        if new_level < 30:
            # Check if we already have a recent low fuel notification
            recent_low_notification = await db.execute(
                select(models.Notification)
                .filter(models.Notification.tank_id == tank_id)
                .filter(models.Notification.type == 'Low')
                .filter(models.Notification.createdAt >= datetime.now() - timedelta(hours=1))
                .limit(1)
            )
            
            if not recent_low_notification.scalars().first():
                low_notification = models.Notification(
                    type='Low',
                    message=f'Low fuel alert: Tank {tank_id} level is {new_level}%',
                    tank_id=tank_id
                )
                db.add(low_notification)
        
        # Check for fuel increase
        previous_reading = await db.execute(
            select(models.Tank)
            .filter(models.Tank.id == tank_id)
            .order_by(models.Tank.createdAt.desc())
            .offset(1)  # Skip the current reading
            .limit(1)
        )
        previous_tank = previous_reading.scalars().first()
        
        if previous_tank and new_level > previous_tank.level:
            # Check if we already have a recent increase notification
            recent_increase_notification = await db.execute(
                select(models.Notification)
                .filter(models.Notification.tank_id == tank_id)
                .filter(models.Notification.type == 'Increase')
                .filter(models.Notification.createdAt >= datetime.now() - timedelta(hours=1))
                .limit(1)
            )
            
            if not recent_increase_notification.scalars().first():
                increase_notification = models.Notification(
                    type='Increase',
                    message=f'Fuel level increased: Tank {tank_id} from {previous_tank.level}% to {new_level}%',
                    tank_id=tank_id
                )
                db.add(increase_notification)
        
        await db.commit()
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while generating notifications: {str(e)}"
        )