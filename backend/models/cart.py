from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from sqlalchemy import DateTime, func, ForeignKey

class BusketCart(Base):
    __tablename__ = 'basketcart'
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity:Mapped[int] = mapped_column(nullable=False)
    price_with_discount: Mapped[float] = mapped_column(nullable=False, default=0)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    user: Mapped['User'] = relationship(back_populates="carts")
    product: Mapped["Product"] = relationship(back_populates="carts")
