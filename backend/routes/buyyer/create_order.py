from fastapi import APIRouter, Depends
from models.user import User
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from enums import Role
from services.permission import requered
from cruds.buyyer_crud.order_create import create_order

buyyer_route = APIRouter()

@buyyer_route.post("/cretae_order")
async def create_order_route(user:User = Depends(requered(Role.SHOPPER)), db:AsyncSession = Depends(get_db)):

    order = await create_order(user, db)

    return order