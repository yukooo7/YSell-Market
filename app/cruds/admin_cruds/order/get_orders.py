from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.order import Order, OrderItem
from schemas.order import OrderOut
from typing import List
from sqlalchemy.orm import selectinload

async def get_all_orders(db:AsyncSession) -> List[OrderOut]:
    """Показывает все заказы которые были выполнеы 

    Args:
        db (AsyncSession): Асинхронная использование бд

    Returns:
        List[OrderOut]: Список всех заказов
    """
    stmt = select(Order).options(selectinload(Order.user),
                                 selectinload(Order.items).selectinload(OrderItem.product))
    result = await db.execute(stmt)
    orders = result.scalars().all()

    return [OrderOut.model_validate(o) for o in orders]