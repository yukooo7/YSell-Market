from fastapi import APIRouter, Depends, UploadFile, File, Form
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.admin_cruds.user import update_user
from enums import Role
from database import get_db
from schemas.user import UserUpdate
from services.permission import requered
from typing import Optional
from datetime import datetime

api_route = APIRouter()

@api_route.patch("/update_user/{user_id}")
async def update_user_route(user_id:int, username:Optional[str] = Form(None),
                                email:Optional[str] = Form(None),
                                phone:Optional[str] = Form(None),
                                role:Optional[Role] = Form(None),
                                created_at:Optional[datetime] = Form(None),
                                avatar_url:Optional[UploadFile] = Form(None), db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN, Role.SELLER))):
    
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
    if avatar is not None:
        data["avatar_url"] = avatar

    updated_user = await update_user.update_user_crud(user_id, data, db)

    return updated_user