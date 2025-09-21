from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas.login import ResponseLogin, RequestToken
from schemas.user import UserCreate, UserOut
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.auth_crud import register_crud



api_route = APIRouter()

@api_route.post("/register")
async def register_route(data:UserCreate, db:AsyncSession= Depends(get_db)):

    user = await register_crud.register(data, db)

    return {'user':user['user'],
            "access_token":user['access_token'],
            "refersh_token":user["refresh_token"]
            }