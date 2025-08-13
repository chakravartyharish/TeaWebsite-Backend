from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.product import Product, Variant

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [
        {"id": p.id, "slug": p.slug, "name": p.name, "hero_image": p.hero_image}
        for p in products
    ]


@router.get("/{slug}")
def get_product(slug: str, db: Session = Depends(get_db)):
    p = db.query(Product).filter_by(slug=slug).first()
    if not p:
        return {"detail": "not found"}
    variants = db.query(Variant).filter_by(product_id=p.id).all()
    return {
        "id": p.id,
        "slug": p.slug,
        "name": p.name,
        "story": p.story,
        "ingredients": p.ingredients,
        "benefits": p.benefits,
        "brew_temp_c": p.brew_temp_c,
        "brew_time_min": p.brew_time_min,
        "hero_image": p.hero_image,
        "variants": [
            {
                "id": v.id,
                "pack_size_g": v.pack_size_g,
                "price_inr": int(v.price_inr),
                "mrp_inr": int(v.mrp_inr),
                "sku": v.sku,
                "inventory_qty": v.inventory_qty,
            }
            for v in variants
        ],
    }


