from fastapi import HTTPException,status
from .. import models,hashing,schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update


async def create(request:schemas.User,db:AsyncSession):
    try:
        result= await db.execute(select(models.User).filter(models.User.email == request.email))
        email_exist =result.scalars().first()
        if email_exist:
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists, please change your email")
        user = models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password),number=request.number,role=request.role)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return schemas.ResponseWrapper(
            data=user,
            msg="User Registered successfully",
            success=True
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )
    
async def getallusers(db:AsyncSession,current_user:schemas.User):
    try:
        result = await db.execute(select(models.User))
        users = result.unique().scalars().all()
        return schemas.ResponseWrapper(
            data= users,
            msg='got all Users successfully',
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )
async def getallusersformobile(db:AsyncSession,):
    try:
        result = await db.execute(select(models.User))
        users = result.unique().scalars().all()
        return schemas.ResponseWrapper(
            data= users,
            msg='got all Users successfully',
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )             

async def getuserbyid(db:AsyncSession,current_user:schemas.User):
    try:
        result = await db.execute(select(models.User).filter(models.User.id == current_user.id))
        user=result.scalars().first()
        if not user:
            raise  HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail="Email already exists, please change your email"
             )
        return schemas.ResponseWrapper(
            data=user,
            msg="got user by id successfully",
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )    
    

async def updateuser(request: schemas.User, id:str, db: AsyncSession, current_user: schemas.User):
    try:
        # Fetch the user to update
        result = await db.execute(select(models.User).filter(models.User.id == id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")

        update_data = request.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] != user.email:
            email_check = await db.execute(select(models.User).filter(models.User.email == update_data["email"]))
            existing_email = email_check.scalars().first()
            if existing_email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists. Please update properly.")
     
        if "password" in update_data:
            update_data["password"] = hashing.Hash.bcrypt(update_data["password"])
     
        stmt = update(models.User).where(models.User.id == id).values(**update_data)
        await db.execute(stmt)
        await db.commit()

        updated_result = await db.execute(select(models.User).filter(models.User.id == id))
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

async def deleteuser(id:str,db:AsyncSession):
    try:
            result = await db.execute(select(models.User).filter(models.User.id == id))
            user=result.scalars().first()
            if not user:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not Found")   
            stmt=(delete(models.User).where(models.User.id == id))
            await db.execute(stmt)
            await db.commit()
            user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role":user.role,
            "number":user.number
            # Add other fields as needed
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