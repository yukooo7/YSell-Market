from sqlalchemy.ext.asyncio import AsyncSession
from models.sale import Sale
from schemas.sale import SaleCreate, SaleOut
from fastapi import HTTPException
from models.product import Product
from models.user import User

async def create_sale(data:SaleCreate, db:AsyncSession, user:User) -> SaleOut:
    """ Создание скидки для товара 

    Args:
        data (SaleCreate): процент и айди продукта
        db (AsyncSession): Ассинхронна сессия для запросов на бд
        user (User): depends

    Raises:
        HTTPException: 404 если товар не найден 
        HTTPException: 401 если нет прав тоесть не ваш товар
        HTTPException: 500 если при создание скидки ошибка

    Returns:
        SaleOut: Данные про скидку
    """
    product_exist = await db.get(Product, data.product_id)
    if not product_exist:
        raise HTTPException(status_code=404, detail="Продукт с таким id не сушествует")
    
    if product_exist.user_id != user.id:
        raise HTTPException(status_code=401,detail="У вас нет права создать скику для этого товара")
    
    product_exist.discount_percent = data.percent
    new_sale = Sale(
        title = data.title,
        product_id = data.product_id,
        percent =data.percent
    )

    try:
        db.add(product_exist)
        db.add(new_sale)
        await db.commit()
        await db.refresh(new_sale)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return SaleOut.model_validate(new_sale)
