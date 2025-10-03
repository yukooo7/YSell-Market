from fastapi import FastAPI, Depends, APIRouter, Query
from cruds.goest.get_products_by_t import get_product_by_title
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.product_schemas import ProductOut
from typing import List

guest_route = APIRouter()

@guest_route.get("/product/search", response_model=List[ProductOut])
async def get_pr(title:str = Query(..., description="Название товара"), db:AsyncSession = Depends(get_db)):

    pro = await get_product_by_title(title ,db)

    return  pro