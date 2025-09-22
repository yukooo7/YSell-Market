from pydantic import BaseModel, Field
from enums import Category
from typing import Optional

class ProductCreate(BaseModel):
    name:str = Field(..., min_length=2, max_length=100, description="Название продукта")
    price:float = Field(..., gt=0, description="Цена товра должна быть боьше 0")
    category:Category
    stock:int = Field(..., ge=0)



class ProductOut(BaseModel):
    id:int
    name:str
    price:float 
    category:Optional[Category] = None
    user_id:int
    discount_percent:Optional[int]
    stock:int

    model_config = {
        "from_attributes":True
    }

class ProductUpdate(BaseModel):
    name:Optional[str] = Field(None, min_length=2, max_length=100, description="Название продукта")
    price:Optional[float] = Field(None, gt=0, description="Цена товра должна быть боьше 0")
    category:Optional[Category] = None
    stack:Optional[int] = Field(None, ge=0)

