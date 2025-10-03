from services.jwt_oauth_header import get_current_tokken
from enums import Role
from fastapi import HTTPException, Depends
from models.user import User


def requered(*allowed_role:Role):
    """ Декоратор для провери токена и потом роля 
    """
    async def wrapper(current_user:User = Depends(get_current_tokken)):
        if not current_user.role in allowed_role:
            raise HTTPException(status_code=403, detail="Нет доступа для этого роля")
        return current_user
    return wrapper
