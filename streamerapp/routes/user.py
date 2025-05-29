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

@router.get('/getUserById',status_code=status.HTTP_200_OK,response_model= schemas.ResponseWrapper[schemas.ShowUser],)
async def get_user_byId(db:AsyncSession=Depends(database.get_async_db),current_user:schemas.User= Depends(oauth2.get_current_user)):
 return await userrepository.getuserbyid(db,current_user)

@router.put('/updateUserInfo',status_code=status.HTTP_200_OK,response_model= schemas.ResponseWrapper[schemas.ShowUser],)
async def updateuser(request:schemas.User,db:AsyncSession=Depends(database.get_async_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
 return await userrepository.updateuser(request,db,current_user)