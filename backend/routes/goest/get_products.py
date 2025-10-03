from fastapi import Depends, HTTPException, APIRouter
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from schemas.product_schemas import ProductOut
from typing import List
from cruds.goest.get_products import get_all_products


guest_route = APIRouter()

@guest_route.get("/products", response_model=List[ProductOut])
async def get_products_route(db:AsyncSession = Depends(get_db)):

    product = await get_all_products(db)

    return product