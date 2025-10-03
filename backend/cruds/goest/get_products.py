from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.product import Product
from typing import List
from schemas.product_schemas import ProductOut

async def get_all_products(db:AsyncSession) -> List[ProductOut]:

    result = await db.execute(select(Product))
    products = result.scalars().all()
    
    return [ProductOut.model_validate(p) for p in products]