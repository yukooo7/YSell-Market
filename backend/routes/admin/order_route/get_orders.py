from fastapi import APIRouter,Depends, HTTPException
from database import get_db
from cruds.admin_cruds.order.get_orders import get_all_orders
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from services.permission import requered
from enums import Role


api_route = APIRouter()

@api_route.get('/get_all_orders')
async def get_all_orders_route(db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN))):

    orders = await get_all_orders(db)
    if not orders:
        raise HTTPException(status_code=401,detail="Не удалось показать списoк товаров")
    return orders