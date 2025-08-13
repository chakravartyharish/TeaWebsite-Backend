from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.db import Base


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    line1 = Column(String(255))
    line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(20))
    country = Column(String(100), default="India")
    is_default = Column(Boolean, default=False)

