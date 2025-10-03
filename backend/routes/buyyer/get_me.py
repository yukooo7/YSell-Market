from fastapi import APIRouter, Depends, UploadFile, File, Form
from cruds.buyyer_crud.get_me import  update_pasaword, upgrade_profile
from models.user import User
from database import get_db
from services.permission import requered
from enums import Role
from schemas.user import PasswordUpdate, UserOut
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

buyyer_route = APIRouter()

@buyyer_route.get("/get_me", response_model= UserOut)
async def get_me_route(user:User = Depends(requered(Role.SHOPPER, Role.SELLER, Role.ADMIN))):


    return UserOut.model_validate(user)

@buyyer_route.patch("/upgrade_profile")
async def upgrade_profile_route(username:Optional[str] = Form(None),
                                email:Optional[str] = Form(None),
                                phone:Optional[str] = Form(None),
                                role:Optional[Role] = Form(None),
                                created_at:Optional[datetime] = Form(None),
                                avatar_url:Optional[UploadFile] = Form(None),
                                user:User = Depends(requered(Role.SHOPPER, Role.SELLER, Role.ADMIN)), db:AsyncSession = Depends(get_db)):
    
    avatar = None
    if avatar_url:
        from static.image.avatars import save_avatar
        avatar = await save_avatar(avatar_url)

    data = {}
    if username is not None:
        data["username"] = username
    if email is not None:
        data["email"] = email
    if phone is not None:
        data["phone"] = phone
    if role is not None:
        data["role"] = role
    if created_at is not None:
        data["created_at"] = created_at
    if avatar:
        data["avatar_url"] = avatar

    user = await upgrade_profile(data, user, db)

    return user

@buyyer_route.put("/update_password")
async def update_password_route(data:PasswordUpdate, user:User = Depends(requered(Role.SHOPPER, Role.SELLER, Role.ADMIN)), db:AsyncSession = Depends(get_db)):

    password = await update_pasaword(data, user, db)

    return password