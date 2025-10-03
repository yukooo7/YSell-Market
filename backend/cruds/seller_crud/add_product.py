from models.product import Product
from schemas.product_schemas import ProductCreate, ProductOut
from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from typing import Optional

async def add_product(data:ProductCreate, image_url: Optional[str], db:AsyncSession, user:User):
    """ Добавлени  продукта

    Args:
        data (ProductCreate): Данные продукта
        db (AsyncSession): Ассинхронна сессия для запросов на бд
        user (User): depends

    Raises:
        HTTPException: 500 если при создание товра ошибка

    Returns:
        Product: Созданный продукт 
    """


    new_product = Product(
        name = data.name,
        price = data.price,
        category = data.category,
        user_id = user.id,
        stock = data.stock,
        image_url = image_url
    )
    try:
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return ProductOut.model_validate(new_product)
