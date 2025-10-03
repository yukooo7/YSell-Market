from fastapi import APIRouter, Depends
from models.user import User
from cruds.buyyer_crud.add_to_card import add_cart
from services.permission import requered
from schemas.cart import CreateCart
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from enums import Role

buyyer_route = APIRouter()

@buyyer_route.post("/add_cart")
async def add_cart_route(data_cart:CreateCart, db:AsyncSession = Depends(get_db), user:User = Depends(requered(Role.SHOPPER,Role.SELLER, Role.ADMIN))):

    order = await add_cart(data_cart, db, user)

    return order