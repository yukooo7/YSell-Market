from fastapi import HTTPException, Depends
from models.order import Order
from schemas.order import  MessageDelete
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from enums import Role
from services.permission import requered


async def delete_order(order_id:int, db:AsyncSession) -> MessageDelete:
    """Удаление заказа может только админ

    Args:
        order_id (int): Id закза коорого хотим удалить 
        db (AsyncSession): Асинхронная использование базы данных


    Returns:
        MessageDelete: Успешное удаление товара
    """

    order = await db.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail='Заказ не найден')
    
    try:
        db.delete(order)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return MessageDelete(message="Заказ успешно удалень")