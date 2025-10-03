from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.user import User
from models.product import Product
from models.order import Order, OrderItem
from schemas.stats import SellerSales, AdminState
from sqlalchemy.orm import selectinload


async def get_admin_stats(db:AsyncSession) -> AdminState:
    """ Статистика програмы для админа 

    Args:
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Returns:
        AdminState: Статистики програмы
    """

    result = await db.execute(select(func.count()).select_from(Order))
    total_orders = result.scalar() or 0

    result = await db.execute(select(func.sum(Order.price)).where(Order.status.in_(['PAID', "PENDING"])))
    total_revenue = result.scalar() or 0.0

    result = await db.execute(select(User.id, User.username, func.count().label("total_order"))
                              .join(Product, Product.user_id == User.id)
                              .join(OrderItem, OrderItem.product_id == Product.id)
                              .join(Order, Order.id == OrderItem.order_id)
                              .group_by(User.id, User.username))
    
    rows = result.all()

    sales_by_seller = [SellerSales(seller_id = r[0],seller_name = r[1], total_sales = r[2]) for r in rows]

    return AdminState(
        total_order=total_orders,
        total_revenue=float(total_revenue),
        sales_by_saller=sales_by_seller
    )