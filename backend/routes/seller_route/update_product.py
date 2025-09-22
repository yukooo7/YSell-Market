from fastapi import APIRouter, Depends 
from database import get_db
from services.permission import requered
from enums import Role
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.seller_crud.update_product import update_product
from models.user import User
from schemas.product_schemas import ProductUpdate

product_route = APIRouter()

@product_route.patch("/product_update/{product_id}")
async def update_product_route(product_id:int, data:ProductUpdate, db:AsyncSession = Depends(get_db), user:User = Depends(requered(Role.SELLER))):

    product = await update_product(product_id, data, db, user)

    return product