from fastapi import HTTPException
from models.cart import BusketCart
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from models.order import Order, OrderItem
from schemas.order import OrderOut
from sqlalchemy.orm import selectinload
from schemas.cart import CartOut
from  typing import List


async def get_all_cart(user:User, db:AsyncSession) -> List[CartOut]:
    """ Показывает все товраы которые добавил в карзину

    Args:
        user (User): Depends
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Raises:
        HTTPException: 404 если карзина пуста

    Returns:
        List: Все товары которы добавил в карзину
    """

    result = await db.execute(select(BusketCart).where(BusketCart.user_id == user.id).options(selectinload(BusketCart.product), selectinload(BusketCart.user)))
    exist_carts = result.scalars().all()

    if not exist_carts:
        raise HTTPException(status_code=404, detail="Карзина товаров пуста")
    
    return [CartOut.model_validate(c) for c in exist_carts]



async def get_order_detail(order_id:int, user:User, db:AsyncSession) -> OrderOut:
    """ показывает детали ордера

    Args:
        order_id (int): айди ордера
        user (User): DEPEnds
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Raises:
        HTTPException: 404 если ордлер не наден
        HTTPException: 403 если не прав нап просмотр ордера

    Returns:
        OrderOut: подробномти ордера
    """

    stmt = select(Order).options(
        selectinload(Order.user), selectinload(Order.items).selectinload(OrderItem.product)
    ).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="У вас нету права посматрет этот заказ")
    return OrderOut.model_validate(order)
    


async def orders_hitory(user:User, db:AsyncSession) -> list[OrderOut]:
    """
    История закзаов

    Args:
        user (User): Depends
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Returns:
        list[OrderOut]: Истории зказов
    """

    stmt = select(Order).options(selectinload(Order.user), selectinload(Order.items).selectinload(OrderItem.product)).where(Order.user_id == user.id)
    result = await db.execute(stmt)
    history = result.scalars().all()

    if not history:
        return []
    return [OrderOut.model_validate(o) for o in history]