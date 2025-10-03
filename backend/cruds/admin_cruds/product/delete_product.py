from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product



async def delete_product(product_id:int,db:AsyncSession):
    """Удаление товра для админа

    Args:
        product_id (int): ID Товра которого хотим удалить
        db (AsyncSession): АКсинхронна сессия для запроса в бд

    Returns:
        str: Удаление товра успешно
    """
    product = await db.get(Product, product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    try:
        db.delete(product)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message":"Удаление продукта успешна"}