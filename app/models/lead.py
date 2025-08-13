from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.db import Base


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    phone = Column(String(20), index=True)
    email = Column(String(255))
    source = Column(String(100))  # popup/quiz/exit-intent
    tags = Column(String(255))
    marketing_optin = Column(Boolean, default=False)
    whatsapp_optin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

