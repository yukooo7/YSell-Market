from fastapi import HTTPException
from models.user import User
from schemas.user import UserOut, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession

async def update_user_crud(user_id:int,new_user: UserUpdate, db:AsyncSession)-> UserOut:
    """ Изменить пользоваеля только для админа

    Args:
        user_id (int): ID Пользовтелья 
        new_user (UserUpdate): Новые данные пользователя
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Raises:
        HTTPException: 404 если пользовател не найден
        HTTPException: 500 если ошибка при изминение

    Returns:
        UserOut: Новый пользовтал которог изменили 
    """

    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    

    update_data = new_user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        await db.commit()
        await db.refresh(user)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return UserOut.model_validate(user)
