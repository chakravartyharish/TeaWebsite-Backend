from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    marketing_optin = Column(Boolean, default=False)
    whatsapp_optin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

