from fastapi import APIRouter, Depends
from models.user import User 
from cruds.seller_crud.create_sale import create_sale
from services.permission import requered
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.sale import SaleCreate
from enums import Role

product_route = APIRouter()

@product_route.post("/create_sale")
async def create_sale_route(data:SaleCreate, db:AsyncSession= Depends(get_db), user:User = Depends(requered(Role.SELLER))):

    sale = await create_sale(data, db, user)

    return sale