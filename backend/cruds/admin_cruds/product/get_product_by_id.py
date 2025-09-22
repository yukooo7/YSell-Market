from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from schemas.product_schemas import ProductOut


async def get_product(product_id:int, db:AsyncSession) -> ProductOut:
    """Показывает  товары по ID 

    Args:
        product_id (int): ID товраа которого хотите найти 
        db (AsyncSession): Асинхронная сессия для запроса б база данных

    Raises:
        HTTPException: 404 если ненайден товар 

    Returns:
        ProductOut: Показывает товар которого искали
    """

    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    return ProductOut.model_validate(product)