from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from schemas.product_schemas import ProductCreate, ProductOut
from cruds.seller_crud.add_product import add_product
from enums import Role
from database import get_db
from models.user import User
from services.permission import requered
from enums import Role


product_route = APIRouter()

@product_route.post("/add_product", response_model=ProductOut)

async def add_product_route(data:ProductCreate, 
                            db:AsyncSession = Depends(get_db),
                             current_user:User = Depends(requered(Role.ADMIN, Role.SELLER))):
    
    product = await add_product(data, db, current_user)

    return ProductOut.model_validate(product)

