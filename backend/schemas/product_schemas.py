from pydantic import BaseModel, Field
from enums import Category
from typing import Optional

class ProductCreate(BaseModel):
    name:str = Field(..., min_length=2, max_length=100, description="Название продукта")
    price:float = Field(..., gt=0, description="Цена товра должна быть боьше 0")
    category:Category
    stock:int = Field(..., ge=0)
    image_url:Optional[str] = None



class ProductOut(BaseModel):
    id:int
    name:str
    price:float 
    category:Optional[Category] = None
    user_id:int
    discount_percent:Optional[int]
    stock:int
    image_url:Optional[str] = None

    model_config = {
        "from_attributes":True
    }
    @classmethod
    def model_validate(cls, product):
        image_url = product.image_url

        if image_url:
            fixed_path = image_url.replace("\\", "/")
            full_url = f"http://localhost:8000/{fixed_path.lstrip('/')}"
        else:
            full_url = None

        return cls(
            id=product.id,
            name=product.name,
            price=product.price,
            stock=product.stock,
            category=product.category,
            image_url=full_url,
            user_id=product.user_id,
            discount_percent=product.discount_percent
        )



class ProductUpdate(BaseModel):
    name:Optional[str] = Field(None, min_length=2, max_length=100, description="Название продукта")
    price:Optional[float] = Field(None, gt=0, description="Цена товра должна быть боьше 0")
    category:Optional[Category] = None
    stock:Optional[int] = Field(None, ge=0)
    image_url:Optional[str] = None

