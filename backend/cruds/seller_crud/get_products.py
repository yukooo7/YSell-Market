from models.product import Product
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from schemas.product_schemas import ProductOut


async def get_product(user:User, db:AsyncSession) -> list[ProductOut]:
    """ Показывает все товары этого пользовател

    Args:
        user (User): Depends
        db (AsyncSession): "message": "Продукт успешно удален"

    Returns:
        list[ProductOut]: Список товраров
    """

    stmt = select(Product).where(Product.user_id == user.id).order_by(desc(Product.created_at))
    result = await db.execute(stmt)
    products = result.scalars().all()

    return [ProductOut.model_validate(p)for p in products]

    