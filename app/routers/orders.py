from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
# MongoDB-only - SQLAlchemy removed
from app.models.cart_order import Order, OrderItem
from app.models.product import Variant
from decimal import Decimal

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderItemIn(BaseModel):
    variant_id: int
    qty: int


class OrderIn(BaseModel):
    user_id: int | None = None
    items: list[OrderItemIn]
    address_id: int | None = None
    notes: dict | None = None


class OrderCreate(BaseModel):
    user_id: int | None = None
    items: list[OrderItemIn]
    address_id: int | None = None
    notes: dict | None = None


@router.post("")
def create_order(order: OrderCreate):
    if not order.items:
        raise HTTPException(400, "No items")
    subtotal = Decimal("0.00")
    order_db = Order(
        user_id=order.user_id,
        status="created",
        payment_status="pending",
        subtotal=0,
        shipping=0,
        tax=0,
        total=0,
    )
    db.add(order)
    db.flush()
    for it in data.items:
        v = db.get(Variant, it.variant_id)
        if not v or v.inventory_qty < it.qty:
            raise HTTPException(400, f"Variant {it.variant_id} unavailable")
        line_total = Decimal(v.price_inr) * it.qty
        subtotal += line_total
        db.add(
            OrderItem(
                order_id=order.id,
                variant_id=v.id,
                qty=it.qty,
                unit_price=v.price_inr,
            )
        )
    shipping = Decimal("0.00") if subtotal >= Decimal("499") else Decimal("49.00")
    tax = (subtotal * Decimal("0.05")).quantize(Decimal("1.00"))  # placeholder 5%
    total = subtotal + shipping + tax
    order.subtotal, order.shipping, order.tax, order.total = subtotal, shipping, tax, total
    db.commit()
    db.refresh(order)
    return {
        "id": order.id,
        "subtotal": float(subtotal),
        "shipping": float(shipping),
        "tax": float(tax),
        "total": float(total),
    }


