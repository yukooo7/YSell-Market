from fastapi import Depends, APIRouter
from cruds.admin_cruds import stats
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from services.permission import requered
from enums import Role


api_route = APIRouter()

@api_route.get('/stats')
async def get_admin_state_route(db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN))):
    
    statics = await stats.get_admin_stats(db)

    return statics

