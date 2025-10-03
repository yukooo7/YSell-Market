from schemas.login import ResponseLogin, RequestToken
from fastapi import HTTPException
from sqlalchemy.sql import select
from models.user import User
from services.password_function import check_password
from services.utilits_token import create_access_token, create_refersh_token
from sqlalchemy.ext.asyncio import AsyncSession

async def login(data:ResponseLogin, db:AsyncSession) -> RequestToken:
    """ Логин 

    Args:
        data (ResponseLogin): Еmail and password 
        db (AsyncSession): Ассинхронна сессия для запросов на бд

    Raises:
        HTTPException: 400 если не коректны емали или пароль

    Returns:
        RequestToken: Access, refresh, token Type
    """
    
    user_email = data.email.lower().strip()
    stmt = select(User).where(User.email == user_email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=400, detail="Введен не кректный email повторите попытку")
    


    if not check_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Введень не правелььный пароль")
    
    payload = {"sub":str(user.id), "role": user.role}
    access_token  = create_access_token(payload)
    refresh_token  = create_refersh_token(payload)

    return RequestToken(access_token=access_token, refresh_token=refresh_token, token_type='bearer')

