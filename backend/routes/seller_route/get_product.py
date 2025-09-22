from fastapi import APIRouter, Depends 
from database import get_db
from services.permission import requered
from enums import Role
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.seller_crud.get_products import get_product
from models.user import User

product_route = APIRouter()

@product_route.get("/get_product")
async def get_all_products_route(user:User = Depends(requered(Role.SELLER)), db:AsyncSession = Depends(get_db)):

    products = await get_product(user, db)

    return products