from fastapi import APIRouter, Depends
from services.permission import requered
from models.user import User
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from enums import Role
from cruds.admin_cruds.user import get_users


api_route = APIRouter()

@api_route.get("/get_users")
async def get_all_users_route(db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN))):

    users = await get_users.get_all_users(db)

    return users