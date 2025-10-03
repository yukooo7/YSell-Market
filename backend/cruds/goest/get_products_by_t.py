from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.product import Product
from schemas.product_schemas import ProductOut
from typing import List

async def get_product_by_title(title:str, db:AsyncSession) -> List[ProductOut]:

    result = await db.execute(select(Product).where(Product.name.ilike(f'%{title.strip()}%')))
    if not title.strip():
        return []
    products = result.scalars().all()
    

    return [ProductOut.model_validate(p) for p in products]