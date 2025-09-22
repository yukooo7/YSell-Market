from fastapi import APIRouter, Depends
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.admin_cruds.user import update_user
from enums import Role
from database import get_db
from schemas.user import UserUpdate
from services.permission import requered


api_route = APIRouter()

@api_route.patch("/update_user/{user_id}")
async def update_user_route(user_id:int, data:UserUpdate, db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN, Role.SELLER))):

    updated_user = await update_user.update_user_crud(user_id, data, db)

    return updated_user