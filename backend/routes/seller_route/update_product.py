from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from database import get_db
from services.permission import requered
from enums import Role
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.seller_crud.update_product import update_product
from models.user import User

product_route = APIRouter()

@product_route.patch("/product_update/{product_id}")
async def update_product_route(
    product_id: int,
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category: Optional[str] = Form(None),
    stock: Optional[int] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(requered(Role.SELLER)),
):

    # Сохраняем новую картинку, если есть
    image_url = None
    if image:
        from static.image.product import save_image  # если не импортировал
        image_url = await save_image(image)

    # Создаем словарь с обновляемыми полями
    update_data = {}
    if name is not None:
        update_data['name'] = name
    if price is not None:
        update_data['price'] = price
    if category is not None:
        update_data['category'] = category
    if stock is not None:
        update_data['stock'] = stock
    if image_url is not None:
        update_data['image_url'] = image_url

    product = await update_product(product_id, update_data, db, user)

    return product
