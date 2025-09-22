from models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.product_schemas import ProductOut
from typing import List

async def get_all_product(db:AsyncSession) -> List[ProductOut]:
    """Показывет все товары которые есть в програме 

    Args:
        db (AsyncSession): Асинхронная сессяи для запросов на бд

    Returns:
        List[ProductOut]: Список всех товаров 
    """
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return [ProductOut.model_validate(u) for u in products]