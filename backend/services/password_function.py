from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hash_password(password:str) -> str:
    """Хешируем пароль с помошю bcrypt
    """
    return pwd_context.hash(password)

def check_password(plain_password:str, hashed_password:str):
    """проверка  паролья с помошю bcrypt
    """
    return pwd_context.verify(plain_password, hashed_password)