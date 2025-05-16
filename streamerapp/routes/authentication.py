from fastapi import APIRouter ,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from ..import database,oauth2,schemas
from sqlalchemy.ext.asyncio import AsyncSession
from ..repository import authenticationrepository


router = APIRouter(
    tags=['authentication']
)

@router.post("/login",status_code = status.HTTP_200_OK)
async def loginuser (request:OAuth2PasswordRequestForm = Depends(),db:AsyncSession = Depends(database.get_async_db)):
    return await  authenticationrepository.loginuser(request,db)

@router.post('/refereshToken', status_code=status.HTTP_200_OK)
async def refereshtoken(referesh_token:str,db:AsyncSession = Depends(database.get_async_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await authenticationrepository.refereshtokens(referesh_token,db)
   
@router.post('/logout',status_code=status.HTTP_200_OK)
async def logoutuser(token:str = Depends(oauth2.oauth2_scheme),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return await authenticationrepository.logoutuser(token)