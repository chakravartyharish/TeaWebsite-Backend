from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from app.core.db import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    slug = Column(String(150), unique=True, index=True)
    name = Column(String(200), nullable=False)
    story = Column(Text)
    ingredients = Column(Text)
    benefits = Column(Text)
    brew_temp_c = Column(Integer)  # e.g., 80
    brew_time_min = Column(Float)  # e.g., 3.5
    hero_image = Column(String(500))


class Variant(Base):
    __tablename__ = "variants"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    pack_size_g = Column(Integer)
    price_inr = Column(Integer)
    mrp_inr = Column(Integer)
    sku = Column(String(100), unique=True)
    inventory_qty = Column(Integer, default=0)

