
from fastapi import HTTPException
from models.cart import BusketCart
from models.order import Order, OrderItem 
from sqlalchemy.ext.asyncio import AsyncSession
from enums import OrderStatus
from models.user import User
from sqlalchemy.future import select

async def create_order(user: User, db: AsyncSession):
    """ Создание заказа по карзине 

    Args:
        user (User): Depends
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Raises:
        HTTPException: 404 если карзина пуста 
        HTTPException: 500 если ошибка при создания заказа

    Returns:
        str: Айди саказа и сколькок оплате 
    """

    stmt = select(BusketCart).where(BusketCart.user_id == user.id)
    result = await db.execute(stmt)
    cart_items = result.scalars().all()
    
    if not cart_items:
        raise HTTPException(status_code=404, detail="Корзина пуста")
    
    total_price = sum(item.price_with_discount * item.quantity for item in cart_items)

    new_order = Order(
        user_id=user.id,
        price=total_price,
        status=OrderStatus.PENDING
    )
    try:
        db.add(new_order)
        await db.flush()

        for item in cart_items:
            if item.product_id is None:
                await db.delete(item)
                continue
            
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_to_purchase=item.price_with_discount
            )
            db.add(order_item)
            await db.delete(item)

        await db.commit()
        await db.refresh(new_order)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Не удалось создать заказ: {e}")

    return {"message": f"Заказ {new_order.id} успешно создан. К оплате: {total_price}"}