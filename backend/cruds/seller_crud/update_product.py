from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from schemas.product_schemas import ProductOut, ProductUpdate
from fastapi import HTTPException
from models.user import User



async def update_product(product_id:int, new_data:ProductUpdate, db:AsyncSession, user:User):
    """ измение товаров можно частично

    Args:
        product_id (int): айди прродукт а которого хотите изменить
        new_data (ProductUpdate): новые данные
        db (AsyncSession): Ассинхронная сессия для запросов на бд
        user (User):  depends

    Raises:
        HTTPException: 404 если продукт не найден
        HTTPException: 401 нет правл не ваш товар
        HTTPException: 500 при изминениее товра произошло ошиька

    Returns:
        _type_: _description_
    """

    product_exist = await db.get(Product, product_id)

    if not product_exist:
        raise HTTPException(status_code=404, detail="Продукт с таким Id не найден")
    if product_exist.user_id != user.id:
        raise HTTPException(status_code=401, detail="У вас нет прав обнавитэтот товар ")


    for k, v in new_data.items():
        setattr(product_exist, k, v)

    try:
        await db.commit()
        await db.refresh(product_exist)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"При обнавление товара была ошибка {e}")

    return ProductOut.model_validate(product_exist)