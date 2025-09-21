from fastapi import HTTPException
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_user(deleted_user:int, db:AsyncSession):
    """Удалнеи пользоватлнй только для админа

    Args:
        deleted_user (int): ID пользователть которого хотите удлить 
        db (AsyncSession): Ассинхронная сессия для запросов в бд

    Raises:
        HTTPException: 404 если пользовател не найден
        HTTPException: 500 если во аремя удаление произошло ошибка 

    Returns:
        str: Собшение про успешное удаление
    """
    user = await db.get(User, deleted_user)
    if not user:
        raise HTTPException(status_code=404, detail="Токой пользователь не сушествует")

    try:
        await db.delete(user)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Пользоватеь успешно удалён"}

