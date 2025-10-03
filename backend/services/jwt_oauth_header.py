from fastapi.security import OAuth2PasswordBearer
from services.utilits_token import decode_token
from models.user import User
from models.token_blakclist import TokenBlackList
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy.sql import select
from jose import JWTError


# Извлекаем токен из загловка Authiretion а tokenUrl это путь в нашем случаи это роут Login
# Он ишет токен в заголовке 
oauth2_schemas = OAuth2PasswordBearer(tokenUrl="/auth/login")


# фунция проверяет токен пользователя если он не BlacklistToken то он выводит payload(user_id, email)
async def get_current_tokken(token:str = Depends(oauth2_schemas), db:AsyncSession = Depends(get_db)):
    """Провеяем подлинность токена если он правельный то
       декодирум и проерям по id еслт такой пользоател в нашем таблице в бд

    Args:
        token (str, optional): token. Defaults to Depends(oauth2_schemas).
        db (AsyncSession, optional): async bd. Defaults to Depends(get_db).

    Raises:
        exeption_401: _description_
        exeption_401: _description_
        exeption_401: _description_
        exeption_401: _description_

    Returns:
        dict: payloa(user)
    """

    # Мы создаем ошибку в перемеоой чтобы не повторять кажый раз
    exeption_401 = HTTPException(status_code=401, detail="Не удалось проверить учетныю запись")

    # Мы ишем в таблице TokenBlacklist токен которого хотим получить данные
    # Это допалнительное проверка нато что на токен не в черном сиске тоесть он на 100% правельный
    stmt = select(TokenBlackList).where(TokenBlackList.token == token)
    result = await db.execute(stmt)
    blacklist_token = result.scalar_one_or_none()


    # Поверяем если есть то выдаем ошикбку котору создали ранее
    if blacklist_token:
        raise HTTPException(status_code=401, detail="A")
    

    # Самое главна  часть мы декодирум на токен чтбы мы могли проверить етсть ли на сомом деле 
    # такой пользоваель на бд 
    try:
        payload =  decode_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="h")
    except JWTError:
        raise HTTPException(status_code=401, detail="j")
    

    user_id = int(payload.get("sub"))
    if not user_id:
        raise HTTPException(status_code=401, detail="o")

    


    # Проверяем есть ли пользоветль с таким id
    stmt = select(User).where(User.id == int(user_id))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="p")

    return user        