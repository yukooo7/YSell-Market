from pydantic import BaseModel
from datetime import datetime
from schemas.user import UserOut
from schemas.product_schemas import ProductOut



class CreateCart(BaseModel):
    product_id:int
    quantity:int


class CartOut(BaseModel):
    id:int
    user:UserOut
    product:ProductOut
    quantity:int
    created_at:datetime

    model_config = {
        "from_attributes":True
    }