from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from jose import JWTError
from models.token_blakclist import TokenBlackList  # Исправил имя модели
from database import get_db
from schemas.login import RequestToken
from services.utilits_token import create_access_token, create_refersh_token, decode_token  # Исправил опечатку
from schemas.token import RefreshRequest

api_route = APIRouter()

@api_route.post("/refresh", response_model=RequestToken)
async def refresh_token_route(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    token_refresh = data.refresh_token

    # Проверяем blacklist
    stmt = select(TokenBlackList).where(TokenBlackList.token == token_refresh)
    is_blacklisted = await db.scalar(stmt)
    if is_blacklisted:
        raise HTTPException(status_code=401, detail="Token is invalid or has been used")

    try:
        payload = decode_token(token_refresh)
        user_id = payload.get("sub")  # Убрал int(), sub обычно строка
        user_role = payload.get("role")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        if user_role is None:
            raise HTTPException(status_code=401, detail="Role not found in token")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Генерируем новые токены с ролью
    new_access_token = create_access_token({"sub": user_id, "role": user_role})
    new_refresh_token = create_refersh_token({"sub": user_id})

    try:
        # Добавляем старый refresh в blacklist
        blacklisted_token = TokenBlackList(token=token_refresh)
        db.add(blacklisted_token)
        await db.commit()
        await db.refresh(blacklisted_token)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer"
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")