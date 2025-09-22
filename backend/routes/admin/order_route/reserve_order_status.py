from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from enums import Role
from cruds.admin_cruds.order.reserve_status import reserve_order_status
from sqlalchemy.ext.asyncio import AsyncSession 
from services.permission import requered 
from schemas.order import  StatusUpdate
from database import get_db


api_route = APIRouter()

@api_route.patch("/reserve_order_status/{order_id}")
async def reserve_orders_status_route(order_id:int, new_data:StatusUpdate, db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN))):
    
    return await reserve_order_status(order_id, new_data, db)
