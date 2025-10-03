from fastapi import Depends,APIRouter, Request
from database import get_db
from services.permission import requered
from enums import Role
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from cruds.admin_cruds.user.get_user_bu_id import get_user_by_id
from schemas.user import UserOut


api_route = APIRouter()

@api_route.get("/get_user_by_id/{user_id}")
async def get_user_route(user_id:int, db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN)), request:Request = None):

    user = await get_user_by_id(user_id, db)

    return user
    