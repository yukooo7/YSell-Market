from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Enum
from enums import OrderStatus
from typing import Optional

class OrderCreate(BaseModel):
    user_id:int
    product_id:int
    price:float
    status:Optional[OrderStatus] = None


class UserOut(BaseModel):
    id: int
    username: str



class ProductOut(BaseModel):
    id: int
    name: str
    price: float




from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schemas.product_schemas import ProductOut  # Схема для товара
from schemas.user import UserOut        # Схема для пользователя


class OrderItemOut(BaseModel):
    id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    price: float
    status: str
    created_at: datetime
    user: UserOut
    items: List[OrderItemOut] 

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status:OrderStatus


class MessageDelete(BaseModel):
    message:str