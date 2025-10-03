from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from cruds.admin_cruds.user import delete
from services.permission import requered
from enums import Role

api_route = APIRouter()

@api_route.delete("/delete_user/{deleted_user}")
async def delete_user_route(deleted_user:int, db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN))):

    await delete.delete_user(deleted_user, db)
    
    return {"Удаление успешно"}