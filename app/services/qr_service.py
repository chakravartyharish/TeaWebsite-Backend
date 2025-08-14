import qrcode
from io import BytesIO
import base64
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json

class QRCodeService:
    """Service for generating and managing QR codes for various use cases"""
    
    @staticmethod
    def generate_qr_code(data: str, size: int = 10, border: int = 4) -> str:
        """
        Generate a QR code and return it as base64 encoded string
        
        Args:
            data: The data to encode in the QR code
            size: Size of the QR code (default 10)
            border: Border size (default 4)
        
        Returns:
            Base64 encoded PNG image of the QR code
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def generate_product_qr(product_id: str, base_url: str = "https://innerveda.netlify.app") -> str:
        """Generate QR code for product page"""
        product_url = f"{base_url}/product/{product_id}"
        return QRCodeService.generate_qr_code(product_url)
    
    @staticmethod
    def generate_order_qr(order_id: str, customer_phone: str, base_url: str = "https://innerveda.netlify.app") -> str:
        """Generate QR code for order tracking"""
        tracking_data = {
            "type": "order_tracking",
            "order_id": order_id,
            "phone": customer_phone,
            "url": f"{base_url}/track-order/{order_id}",
            "timestamp": datetime.utcnow().isoformat()
        }
        return QRCodeService.generate_qr_code(json.dumps(tracking_data))
    
    @staticmethod
    def generate_payment_qr(amount: float, order_id: str, merchant_info: Dict[str, str]) -> str:
        """Generate UPI payment QR code"""
        # UPI QR code format
        upi_string = (
            f"upi://pay?"
            f"pa={merchant_info.get('upi_id', 'merchant@upi')}&"
            f"pn={merchant_info.get('name', 'Inner Veda')}&"
            f"am={amount}&"
            f"cu=INR&"
            f"tn=Order {order_id}"
        )
        return QRCodeService.generate_qr_code(upi_string)
    
    @staticmethod
    def generate_contact_qr(contact_info: Dict[str, str]) -> str:
        """Generate vCard QR code for contact information"""
        vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact_info.get('name', 'Inner Veda')}
ORG:{contact_info.get('organization', 'Inner Veda Tea Store')}
TEL:{contact_info.get('phone', '')}
EMAIL:{contact_info.get('email', '')}
URL:{contact_info.get('website', 'https://innerveda.netlify.app')}
END:VCARD"""
        return QRCodeService.generate_qr_code(vcard)
    
    @staticmethod
    def generate_wifi_qr(ssid: str, password: str, security: str = "WPA") -> str:
        """Generate WiFi QR code"""
        wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"
        return QRCodeService.generate_qr_code(wifi_string)
    
    @staticmethod
    def generate_feedback_qr(product_id: Optional[str] = None, base_url: str = "https://innerveda.netlify.app") -> str:
        """Generate QR code for feedback form"""
        if product_id:
            feedback_url = f"{base_url}/feedback?product={product_id}"
        else:
            feedback_url = f"{base_url}/feedback"
        return QRCodeService.generate_qr_code(feedback_url)
    
    @staticmethod
    def generate_discount_qr(discount_code: str, expiry_date: datetime, terms: str = "") -> str:
        """Generate QR code for discount/coupon"""
        discount_data = {
            "type": "discount",
            "code": discount_code,
            "expires": expiry_date.isoformat(),
            "terms": terms,
            "timestamp": datetime.utcnow().isoformat()
        }
        return QRCodeService.generate_qr_code(json.dumps(discount_data))
    
    @staticmethod
    def generate_loyalty_qr(customer_id: str, points: int = 0) -> str:
        """Generate QR code for loyalty program"""
        loyalty_data = {
            "type": "loyalty",
            "customer_id": customer_id,
            "points": points,
            "timestamp": datetime.utcnow().isoformat()
        }
        return QRCodeService.generate_qr_code(json.dumps(loyalty_data))
    
    @staticmethod
    def generate_inventory_qr(product_id: str, sku: str, location: str = "") -> str:
        """Generate QR code for inventory management"""
        inventory_data = {
            "type": "inventory",
            "product_id": product_id,
            "sku": sku,
            "location": location,
            "timestamp": datetime.utcnow().isoformat()
        }
        return QRCodeService.generate_qr_code(json.dumps(inventory_data))
    
    @staticmethod
    def generate_store_location_qr(store_info: Dict[str, str]) -> str:
        """Generate QR code for store location"""
        # Google Maps URL format
        maps_url = f"https://maps.google.com/?q={store_info.get('latitude', '')},{store_info.get('longitude', '')}"
        
        location_data = {
            "type": "store_location",
            "name": store_info.get('name', 'Inner Veda Store'),
            "address": store_info.get('address', ''),
            "phone": store_info.get('phone', ''),
            "maps_url": maps_url,
            "hours": store_info.get('hours', ''),
            "timestamp": datetime.utcnow().isoformat()
        }
        return QRCodeService.generate_qr_code(json.dumps(location_data))
    
    @staticmethod
    def generate_table_order_qr(table_number: str, restaurant_id: str, base_url: str = "https://innerveda.netlify.app") -> str:
        """Generate QR code for table ordering (dine-in)"""
        order_url = f"{base_url}/table-order?table={table_number}&restaurant={restaurant_id}"
        return QRCodeService.generate_qr_code(order_url)
    
    @staticmethod
    def generate_social_media_qr(platform: str, handle: str) -> str:
        """Generate QR code for social media profiles"""
        social_urls = {
            "instagram": f"https://instagram.com/{handle}",
            "facebook": f"https://facebook.com/{handle}",
            "twitter": f"https://twitter.com/{handle}",
            "youtube": f"https://youtube.com/{handle}",
            "linkedin": f"https://linkedin.com/company/{handle}"
        }
        
        url = social_urls.get(platform.lower(), f"https://{platform}.com/{handle}")
        return QRCodeService.generate_qr_code(url)