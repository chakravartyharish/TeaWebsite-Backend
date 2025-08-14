from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json

from ..services.qr_service import QRCodeService
from ..models.mongo_models import Product

router = APIRouter(prefix="/qr", tags=["QR Codes"])

class QRCodeResponse(BaseModel):
    qr_code: str
    data: str
    type: str

class PaymentQRRequest(BaseModel):
    amount: float
    order_id: str
    merchant_upi_id: Optional[str] = "innerveda@upi"
    merchant_name: Optional[str] = "Inner Veda"

class ContactQRRequest(BaseModel):
    name: str
    organization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None

class StoreLocationQRRequest(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    hours: Optional[str] = None

class DiscountQRRequest(BaseModel):
    discount_code: str
    expiry_days: int = 30
    terms: Optional[str] = ""

class LoyaltyQRRequest(BaseModel):
    customer_id: str
    points: int = 0

class InventoryQRRequest(BaseModel):
    product_id: str
    sku: str
    location: Optional[str] = ""

@router.get("/product/{product_slug}", response_model=QRCodeResponse)
async def generate_product_qr(product_slug: str):
    """Generate QR code for a specific product"""
    try:
        # Get product to verify it exists
        product = await Product.find_one(Product.slug == product_slug)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        qr_code = QRCodeService.generate_product_qr(product_slug)
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"https://innerveda.netlify.app/product/{product_slug}",
            type="product"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")

@router.post("/payment", response_model=QRCodeResponse)
async def generate_payment_qr(request: PaymentQRRequest):
    """Generate UPI payment QR code"""
    try:
        merchant_info = {
            "upi_id": request.merchant_upi_id,
            "name": request.merchant_name
        }
        
        qr_code = QRCodeService.generate_payment_qr(
            amount=request.amount,
            order_id=request.order_id,
            merchant_info=merchant_info
        )
        
        upi_string = (
            f"upi://pay?"
            f"pa={request.merchant_upi_id}&"
            f"pn={request.merchant_name}&"
            f"am={request.amount}&"
            f"cu=INR&"
            f"tn=Order {request.order_id}"
        )
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=upi_string,
            type="payment"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate payment QR code: {str(e)}")

@router.post("/contact", response_model=QRCodeResponse)
async def generate_contact_qr(request: ContactQRRequest):
    """Generate vCard QR code for contact information"""
    try:
        contact_info = {
            "name": request.name,
            "organization": request.organization or "Inner Veda Tea Store",
            "phone": request.phone or "",
            "email": request.email or "",
            "website": request.website or "https://innerveda.netlify.app"
        }
        
        qr_code = QRCodeService.generate_contact_qr(contact_info)
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"Contact: {request.name}",
            type="contact"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate contact QR code: {str(e)}")

@router.get("/order/{order_id}")
async def generate_order_tracking_qr(order_id: str, phone: str = Query(...)):
    """Generate QR code for order tracking"""
    try:
        qr_code = QRCodeService.generate_order_qr(order_id, phone)
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"Order tracking: {order_id}",
            type="order_tracking"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate order QR code: {str(e)}")

@router.get("/feedback")
async def generate_feedback_qr(product_id: Optional[str] = Query(None)):
    """Generate QR code for feedback form"""
    try:
        qr_code = QRCodeService.generate_feedback_qr(product_id)
        
        feedback_url = f"https://innerveda.netlify.app/feedback"
        if product_id:
            feedback_url += f"?product={product_id}"
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=feedback_url,
            type="feedback"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate feedback QR code: {str(e)}")

@router.post("/store-location", response_model=QRCodeResponse)
async def generate_store_location_qr(request: StoreLocationQRRequest):
    """Generate QR code for store location"""
    try:
        store_info = {
            "name": request.name,
            "address": request.address,
            "phone": request.phone or "",
            "latitude": request.latitude or "",
            "longitude": request.longitude or "",
            "hours": request.hours or ""
        }
        
        qr_code = QRCodeService.generate_store_location_qr(store_info)
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"Store: {request.name} at {request.address}",
            type="store_location"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate store location QR code: {str(e)}")

@router.post("/discount", response_model=QRCodeResponse)
async def generate_discount_qr(request: DiscountQRRequest):
    """Generate QR code for discount/coupon"""
    try:
        expiry_date = datetime.utcnow() + timedelta(days=request.expiry_days)
        qr_code = QRCodeService.generate_discount_qr(
            discount_code=request.discount_code,
            expiry_date=expiry_date,
            terms=request.terms or ""
        )
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"Discount code: {request.discount_code}",
            type="discount"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate discount QR code: {str(e)}")

@router.post("/loyalty", response_model=QRCodeResponse)
async def generate_loyalty_qr(request: LoyaltyQRRequest):
    """Generate QR code for loyalty program"""
    try:
        qr_code = QRCodeService.generate_loyalty_qr(
            customer_id=request.customer_id,
            points=request.points
        )
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"Loyalty: {request.customer_id} ({request.points} points)",
            type="loyalty"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate loyalty QR code: {str(e)}")

@router.post("/inventory", response_model=QRCodeResponse)
async def generate_inventory_qr(request: InventoryQRRequest):
    """Generate QR code for inventory management"""
    try:
        qr_code = QRCodeService.generate_inventory_qr(
            product_id=request.product_id,
            sku=request.sku,
            location=request.location or ""
        )
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"Inventory: {request.sku}",
            type="inventory"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate inventory QR code: {str(e)}")

@router.get("/wifi")
async def generate_wifi_qr(ssid: str = Query(...), password: str = Query(...), security: str = Query("WPA")):
    """Generate WiFi QR code"""
    try:
        qr_code = QRCodeService.generate_wifi_qr(ssid, password, security)
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"WiFi: {ssid}",
            type="wifi"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate WiFi QR code: {str(e)}")

@router.get("/social/{platform}")
async def generate_social_media_qr(platform: str, handle: str = Query(...)):
    """Generate QR code for social media profiles"""
    try:
        qr_code = QRCodeService.generate_social_media_qr(platform, handle)
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"{platform.title()}: @{handle}",
            type="social_media"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate social media QR code: {str(e)}")

@router.get("/table-order/{table_number}")
async def generate_table_order_qr(table_number: str, restaurant_id: str = Query("main")):
    """Generate QR code for table ordering"""
    try:
        qr_code = QRCodeService.generate_table_order_qr(table_number, restaurant_id)
        
        return QRCodeResponse(
            qr_code=qr_code,
            data=f"Table order: Table {table_number}",
            type="table_order"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate table order QR code: {str(e)}")