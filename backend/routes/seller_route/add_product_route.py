from fastapi import Depends, APIRouter, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from static.image.product import save_image
from schemas.product_schemas import ProductCreate, ProductOut
from cruds.seller_crud.add_product import add_product
from enums import Role
from database import get_db
from models.user import User
from services.permission import requered
from enums import Role



product_route = APIRouter()

@product_route.post("/add_product", response_model=ProductOut)

async def add_product_route( name: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(requered(Role.ADMIN, Role.SELLER))):
    
    image_url = None
    if image:
        image_url = await save_image(image)
    
    data = ProductCreate(
        name=name,
        price=price,
        category=category,
        stock=stock,
        image_url=image_url )
    
    product = await add_product(data,image_url, db, current_user)

    return ProductOut.model_validate(product)

