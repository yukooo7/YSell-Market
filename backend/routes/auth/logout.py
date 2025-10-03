from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.auth_crud.logout import logout_c
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



api_route = APIRouter()

@api_route.post('/logout')
async def logout_route(token_str:str = Depends(oauth2_scheme),db:AsyncSession = Depends(get_db),):

    await logout_c(token_str, db)
    return {"message": "Успешный выход"}