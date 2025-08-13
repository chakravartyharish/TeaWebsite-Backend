import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.db import Base
from app.models.product import Product, Variant


DB = os.getenv('DATABASE_URL')
engine = create_engine(DB)
Base.metadata.create_all(engine)

with Session(engine) as s:
    t = Product(
        slug='darjeeling-first-flush',
        name='Darjeeling First Flush',
        story='Spring pluck, floral',
        ingredients='Camellia sinensis',
        benefits='Light, uplifting',
        brew_temp_c=85,
        brew_time_min=3,
        hero_image='https://picsum.photos/seed/tea1/800'
    )
    s.add(t)
    s.flush()
    s.add_all([
        Variant(product_id=t.id, pack_size_g=50, price_inr=399, mrp_inr=449, sku='DJ-FF-50', inventory_qty=100),
        Variant(product_id=t.id, pack_size_g=100, price_inr=699, mrp_inr=799, sku='DJ-FF-100', inventory_qty=80),
    ])
    s.commit()
print('Seeded!')


