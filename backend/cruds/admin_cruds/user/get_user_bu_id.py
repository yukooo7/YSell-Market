from fastapi import HTTPException
from models.user import User
from schemas.user import UserOut
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_id(user_id:int, db:AsyncSession) -> UserOut:
    """Поиск пользовтеля по ID для админа 

    Args:
        user_id (int): ID Пользователя которого хотите найти 
        db (AsyncSession): Ассинхронная сессия для запросов в бд

    Raises:
        HTTPException: 404 если пользовател не найден

    Returns:
        UserOut: Ползоател которого нашли
    """

    user_exist = await db.get(User, user_id)

    if not user_exist:
        raise HTTPException(status_code=404, detail="Пльзователь не наайден")
    
    return UserOut.model_validate(user_exist)