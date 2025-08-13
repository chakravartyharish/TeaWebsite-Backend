from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, random, redis

router = APIRouter(prefix="/auth", tags=["auth"])
_r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))


class OTPRequest(BaseModel):
    phone: str


class OTPVerify(BaseModel):
    phone: str
    code: str


def _otp_key(phone: str):
    return f"otp:{phone}"


@router.post("/otp/request")
def request_otp(data: OTPRequest):
    # rate-limit basic: prevent frequent resend
    k = _otp_key(data.phone)
    if _r.ttl(k) and _r.ttl(k) > 240:
        raise HTTPException(429, "Please wait before requesting another OTP")
    code = f"{random.randint(100000, 999999)}"
    _r.setex(k, 300, code)  # 5 minutes
    # TODO: integrate MSG91/Twilio to send SMS/WhatsApp
    print("DEBUG OTP:", code)
    return {"ok": True}


@router.post("/otp/verify")
def verify_otp(data: OTPVerify):
    k = _otp_key(data.phone)
    saved = _r.get(k)
    if not saved or data.code != saved.decode():
        raise HTTPException(400, "Invalid or expired OTP")
    _r.delete(k)
    return {"ok": True, "phone": data.phone}


