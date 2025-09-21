from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from models.product import Product
from schemas.product_schemas import ProductOut


async def get_products_by_title(title:str, db:AsyncSession) -> list[ProductOut]:
    """ Искать товар по названию

    Args:
        title (str): назване товара
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Returns:
        list[ProductOut]: списко твраов которые ты искал или похшжие 
    """
    if not title.strip():
        return []
    stmt  = select(Product).where(Product.name.ilike(f"%{title.strip()}%")).order_by(desc(Product.created_at))
    result = await db.execute(stmt)
    products = result.scalars().all()
    
    return [ProductOut.model_validate(p) for p in products]
