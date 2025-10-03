from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from schemas.product_schemas import ProductOut, ProductUpdate


async def update_product(product_id:int, new_data:ProductUpdate, db:AsyncSession)-> ProductOut:
    # Мы находим продуктп id
    product = await db.get(Product, product_id)
    # Если его нет т выдаем ошибку 404
    if not product:
        raise HTTPException(status_code=404, detail="продукт не найден")
    # мы ьерм наши новые данные и преврашяем его в дикт ст помошю model_dump
    # и говарим с помошю exlude_unset что если пару поль не ввели то пропусти их
    new_product = new_data.model_dump(exclude_unset=True)
    # перебираем все данные с нашего нового пролуката в качсве дикт
    for k, v in new_product.items():
    # setettr обнавляет Product находя key на новое value 
        setattr(product, k, v)

    try:
        await db.commit()
        await db.refresh(product)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return ProductOut.model_validate(product)