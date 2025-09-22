from fastapi import HTTPException
from models.order import Order, OrderItem
from schemas.order import OrderOut, StatusUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload



async def reserve_order_status(order_id:int,new_status:StatusUpdate,  db:AsyncSession) -> OrderOut:
    """Изменение статуса товара 

    Args:
        order_id (int): ID ордера котого хотим изменить 
        new_status (StatusUpdate): Новый статус на которого хотим изменить 
        db (AsyncSession): асинхронна исп бд

    Returns:
        OrderOut: Заказа если измениося успешно 
    """
    
    stmt = select(Order).options(
        selectinload(Order.user),
        selectinload(Order.items),
        selectinload(Order.items).selectinload(OrderItem.product)
    ).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    order.status = new_status.status

    try:
        await db.commit()
        await db.refresh(order)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return OrderOut.model_validate(order)
    