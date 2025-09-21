from fastapi import APIRouter, Depends
from cruds.buyyer_crud.get_me import  update_pasaword, upgrade_profile
from models.user import User
from database import get_db
from services.permission import requered
from enums import Role
from schemas.user import ProfileUpdate, PasswordUpdate, UserOut
from sqlalchemy.ext.asyncio import AsyncSession

buyyer_route = APIRouter()

@buyyer_route.get("/get_me", response_model=UserOut)
async def get_me_route(user:User = Depends(requered(Role.SHOPPER, Role.SELLER, Role.ADMIN))):


    return UserOut.model_validate(user)

@buyyer_route.patch("/upgrade_profile")
async def upgrade_profile_route(user_data:ProfileUpdate, user:User = Depends(requered(Role.SHOPPER, Role.SELLER, Role.ADMIN)), db:AsyncSession = Depends(get_db)):

    user = await upgrade_profile(user_data, user, db)

    return user

@buyyer_route.put("/update_password")
async def update_password_route(data:PasswordUpdate, user:User = Depends(requered(Role.SHOPPER, Role.SELLER, Role.ADMIN)), db:AsyncSession = Depends(get_db)):

    password = await update_pasaword(data, user, db)

    return password