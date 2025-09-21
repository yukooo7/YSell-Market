from fastapi import APIRouter, Depends 
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.permission import requered
from enums import Role
from models.user import User
from cruds.buyyer_crud.get_cart import get_all_cart, get_order_detail, orders_hitory

buyyer_route = APIRouter()

@buyyer_route.get("/get_all_carts")
async def get_all_carts_route(user:User = Depends(requered(Role.SHOPPER)), db:AsyncSession = Depends(get_db)):

    carts = await get_all_cart(user, db)

    return carts

@buyyer_route.get("/get_order_detail/{order_id}")
async def get_order_detail_route(order_id:int, user:User = Depends(requered(Role.SHOPPER)), db:AsyncSession = Depends(get_db)):

    order = await get_order_detail(order_id, user, db)

    return order

@buyyer_route.get("/get_orders_history")
async def order_history_route(user:User = Depends(requered(Role.SHOPPER)), db:AsyncSession = Depends(get_db)):

    orders = await orders_hitory(user, db)

    return orders