from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Union


SECRET_KEY = "NEVERDONTSTOPBRO"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MIN = 60
REFRESH_TOKEN_EXPIRE_DAY = 7


def create_access_token(data: dict) -> str:
    encode_to = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    encode_to.update({"exp": int(expire.timestamp())})
    print("[create_access_token] Payload:", encode_to)
    token = jwt.encode(encode_to, SECRET_KEY, algorithm=ALGORITHM)
    print("[create_access_token] Token:", token)
    return token

def create_refersh_token(data: dict) -> str:
    """Создание refresh токена 
        Вводим Dict а в ответ получаем Token в виде Str


    Args:
        data (dict): User

    Returns:
        str: User-s Token which we made
    """

    # Делаем копию нашего пользователья чтобы
    # не изменить его данные
    encode_to = data.copy()

    # Создаем длитеьность  жизни referesh токена
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAY)

    # В Encode добавляем словарь exp это длительность жизни refresh токена
    encode_to.update({"exp": int(expire.timestamp())})

    # Coздаем jwt токен
    encode_jwt = jwt.encode(encode_to, SECRET_KEY, algorithm=ALGORITHM)

    # Выводим наш токен чтобы прогрма могла с ним работать 
    return encode_jwt



def decode_token(token: str) -> Union[dict, None]:
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODED PAYLOAD:", decode)
        return decode
    except JWTError as e:
        print("JWT DECODE ERROR:", e)
        return None