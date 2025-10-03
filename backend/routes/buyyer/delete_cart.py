from fastapi import APIRouter, Depends
from database import get_db
from services.permission import requered
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from enums import Role
from cruds.buyyer_crud.delete_cart import delete_cart, delete_all_cart

buyyer_route = APIRouter()

@buyyer_route.delete("/delete_cart/{cart_id}")
async def delete_cart_route(cart_id:int, db:AsyncSession = Depends(get_db), user:User = Depends(requered(Role.SHOPPER))):

    cart = await delete_cart(cart_id, db, user)

    return cart

@buyyer_route.delete("/delete_all_carts")
async def delete_all_carts_route(db:AsyncSession = Depends(get_db), user:User = Depends(requered(Role.SHOPPER))):

    carts = await delete_all_cart(db, user)
    return carts