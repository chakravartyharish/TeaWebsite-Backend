"""
Comprehensive notification service for Tea Store e-commerce platform.
Supports multiple channels: Email, SMS, WhatsApp with event-driven architecture.
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import httpx
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import ssl
from app.services.template_engine import template_engine

# Setup logging
logger = logging.getLogger(__name__)

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PUSH = "push"  # For future implementation

class NotificationEvent(str, Enum):
    # Order events
    ORDER_PLACED = "order_placed"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    ORDER_CANCELLED = "order_cancelled"
    
    # Payment events
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    PAYMENT_PENDING = "payment_pending"
    
    # User events
    USER_REGISTERED = "user_registered"
    USER_LOGIN = "user_login"
    PASSWORD_RESET = "password_reset"
    
    # Marketing events
    WELCOME_SERIES = "welcome_series"
    CART_ABANDONED = "cart_abandoned"
    PRODUCT_RESTOCK = "product_restock"
    
    # Support events
    CONTACT_FORM = "contact_form"
    FEEDBACK_RECEIVED = "feedback_received"
    
    # Admin events
    LOW_INVENTORY = "low_inventory"
    NEW_ORDER_ADMIN = "new_order_admin"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class NotificationTemplate:
    """Template for notification content"""
    subject: str
    body: str
    html_body: Optional[str] = None
    variables: List[str] = None

@dataclass
class NotificationRequest:
    """Request object for sending notifications"""
    event: NotificationEvent
    channels: List[NotificationChannel]
    recipient: str  # Email, phone, or user ID
    data: Dict[str, Any]  # Template variables
    priority: NotificationPriority = NotificationPriority.MEDIUM
    scheduled_at: Optional[datetime] = None
    template_override: Optional[NotificationTemplate] = None

class NotificationProvider:
    """Base class for notification providers"""
    
    async def send(self, request: NotificationRequest) -> Dict[str, Any]:
        raise NotImplementedError

class EmailProvider(NotificationProvider):
    """Email notification provider using SMTP"""
    
    def __init__(self):
        self.smtp_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_PORT", "587"))
        self.username = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("EMAIL_FROM")
        self.from_name = os.getenv("EMAIL_FROM_NAME", "Inner Veda")
    
    async def send(self, request: NotificationRequest) -> Dict[str, Any]:
        """Send email notification"""
        try:
            template = self._get_template(request.event, request.data)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = template.subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = request.recipient
            
            # Add text version
            text_part = MIMEText(template.body, 'plain')
            msg.attach(text_part)
            
            # Add HTML version if available
            if template.html_body:
                html_part = MIMEText(template.html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {request.recipient}")
            return {"status": "sent", "provider": "email", "recipient": request.recipient}
            
        except Exception as e:
            logger.error(f"Email send failed: {str(e)}")
            return {"status": "failed", "error": str(e), "provider": "email"}
    
    def _get_template(self, event: NotificationEvent, data: Dict[str, Any]) -> NotificationTemplate:
        """Get email template for event"""
        templates = {
            NotificationEvent.ORDER_PLACED: NotificationTemplate(
                subject="🍃 Order Confirmation - Inner Veda #{{order_id}}",
                body="Dear {{customer_name}},\n\nYour order #{{order_id}} has been placed successfully!\n\nOrder Total: ₹{{amount}}\n\nWe'll notify you once your order is shipped.\n\nThank you for choosing Inner Veda!",
                html_body=self._get_order_placed_html()
            ),
            NotificationEvent.ORDER_SHIPPED: NotificationTemplate(
                subject="📦 Your Order is on the way! - Inner Veda #{{order_id}}",
                body="Dear {{customer_name}},\n\nGreat news! Your order #{{order_id}} has been shipped.\n\nTracking ID: {{tracking_id}}\n\nExpected delivery: {{delivery_date}}\n\nTrack your order: {{tracking_url}}",
                html_body=self._get_order_shipped_html()
            ),
            NotificationEvent.CONTACT_FORM: NotificationTemplate(
                subject="🍃 Thank you for contacting Inner Veda",
                body="Dear {{name}},\n\nThank you for contacting us regarding {{category}}.\n\nWe've received your inquiry and will respond within 24 hours.\n\nReference ID: {{reference_id}}",
                html_body=self._get_contact_form_html()
            ),
        }
        
        template = templates.get(event)
        if not template:
            # Default template
            template = NotificationTemplate(
                subject="Notification from Inner Veda",
                body="Hello,\n\nYou have a new notification.\n\nThank you!"
            )
        
        # Replace variables
        template.subject = self._replace_variables(template.subject, data)
        template.body = self._replace_variables(template.body, data)
        if template.html_body:
            template.html_body = self._replace_variables(template.html_body, data)
        
        return template
    
    def _replace_variables(self, text: str, data: Dict[str, Any]) -> str:
        """Replace template variables with actual data using enhanced Jinja2 engine"""
        return template_engine.render_template(text, data)
    
    def _get_order_placed_html(self) -> str:
        return """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #2d5a45, #3b7057); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0;">🍃 Inner Veda</h1>
                <p>Order Confirmation</p>
            </div>
            <div style="padding: 30px; background: white;">
                <h2>Dear {{customer_name}},</h2>
                <p>Your order <strong>#{{order_id}}</strong> has been placed successfully!</p>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>Order Details</h3>
                    <p><strong>Order ID:</strong> {{order_id}}</p>
                    <p><strong>Total Amount:</strong> ₹{{amount}}</p>
                    <p><strong>Order Date:</strong> {{order_date}}</p>
                </div>
                <p>We'll notify you once your order is shipped.</p>
                <p>Thank you for choosing Inner Veda for your wellness journey!</p>
            </div>
        </div>
        """
    
    def _get_order_shipped_html(self) -> str:
        return """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #2d5a45, #3b7057); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0;">🍃 Inner Veda</h1>
                <p>Your Order is on the way!</p>
            </div>
            <div style="padding: 30px; background: white;">
                <h2>Great news, {{customer_name}}!</h2>
                <p>Your order <strong>#{{order_id}}</strong> has been shipped and is on its way to you.</p>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>Shipping Details</h3>
                    <p><strong>Tracking ID:</strong> {{tracking_id}}</p>
                    <p><strong>Expected Delivery:</strong> {{delivery_date}}</p>
                    <p><a href="{{tracking_url}}" style="color: #2d5a45;">Track your order</a></p>
                </div>
                <p>We hope you'll love your Inner Veda products!</p>
            </div>
        </div>
        """
    
    def _get_contact_form_html(self) -> str:
        return """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #2d5a45, #3b7057); padding: 30px; text-align: center; color: white;">
                <h1 style="margin: 0;">🍃 Inner Veda</h1>
                <p>Thank you for contacting us</p>
            </div>
            <div style="padding: 30px; background: white;">
                <h2>Dear {{name}},</h2>
                <p>Thank you for contacting us regarding <strong>{{category}}</strong>.</p>
                <p>We've received your inquiry and our team will respond within 24 hours.</p>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Reference ID:</strong> {{reference_id}}</p>
                    <p><strong>Subject:</strong> {{subject}}</p>
                </div>
                <p>For urgent matters, please call us at +91 9113920980.</p>
                <p>Thank you for choosing Inner Veda!</p>
            </div>
        </div>
        """

class WhatsAppProvider(NotificationProvider):
    """WhatsApp notification provider using Facebook Graph API"""
    
    def __init__(self):
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.phone_id = os.getenv("WHATSAPP_PHONE_ID")
        self.base_url = f"https://graph.facebook.com/v19.0/{self.phone_id}/messages"
    
    async def send(self, request: NotificationRequest) -> Dict[str, Any]:
        """Send WhatsApp notification"""
        try:
            template_name, variables = self._get_template(request.event, request.data)
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
            
            data = {
                "messaging_product": "whatsapp",
                "to": request.recipient,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "en"},
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": v} for v in variables
                            ],
                        }
                    ],
                },
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, json=data, headers=headers)
                response.raise_for_status()
                
                logger.info(f"WhatsApp sent successfully to {request.recipient}")
                return {"status": "sent", "provider": "whatsapp", "recipient": request.recipient}
                
        except Exception as e:
            logger.error(f"WhatsApp send failed: {str(e)}")
            return {"status": "failed", "error": str(e), "provider": "whatsapp"}
    
    def _get_template(self, event: NotificationEvent, data: Dict[str, Any]) -> tuple[str, List[str]]:
        """Get WhatsApp template name and variables"""
        templates = {
            NotificationEvent.ORDER_PLACED: ("order_placed", [
                data.get("order_id", ""),
                f"₹{data.get('amount', 0)}"
            ]),
            NotificationEvent.ORDER_SHIPPED: ("order_shipped", [
                data.get("order_id", ""),
                data.get("tracking_id", "")
            ]),
            NotificationEvent.ORDER_DELIVERED: ("order_delivered", [
                data.get("order_id", "")
            ]),
        }
        
        return templates.get(event, ("general_notification", [data.get("message", "")]))

class SMSProvider(NotificationProvider):
    """SMS notification provider (can be integrated with Twilio, AWS SNS, etc.)"""
    
    def __init__(self):
        self.api_key = os.getenv("SMS_API_KEY")
        self.sender_id = os.getenv("SMS_SENDER_ID", "INNERVEDA")
    
    async def send(self, request: NotificationRequest) -> Dict[str, Any]:
        """Send SMS notification"""
        try:
            message = self._get_message(request.event, request.data)
            
            # TODO: Implement actual SMS provider integration
            # This is a placeholder for SMS provider integration
            logger.info(f"SMS would be sent to {request.recipient}: {message}")
            
            return {"status": "sent", "provider": "sms", "recipient": request.recipient}
            
        except Exception as e:
            logger.error(f"SMS send failed: {str(e)}")
            return {"status": "failed", "error": str(e), "provider": "sms"}
    
    def _get_message(self, event: NotificationEvent, data: Dict[str, Any]) -> str:
        """Get SMS message for event"""
        messages = {
            NotificationEvent.ORDER_PLACED: f"Dear {data.get('customer_name', 'Customer')}, your order #{data.get('order_id')} worth ₹{data.get('amount')} has been placed successfully! - Inner Veda",
            NotificationEvent.ORDER_SHIPPED: f"Great news! Your order #{data.get('order_id')} has been shipped. Track: {data.get('tracking_id')} - Inner Veda",
            NotificationEvent.ORDER_DELIVERED: f"Your order #{data.get('order_id')} has been delivered. Thank you for choosing Inner Veda!",
        }
        
        return messages.get(event, f"You have a notification from Inner Veda. {data.get('message', '')}")

class NotificationService:
    """Main notification service orchestrator"""
    
    def __init__(self):
        self.providers = {
            NotificationChannel.EMAIL: EmailProvider(),
            NotificationChannel.WHATSAPP: WhatsAppProvider(),
            NotificationChannel.SMS: SMSProvider(),
        }
        self.retry_attempts = 3
        self.retry_delay = 5  # seconds
    
    async def send_notification(self, request: NotificationRequest) -> Dict[str, Any]:
        """Send notification through specified channels"""
        results = {}
        
        for channel in request.channels:
            provider = self.providers.get(channel)
            if not provider:
                results[channel.value] = {"status": "failed", "error": "Provider not available"}
                continue
            
            # Send with retries
            result = await self._send_with_retry(provider, request)
            results[channel.value] = result
        
        return {
            "event": request.event.value,
            "recipient": request.recipient,
            "priority": request.priority.value,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _send_with_retry(self, provider: NotificationProvider, request: NotificationRequest) -> Dict[str, Any]:
        """Send notification with retry logic"""
        last_error = None
        
        for attempt in range(self.retry_attempts):
            try:
                result = await provider.send(request)
                if result.get("status") == "sent":
                    return result
                last_error = result.get("error", "Unknown error")
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
            
            if attempt < self.retry_attempts - 1:
                await asyncio.sleep(self.retry_delay)
        
        return {"status": "failed", "error": last_error, "attempts": self.retry_attempts}
    
    async def send_order_notification(self, event: NotificationEvent, order_data: Dict[str, Any], channels: List[NotificationChannel] = None) -> Dict[str, Any]:
        """Convenience method for order notifications"""
        if channels is None:
            channels = [NotificationChannel.EMAIL, NotificationChannel.WHATSAPP]
        
        request = NotificationRequest(
            event=event,
            channels=channels,
            recipient=order_data.get("customer_email") or order_data.get("customer_phone"),
            data=order_data,
            priority=NotificationPriority.HIGH if event == NotificationEvent.ORDER_PLACED else NotificationPriority.MEDIUM
        )
        
        return await self.send_notification(request)
    
    async def send_user_notification(self, event: NotificationEvent, user_data: Dict[str, Any], channels: List[NotificationChannel] = None) -> Dict[str, Any]:
        """Convenience method for user notifications"""
        if channels is None:
            channels = [NotificationChannel.EMAIL]
        
        request = NotificationRequest(
            event=event,
            channels=channels,
            recipient=user_data.get("email"),
            data=user_data,
            priority=NotificationPriority.MEDIUM
        )
        
        return await self.send_notification(request)
    
    async def send_admin_notification(self, event: NotificationEvent, admin_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send notification to admin"""
        admin_email = os.getenv("ADMIN_EMAIL", "hkchakravarty@gmail.com")
        
        request = NotificationRequest(
            event=event,
            channels=[NotificationChannel.EMAIL],
            recipient=admin_email,
            data=admin_data,
            priority=NotificationPriority.HIGH
        )
        
        return await self.send_notification(request)

# Global notification service instance
notification_service = NotificationService()

# Convenience functions for easy integration
async def notify_order_placed(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send order placed notification"""
    return await notification_service.send_order_notification(
        NotificationEvent.ORDER_PLACED, 
        order_data
    )

async def notify_order_shipped(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send order shipped notification"""
    return await notification_service.send_order_notification(
        NotificationEvent.ORDER_SHIPPED, 
        order_data
    )

async def notify_order_delivered(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send order delivered notification"""
    return await notification_service.send_order_notification(
        NotificationEvent.ORDER_DELIVERED, 
        order_data
    )

async def notify_contact_form(contact_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send contact form notification"""
    return await notification_service.send_user_notification(
        NotificationEvent.CONTACT_FORM,
        contact_data,
        [NotificationChannel.EMAIL]
    )

async def notify_admin_new_order(order_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send new order notification to admin"""
    return await notification_service.send_admin_notification(
        NotificationEvent.NEW_ORDER_ADMIN,
        order_data
    )