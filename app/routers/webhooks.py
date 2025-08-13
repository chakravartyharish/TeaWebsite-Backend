from fastapi import APIRouter, Request, Header, HTTPException
import hmac, hashlib, os
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.cart_order import Order
from app.services.inventory import deduct_inventory
from app.services.notifications_flow import notify_order_placed

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/razorpay")
async def razorpay_webhook(req: Request, x_razorpay_signature: str = Header(None)):
    body = await req.body()
    secret = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_razorpay_signature or ""):
        raise HTTPException(400, "Bad signature")
    payload = await req.json()
    event = payload.get('event')
    if event == 'payment.captured':
        try:
            order_id = int(payload['payload']['payment']['entity']['notes'].get('order_id', 0)) if payload['payload']['payment']['entity']['notes'] else 0
        except Exception:
            order_id = 0
        amount = int(payload['payload']['payment']['entity'].get('amount', 0)) // 100
        phone = payload['payload']['payment']['entity'].get('contact')
        if order_id:
            with SessionLocal() as db:
                order = db.get(Order, order_id)
                if order:
                    order.payment_status = 'paid'
                    order.status = 'confirmed'
                    db.add(order)
                    deduct_inventory(db, order.id)
                    db.commit()
        if phone and order_id:
            await notify_order_placed(phone, order_id, amount)
    return {"ok": True}


