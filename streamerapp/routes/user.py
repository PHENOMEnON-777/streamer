from fastapi import APIRouter,Depends,status
from streamerapp import oauth2
from .. import schemas,database 
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import userrepository

router = APIRouter(
    tags=['user']
)

@router.post('/createuser',status_code=status.HTTP_201_CREATED,response_model= schemas.ResponseWrapper[schemas.ShowUser],)
async def create_user(request:schemas.User,db:AsyncSession = Depends(database.get_async_db),):
 return await userrepository.create(request,db)

@router.get('/getallUsers',status_code=status.HTTP_200_OK,response_model=schemas.ResponseWrapper[list[schemas.ShowUser]])
async def getallusers(db:AsyncSession = Depends(database.get_async_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return await userrepository.getallusers(db,current_user)


@router.get('/getallUsersformobile',status_code=status.HTTP_200_OK,response_model=schemas.ResponseWrapper[list[schemas.ShowUser]])
async def getallusers(db:AsyncSession = Depends(database.get_async_db),):
    return await userrepository.getallusersformobile(db,)

@router.get('/getUserById',status_code=status.HTTP_200_OK,response_model= schemas.ResponseWrapper[schemas.ShowUser],)
async def get_user_byId(db:AsyncSession=Depends(database.get_async_db),current_user:schemas.User= Depends(oauth2.get_current_user)):
 return await userrepository.getuserbyid(db,current_user)

@router.put('/updateUserInfobyId/{id}',status_code=status.HTTP_200_OK,response_model= schemas.ResponseWrapper[schemas.ShowUser],)
async def updateuser(request:schemas.User,id, db:AsyncSession=Depends(database.get_async_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
 return await userrepository.updateuser(request,id,db,current_user)

@router.delete('/deletuserbyId/{id}',status_code=status.HTTP_200_OK,response_model= schemas.ResponseWrapper[schemas.ShowUser],)
async def deleteuser(id, db:AsyncSession=Depends(database.get_async_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
 return await userrepository.deleteuser(id,db,)