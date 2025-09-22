from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from jose import JWTError
from models.token_blakclist import TokenBlackList
from database import get_db
from schemas.login import RequestToken
from services.utilits_token import create_access_token, create_refersh_token, decode_token
from pydantic import BaseModel
from schemas.token import RefreshRequest

api_route = APIRouter()

@api_route.post("/refresh", response_model=RequestToken)
async def refresh_token_route(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    token_refresh = data.refresh_token

    stmt = select(TokenBlackList).where(TokenBlackList.token == token_refresh)
    is_blacklisted = await db.scalar(stmt)
    if is_blacklisted:
        raise HTTPException(status_code=401, detail="Token is invalid or has been used")
    try:
        payload = decode_token(token_refresh)
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refersh_token({"sub": user_id})


    try:
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
        raise HTTPException(status_code=500, detail="An error occurred during token refresh")