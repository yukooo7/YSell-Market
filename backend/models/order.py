from database import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship
from sqlalchemy import ForeignKey, DateTime, Enum
from datetime import datetime
from sqlalchemy.sql import func
from enums import OrderStatus
from typing import List

class Order(Base):
    __tablename__ = "orders"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    status:Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    items:Mapped[List["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan", passive_deletes=True)
    user:Mapped["User"] = relationship(back_populates="orders")


class OrderItem(Base):
    __tablename__ = 'order_items'
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete='CASCADE'), nullable=False)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id",ondelete="CASCADE"), nullable=False)
    quantity:Mapped[int] = mapped_column(nullable=False)
    price_to_purchase:Mapped[int] = mapped_column(nullable=False)
    order:Mapped["Order"] = relationship(back_populates="items")
    product:Mapped["Product"] = relationship(back_populates="order_items")
