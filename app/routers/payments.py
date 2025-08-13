from fastapi import APIRouter
import httpx, os

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/razorpay/order")
async def create_rzp_order(payload: dict):
    """ payload: {amount_inr: int, receipt: str, notes?: dict} """
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    async with httpx.AsyncClient(auth=(key_id, key_secret)) as client:
        r = await client.post(
            "https://api.razorpay.com/v1/orders",
            json={
                "amount": payload["amount_inr"] * 100,
                "currency": "INR",
                "receipt": payload.get("receipt", "rcpt1"),
                "notes": payload.get("notes", {}),
                "payment_capture": 1,
            },
        )
        r.raise_for_status()
        return r.json()


