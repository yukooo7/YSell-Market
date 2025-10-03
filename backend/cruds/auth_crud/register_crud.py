from sqlalchemy.ext.asyncio import AsyncSession
from services.password_function import hash_password, check_password
from models.user import User
from schemas.user import UserCreate, UserOut
from services import  utilits_token
from sqlalchemy.sql import select
from fastapi import HTTPException
from enums import Role


ALLOWED_ROLE_FOR_REGISTRATION = {Role.SELLER, Role.SHOPPER, Role.ADMIN}


async def register(data:UserCreate, db:AsyncSession) -> UserOut:
    """ Регистрация пользователя 

    Args:
        data (UserCreate): необходимые данные для регистрации
        db (AsyncSession): Ассинхронна сессия для запросов на бд


    Returns:
        UserOut: Новый юсер которы зрегался и его токены 
    """
    user_email = data.email.lower().strip()

    stmt = select(User).where(User.email == user_email)
    result = await db.execute(stmt)
    exist_user = result.scalar_one_or_none()

    if exist_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже сушествует!")
    

    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail='Пароль Должен быть не менее 8 символов')
    if len(data.password) > 64:
        raise HTTPException(status_code=400, detail="Пароль не может быть больше 64 символов")

    new_password = hash_password(data.password)


    if data.role is not None:
        if data.role not in ALLOWED_ROLE_FOR_REGISTRATION:
            raise HTTPException(status_code=403, detail="Не допустимы роль для регстрации")
        user_role = data.role
    else:
        user_role = Role.GUEST

    new_user = User(
        username = data.username,
        email = user_email,
        phone = data.phone,
        role = user_role,
        password = new_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token_data = {"sub": str(new_user.id), "role": str(new_user.role)}
    access_token = utilits_token.create_access_token(token_data)
    refresh_token = utilits_token.create_refersh_token(token_data)



    return {
        "user":UserOut.model_validate(new_user),
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
        }