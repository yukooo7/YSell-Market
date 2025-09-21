from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Enum
from enums import  Role
from typing import List

class User(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    username:Mapped[str] = mapped_column( nullable=False)
    email:Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    phone:Mapped[str] = mapped_column(nullable=False)
    role:Mapped[Role] = mapped_column(Enum(Role), default=Role.GUEST)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    password:Mapped[str] = mapped_column(nullable=False)
    orders: Mapped[List["Order"]] = relationship(back_populates='user', cascade='all, delete-orphan', passive_deletes=True)
    products :Mapped[List["Product"]] = relationship(back_populates='user', cascade='all, delete-orphan')
    carts: Mapped[List["BusketCart"]] = relationship(back_populates='user', cascade='all, delete-orphan')