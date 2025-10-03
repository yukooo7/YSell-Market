from fastapi import HTTPException
from models.cart import BusketCart
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from sqlalchemy.future import select

# удалениеп по айди 
async def delete_cart(cart_id:int, db:AsyncSession, user:User):
    """ Удаление товра и карзиный

    Args:
        cart_id (int): Айди товра из корзщины
        db (AsyncSession): Ассинхронна сессия для запросов на бд
        user (User): depends Для ролучение доступа


    Returns:
        str: сообшение о успешном удаление 
    """
    exist_cart = await db.get(BusketCart,  cart_id)

    if not exist_cart:
        raise HTTPException(status_code=404, detail="Товар с таким id нет в карзине")
    
    if exist_cart.user_id != user.id:
        raise HTTPException(status_code=403, detail="Вы не в праве удаить пользователя ")


    await db.delete(exist_cart)
    await db.commit()

    return {"Удаление Успешно"}


# Полное удаление карзины

async def delete_all_cart(db:AsyncSession, user:User):
    """ Очиска Карзины

    Args:
        db (AsyncSession): Ассинхронна сессия для запросов на бд
        user (User): Depends

    Raises:
        HTTPException: 404 если карзина пуста

    Returns:
        str:  Cообшение об успешной очиске карзины
    """

    result = await db.execute(select(BusketCart).where(BusketCart.user_id == user.id))
    exist_carts = result.scalars().all()

    if not exist_carts:
        raise HTTPException(status_code=404, detail="Карзина пуста")
    
    for cart_item in exist_carts:
        await db.delete(cart_item)

    await db.commit()

    return {"Удаление Успешно"}
