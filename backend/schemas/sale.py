from pydantic import BaseModel, Field
from datetime import datetime
from schemas.product_schemas import ProductOut



class SaleCreate(BaseModel):
    title:str = Field(..., min_length=1, max_length=100, description="Название скидки")
    product_id:int = Field(..., gt=0)
    percent:int = Field(..., gt=1, lt=99)

class SaleOut(BaseModel):
    title:str
    product:ProductOut
    created_at:datetime

    model_config = {
        "from_attributes":True
    }

