from models.product import Product
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.user import User


async def delete_products(product_id:int, db:AsyncSession, user:User):
    """ Удаление товара 

    Args:
        product_id (int): Айди продукта
        db (AsyncSession): Ассинхронна сессия для запросов на бд
        user (User): Depends

    Raises:
        HTTPException: 404 если продукт не найден
        HTTPException: 401 нет прав тоесть не ваш товар 
        HTTPException: 500 если при удаление ошибка

    Returns:
        "message": "Продукт успешно удален"
    """

    stmt = select(Product).where(Product.id == product_id)
    result = await db.execute(stmt)
    product_exist = result.scalar_one_or_none()

    if product_exist is None:
        raise HTTPException(status_code=404, detail=f'Продукт с таким id {product_id} не найден')

    if product_exist.user_id != user.id:
        raise HTTPException(status_code=401, detail="У вас нет прав удалить этот товар")
    
    await db.delete(product_exist)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Продукт успешно удален"}