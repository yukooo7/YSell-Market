from fastapi import HTTPException
from models.user import User
from models.product import Product
from models.cart import BusketCart
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.cart import CreateCart, CartOut
from sqlalchemy.future import select
from sqlalchemy import and_

async def add_cart(cart_data:CreateCart, db:AsyncSession, user:User) ->CartOut:
    """ Добавлоение товара в карзину 

    Args:
        cart_data (CreateCart): ID продукта и количество
        db (AsyncSession): Ассинхронна сессия для запросов на бд
        user (User): это Depends его не вводит пользовтель

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        CartOut: _description_
    """

    product = await db.get(Product, cart_data.product_id)
    if not product:
        raise HTTPException(status_code=404,detail="Продукт не найден")
    

    final_price = product.price
    if product.discount_percent and product.discount_percent > 0:
        final_price = product.price * (1 - product.discount_percent / 100)
        if final_price < 0:
            final_price = 0
            
    reslut = await db.execute(
        select(BusketCart).where(
        and_(BusketCart.product_id == cart_data.product_id,
        BusketCart.user_id == user.id
        ))
    )
    cart_exist = reslut.scalar_one_or_none()

    try:
        if cart_exist:
            cart_exist.quantity += cart_data.quantity
            await db.commit()
            await db.refresh(cart_exist)
            return CartOut.model_validate(cart_exist)
        else:
            new_cart = BusketCart(
                user_id = user.id,
                product_id = cart_data.product_id,
                quantity = cart_data.quantity,
                price_with_discount = final_price
            )
            db.add(new_cart)
            await db.commit()
            await db.refresh(new_cart)
            return CartOut.model_validate(new_cart)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))