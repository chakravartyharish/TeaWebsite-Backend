"""
MongoDB models for notification system
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from beanie import Document
from pymongo import IndexModel

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SCHEDULED = "scheduled"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    PUSH = "push"

class NotificationEvent(str, Enum):
    ORDER_PLACED = "order_placed"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    ORDER_CANCELLED = "order_cancelled"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    USER_REGISTERED = "user_registered"
    CONTACT_FORM = "contact_form"
    CART_ABANDONED = "cart_abandoned"
    PRODUCT_RESTOCK = "product_restock"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationPreferences(BaseModel):
    """User notification preferences"""
    email_enabled: bool = True
    sms_enabled: bool = False
    whatsapp_enabled: bool = True
    push_enabled: bool = False
    
    # Event-specific preferences
    order_notifications: bool = True
    marketing_notifications: bool = False
    support_notifications: bool = True
    inventory_notifications: bool = False

class NotificationTemplate(Document):
    """Notification template document"""
    name: str = Field(..., description="Template name/identifier")
    event: NotificationEvent = Field(..., description="Event this template is for")
    channel: NotificationChannel = Field(..., description="Notification channel")
    subject: str = Field(..., description="Template subject/title")
    body: str = Field(..., description="Template body content")
    html_body: Optional[str] = Field(None, description="HTML version of body")
    variables: List[str] = Field(default_factory=list, description="Template variables")
    is_active: bool = Field(default=True, description="Whether template is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "notification_templates"
        indexes = [
            IndexModel([("event", 1), ("channel", 1)], unique=True),
            IndexModel([("name", 1)]),
            IndexModel([("is_active", 1)])
        ]

class NotificationLog(Document):
    """Log of sent notifications"""
    event: NotificationEvent = Field(..., description="Event that triggered notification")
    channel: NotificationChannel = Field(..., description="Channel used")
    recipient: str = Field(..., description="Recipient identifier")
    status: NotificationStatus = Field(..., description="Notification status")
    priority: NotificationPriority = Field(..., description="Notification priority")
    
    # Content
    subject: Optional[str] = Field(None, description="Notification subject")
    body: str = Field(..., description="Notification body")
    data: Dict[str, Any] = Field(default_factory=dict, description="Template data used")
    
    # Metadata
    template_id: Optional[str] = Field(None, description="Template used")
    provider_response: Optional[Dict[str, Any]] = Field(None, description="Provider response")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    retry_count: int = Field(default=0, description="Number of retry attempts")
    
    # Timestamps
    scheduled_at: Optional[datetime] = Field(None, description="When notification was scheduled")
    sent_at: Optional[datetime] = Field(None, description="When notification was sent")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "notification_logs"
        indexes = [
            IndexModel([("event", 1), ("channel", 1)]),
            IndexModel([("recipient", 1)]),
            IndexModel([("status", 1)]),
            IndexModel([("created_at", -1)]),
            IndexModel([("sent_at", -1)]),
            IndexModel([("scheduled_at", 1)])
        ]

class UserNotificationPreferences(Document):
    """User-specific notification preferences"""
    user_id: str = Field(..., description="User identifier")
    email: Optional[str] = Field(None, description="User email")
    phone: Optional[str] = Field(None, description="User phone")
    
    preferences: NotificationPreferences = Field(default_factory=NotificationPreferences)
    
    # Subscription management
    unsubscribed_events: List[NotificationEvent] = Field(default_factory=list)
    unsubscribed_channels: List[NotificationChannel] = Field(default_factory=list)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "user_notification_preferences"
        indexes = [
            IndexModel([("user_id", 1)], unique=True),
            IndexModel([("email", 1)]),
            IndexModel([("phone", 1)])
        ]

class NotificationQueue(Document):
    """Queue for scheduled notifications"""
    event: NotificationEvent = Field(..., description="Event to trigger")
    channel: NotificationChannel = Field(..., description="Channel to use")
    recipient: str = Field(..., description="Recipient identifier")
    priority: NotificationPriority = Field(..., description="Notification priority")
    
    data: Dict[str, Any] = Field(default_factory=dict, description="Template data")
    template_id: Optional[str] = Field(None, description="Specific template to use")
    
    scheduled_at: datetime = Field(..., description="When to send notification")
    expires_at: Optional[datetime] = Field(None, description="When notification expires")
    
    # Processing status
    status: NotificationStatus = Field(default=NotificationStatus.SCHEDULED)
    processed_at: Optional[datetime] = Field(None, description="When notification was processed")
    error_message: Optional[str] = Field(None, description="Error if processing failed")
    retry_count: int = Field(default=0, description="Number of processing attempts")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "notification_queue"
        indexes = [
            IndexModel([("scheduled_at", 1), ("status", 1)]),
            IndexModel([("priority", 1), ("scheduled_at", 1)]),
            IndexModel([("status", 1)]),
            IndexModel([("expires_at", 1)])
        ]

# Request/Response models for API
class NotificationRequest(BaseModel):
    """API request for sending notification"""
    event: NotificationEvent
    channels: List[NotificationChannel]
    recipient: str
    data: Dict[str, Any]
    priority: NotificationPriority = NotificationPriority.MEDIUM
    scheduled_at: Optional[datetime] = None

class NotificationResponse(BaseModel):
    """API response for notification request"""
    success: bool
    message: str
    notification_id: Optional[str] = None
    results: Dict[str, Any] = {}

class PreferencesUpdateRequest(BaseModel):
    """Request to update notification preferences"""
    preferences: NotificationPreferences
    unsubscribed_events: Optional[List[NotificationEvent]] = None
    unsubscribed_channels: Optional[List[NotificationChannel]] = None

class TemplateCreateRequest(BaseModel):
    """Request to create notification template"""
    name: str
    event: NotificationEvent
    channel: NotificationChannel
    subject: str
    body: str
    html_body: Optional[str] = None
    variables: List[str] = []

class NotificationStatsResponse(BaseModel):
    """Notification statistics response"""
    total_sent: int
    total_failed: int
    success_rate: float
    by_channel: Dict[str, int]
    by_event: Dict[str, int]
    recent_activity: List[Dict[str, Any]]