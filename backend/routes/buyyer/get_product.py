from fastapi import APIRouter, Depends, Query
from cruds.buyyer_crud.get_products import get_products_by_title
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


buyyer_route = APIRouter()

@buyyer_route.get("/products/search")
async def get_product_route(title:str = Query(..., description="Название товара..."), db:AsyncSession = Depends(get_db)):


    return await get_products_by_title(title, db)