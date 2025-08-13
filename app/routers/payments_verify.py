from fastapi import APIRouter, HTTPException
import os, hmac, hashlib

router = APIRouter(prefix="/payments", tags=["payments"]) 


@router.post('/razorpay/verify')
async def verify(resp: dict):
    order_id = resp.get('razorpay_order_id')
    payment_id = resp.get('razorpay_payment_id')
    signature = resp.get('razorpay_signature')
    secret = os.getenv('RAZORPAY_KEY_SECRET', '')
    body = f"{order_id}|{payment_id}".encode()
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature or ''):
        raise HTTPException(400, 'Invalid signature')
    return {"ok": True, "order_id": order_id, "payment_id": payment_id}


