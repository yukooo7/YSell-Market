from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Union

SECRET_KEY = "NEVERDONTSTOPBRO"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MIN = 60
REFRESH_TOKEN_EXPIRE_DAY = 7

def create_access_token(data: dict) -> str:
    """Создание access токена

    Args:
        data (dict): Данные пользователя, включая 'sub' (ID) и 'role'

    Returns:
        str: JWT access token
    """
    encode_to = data.copy()  # Копируем, чтобы не изменять исходные данные
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    encode_to.update({"exp": int(expire.timestamp())})
    token = jwt.encode(encode_to, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_refersh_token(data: dict) -> str:
    """Создание refresh токена

    Args:
        data (dict): Данные пользователя, включая 'sub' (ID)

    Returns:
        str: JWT refresh token
    """
    encode_to = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAY)
    encode_to.update({"exp": int(expire.timestamp())})
    token = jwt.encode(encode_to, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> Union[dict, None]:
    """Декодирование JWT токена

    Args:
        token (str): JWT токен

    Returns:
        Union[dict, None]: Payload токена или None при ошибке
    """
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODED PAYLOAD:", decode)
        return decode
    except JWTError as e:
        print("JWT DECODE ERROR:", e)
        return None