from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from app.core.db import Base


class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), unique=True, index=True)


class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"))
    variant_id = Column(Integer)
    qty = Column(Integer)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(30), default="created")
    subtotal = Column(Numeric(12, 2))
    shipping = Column(Numeric(12, 2))
    tax = Column(Numeric(12, 2))
    total = Column(Numeric(12, 2))
    payment_status = Column(String(30), default="pending")
    payment_gateway = Column(String(30))
    gateway_order_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    variant_id = Column(Integer)
    qty = Column(Integer)
    unit_price = Column(Numeric(12, 2))

