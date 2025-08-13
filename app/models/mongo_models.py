from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class Variant(BaseModel):
    id: int
    pack_size_g: int
    price_inr: float
    mrp_inr: float
    sku: str
    inventory_qty: int

class Product(Document):
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    image: str
    category: str
    benefits: List[str] = []
    in_stock: bool = True
    rating: float = 0.0
    reviews: int = 0
    slug: str
    story: Optional[str] = None
    ingredients: Optional[str] = None
    brew_temp_c: Optional[int] = None
    brew_time_min: Optional[int] = None
    hero_image: Optional[str] = None
    variants: List[Variant] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "products"
        indexes = [
            "slug",
            "category",
            "in_stock"
        ]

class Category(Document):
    name: str
    description: Optional[str] = None
    slug: str
    image: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "categories"
        indexes = ["slug"]
