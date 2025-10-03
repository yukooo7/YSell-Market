from fastapi import HTTPException
from models.user import User
from schemas.user import UserOut, ProfileUpdate, PasswordUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from services.password_function import hash_password, check_password


async def get_me(user:User) -> UserOut:
    """Личны кабинет или профил тоест данные о себе

    Args:
        user (User): Depends

    Returns:
        UserOut: Данные о себе
    """

    return UserOut.model_validate(user)

async def upgrade_profile(user_data:ProfileUpdate, user:User, db:AsyncSession) -> UserOut:
    """Изменить профил можно частично 

    Args:
        user_data (ProfileUpdate): даныве на котрох хочешь менять 
        user (User):  depends
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Raises:
        HTTPException: 500 если ошибка при изменение

    Returns:
        UserOut: Изменненый профил
    """
   
    for k, v in user_data.items():
        setattr(user, k, v)
    try:
        await db.commit()
        await db.refresh(user)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return UserOut.model_validate(user)


async def update_pasaword(data:PasswordUpdate, user:User, db:AsyncSession):
    """ изменяеть пароль

    Args:
        data (PasswordUpdate): New and old password
        user (User): dpends
        db (AsyncSession):  Ассинхронна сессия для запросов на бд


    Raises:
        HTTPException: 401 если не верный пароль
        HTTPException: 500 если ошибка при изминение

    Returns:
        str: Сообшение об успешном обнавление паролья
    """
    
    try:
        if not check_password(data.old_password , user.password):
            raise HTTPException(401, detail="Не правельный пароль")
        hashed_password = hash_password(data.new_password)
        user.password = hashed_password

        await db.commit()
        await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Не удлось поменять пароль {e}")
    return {"message":"Пароль успешно изменень"}
    
