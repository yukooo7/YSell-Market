from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func
from enums import Category
from sqlalchemy import Enum
from datetime import datetime
from models.cart import BusketCart
from typing import List

class Product(Base):
    __tablename__ = 'products'
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    name:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[float] = mapped_column(nullable=False)
    category:Mapped[Category] = mapped_column(Enum(Category), default=None)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    discount_percent:Mapped[int] = mapped_column(default=0)
    stock: Mapped[int] = mapped_column(default=0) 
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sales:Mapped[List["Sale"]] = relationship(back_populates="product",cascade='all, delete-orphan' )
    user:Mapped["User"] = relationship(back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")
    carts:Mapped[List["BusketCart"]] = relationship(back_populates="product")