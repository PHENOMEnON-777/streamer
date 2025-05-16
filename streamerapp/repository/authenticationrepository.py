from fastapi import status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from .. import models,hashing,jwtToken
from jose import JWTError
from sqlalchemy.future import select
from datetime import timedelta 
from ..jwtToken import create_access_token,create_referesh_token,verify_token


from core.config import get_settings

settings = get_settings()



async def loginuser(request:OAuth2PasswordRequestForm, db:AsyncSession):
    try:
        result = await db.execute(select(models.User).filter(models.User.email == request.username))
        user =  result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='invalid cridentials')
        if not hashing.Hash.verify(user.password,request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='incorrect password')

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email,"id": user.id},expires_delta = access_token_expires)
        referesh_token = create_referesh_token(data={"sub":user.email,"id":user.id},)
        return {"access_token" : access_token,"referesh_token":referesh_token, "token_type" : "bearer","success":True,"msg":"loged in successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"An error occurred: {str(e)}"
        )

async def refereshtokens(referesh_token:str,db:AsyncSession):
    try:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        payload= jwtToken.verify_token(referesh_token,credentials_exception)
        user_id = payload.id
        if not user_id:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid referesh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
        result = await db.execute(select(models.User).filter(models.User.id == user_id))
        user = result.scalars().first()  
        if not user:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid referesh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email,"id": user.id},expires_delta = access_token_expires)
        referesh_token = create_referesh_token(data={"sub":user.email,"id":user.id},)
        return {"access_token" : access_token,"referesh_token":referesh_token, "token_type" : "bearer"}
    except JWTError:
        raise credentials_exception
        
        
async def logoutuser(token:str):
    try:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        payload= jwtToken.verify_token(token,credentials_exception)
        return {"msg":"Logged Out Successfully","success":True,"data":""}
    except JWTError:
        raise credentials_exception
        