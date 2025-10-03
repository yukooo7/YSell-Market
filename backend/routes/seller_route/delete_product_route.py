from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from enums import Role
from services.permission import requered
from cruds.seller_crud.delete_product import delete_products
from models.user import User


product_route = APIRouter()

@product_route.delete("/product/{product_id}")
async def delete_product_route(product_id:int, db:AsyncSession = Depends(get_db),
                               user:User = Depends(requered(Role.SELLER))):
    
    product = await delete_products(product_id, db, user)

    return product