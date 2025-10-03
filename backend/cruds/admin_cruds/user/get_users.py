from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserOut
from typing import List
from sqlalchemy.future import select
async def get_all_users(db:AsyncSession) -> List[UserOut]:
    """ Показывает всех пользовтаел програмы только для админа

    Args:
        db (AsyncSession): Ассинхронная сессия для запросов в бд

    Returns:
        List[UserOut]: Список пользователей
    """

    result  = await db.execute(select(User))
    users = result.scalars().all()

    return [UserOut.model_validate(i) for i in users]