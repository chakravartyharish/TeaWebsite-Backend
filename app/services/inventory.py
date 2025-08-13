from sqlalchemy.orm import Session
from app.models.cart_order import OrderItem
from app.models.product import Variant


def deduct_inventory(db: Session, order_id: int):
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    for it in items:
        v = db.get(Variant, it.variant_id)
        if v:
            v.inventory_qty = max(0, (v.inventory_qty or 0) - it.qty)
            db.add(v)


