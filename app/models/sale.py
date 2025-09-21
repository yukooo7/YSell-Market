from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.sql import func



class Sale(Base):
    __tablename__ = "sales"
    id:Mapped[int] = mapped_column(primary_key=True, index = True)
    title:Mapped[str] = mapped_column( nullable=False)
    product_id:Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    percent:Mapped[int] = mapped_column(nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    product: Mapped["Product"] = relationship(back_populates="sales")