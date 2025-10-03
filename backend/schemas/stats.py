from pydantic import BaseModel
from typing import List

class SellerSales(BaseModel):
    seller_id:int
    seller_name:str
    total_sales:int
    
class AdminState(BaseModel):
    total_order:int
    total_revenue:float
    sales_by_saller:List[SellerSales]