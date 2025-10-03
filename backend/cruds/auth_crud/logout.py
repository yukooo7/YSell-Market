from sqlalchemy.ext.asyncio import AsyncSession
from models.token_blakclist import TokenBlackList
from fastapi import HTTPException, status
from sqlalchemy.future import select

async def logout_c(token_string: str, db: AsyncSession):
    """ Выход из профиля 

    Args:
        token_string (str): токен пользовтаеля он егно получает через depends
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Raises:
        HTTPException: 401 есили уже токен пользователя не валиден
        HTTPException: 500 если ошибка при логоут 
    """
    # Проверяем, не был ли токен уже занесён в черный список
    stmt = select(TokenBlackList).where(TokenBlackList.token == token_string)
    result = await db.execute(stmt)
    existing_entry = result.scalar_one_or_none()
    
    if existing_entry:
        raise HTTPException(
            status_code=401, 
            detail="Токен уже недействителен"
        )
    
    # Создаем новую запись и добавляем в неё строку токена
    new_blacklist_entry = TokenBlackList(token=token_string)
    
    try:
        db.add(new_blacklist_entry)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Не удалось занести токен в черный список: {str(e)}"
        )