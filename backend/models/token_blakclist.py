from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime
from database import Base
from datetime import datetime
from sqlalchemy.sql import func


class TokenBlackList(Base):
   __tablename__ = "token_blacklists"
   id:Mapped[int] = mapped_column(primary_key=True, index=True)
   token:Mapped[str] = mapped_column(nullable=False, index=True)
   created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())