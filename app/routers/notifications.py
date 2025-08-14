"""
Notification API endpoints
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Depends
from fastapi.responses import JSONResponse

from app.services.notification_service import (
    notification_service,
    NotificationRequest as ServiceNotificationRequest,
    NotificationEvent,
    NotificationChannel,
    NotificationPriority
)
from app.models.notification_models import (
    NotificationRequest,
    NotificationResponse,
    PreferencesUpdateRequest,
    TemplateCreateRequest,
    NotificationStatsResponse,
    NotificationTemplate,
    NotificationLog,
    UserNotificationPreferences,
    NotificationQueue,
    NotificationStatus
)

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/send", response_model=NotificationResponse)
async def send_notification(
    request: NotificationRequest,
    background_tasks: BackgroundTasks
):
    """Send a notification immediately"""
    try:
        # Convert API request to service request
        service_request = ServiceNotificationRequest(
            event=request.event,
            channels=request.channels,
            recipient=request.recipient,
            data=request.data,
            priority=request.priority,
            scheduled_at=request.scheduled_at
        )
        
        if request.scheduled_at and request.scheduled_at > datetime.utcnow():
            # Schedule for later
            queue_item = NotificationQueue(
                event=request.event,
                channel=request.channels[0],  # Use first channel for queue
                recipient=request.recipient,
                priority=request.priority,
                data=request.data,
                scheduled_at=request.scheduled_at
            )
            await queue_item.insert()
            
            return NotificationResponse(
                success=True,
                message="Notification scheduled successfully",
                notification_id=str(queue_item.id)
            )
        else:
            # Send immediately in background
            background_tasks.add_task(
                _send_notification_task,
                service_request
            )
            
            return NotificationResponse(
                success=True,
                message="Notification queued for immediate delivery"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

@router.post("/send/order-placed")
async def send_order_placed_notification(
    order_data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Send order placed notification"""
    try:
        background_tasks.add_task(
            _send_order_notification_task,
            NotificationEvent.ORDER_PLACED,
            order_data
        )
        
        return {"success": True, "message": "Order placed notification sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send/order-shipped")
async def send_order_shipped_notification(
    order_data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Send order shipped notification"""
    try:
        background_tasks.add_task(
            _send_order_notification_task,
            NotificationEvent.ORDER_SHIPPED,
            order_data
        )
        
        return {"success": True, "message": "Order shipped notification sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send/contact-form")
async def send_contact_form_notification(
    contact_data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Send contact form notification"""
    try:
        background_tasks.add_task(
            _send_contact_notification_task,
            contact_data
        )
        
        return {"success": True, "message": "Contact form notification sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences/{user_id}")
async def get_user_preferences(user_id: str):
    """Get user notification preferences"""
    try:
        preferences = await UserNotificationPreferences.find_one(
            UserNotificationPreferences.user_id == user_id
        )
        
        if not preferences:
            # Return default preferences
            return {
                "user_id": user_id,
                "preferences": {
                    "email_enabled": True,
                    "sms_enabled": False,
                    "whatsapp_enabled": True,
                    "push_enabled": False,
                    "order_notifications": True,
                    "marketing_notifications": False,
                    "support_notifications": True,
                    "inventory_notifications": False
                },
                "unsubscribed_events": [],
                "unsubscribed_channels": []
            }
        
        return preferences.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/preferences/{user_id}")
async def update_user_preferences(
    user_id: str,
    request: PreferencesUpdateRequest
):
    """Update user notification preferences"""
    try:
        preferences = await UserNotificationPreferences.find_one(
            UserNotificationPreferences.user_id == user_id
        )
        
        if preferences:
            # Update existing preferences
            preferences.preferences = request.preferences
            if request.unsubscribed_events:
                preferences.unsubscribed_events = request.unsubscribed_events
            if request.unsubscribed_channels:
                preferences.unsubscribed_channels = request.unsubscribed_channels
            preferences.updated_at = datetime.utcnow()
            await preferences.save()
        else:
            # Create new preferences
            preferences = UserNotificationPreferences(
                user_id=user_id,
                preferences=request.preferences,
                unsubscribed_events=request.unsubscribed_events or [],
                unsubscribed_channels=request.unsubscribed_channels or []
            )
            await preferences.insert()
        
        return {"success": True, "message": "Preferences updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_templates(
    event: Optional[NotificationEvent] = None,
    channel: Optional[NotificationChannel] = None,
    active_only: bool = True
):
    """Get notification templates"""
    try:
        filters = {}
        if event:
            filters["event"] = event
        if channel:
            filters["channel"] = channel
        if active_only:
            filters["is_active"] = True
        
        templates = await NotificationTemplate.find(filters).to_list()
        return templates
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/templates")
async def create_template(request: TemplateCreateRequest):
    """Create a new notification template"""
    try:
        # Check if template already exists for this event/channel combination
        existing = await NotificationTemplate.find_one({
            "event": request.event,
            "channel": request.channel
        })
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Template already exists for {request.event}/{request.channel}"
            )
        
        template = NotificationTemplate(
            name=request.name,
            event=request.event,
            channel=request.channel,
            subject=request.subject,
            body=request.body,
            html_body=request.html_body,
            variables=request.variables
        )
        await template.insert()
        
        return {"success": True, "message": "Template created successfully", "id": str(template.id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_notification_logs(
    recipient: Optional[str] = None,
    event: Optional[NotificationEvent] = None,
    channel: Optional[NotificationChannel] = None,
    status: Optional[NotificationStatus] = None,
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0)
):
    """Get notification logs"""
    try:
        filters = {}
        if recipient:
            filters["recipient"] = recipient
        if event:
            filters["event"] = event
        if channel:
            filters["channel"] = channel
        if status:
            filters["status"] = status
        
        logs = await NotificationLog.find(filters).skip(offset).limit(limit).sort("-created_at").to_list()
        total = await NotificationLog.find(filters).count()
        
        return {
            "logs": logs,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=NotificationStatsResponse)
async def get_notification_stats(
    days: int = Query(7, ge=1, le=365),
    event: Optional[NotificationEvent] = None,
    channel: Optional[NotificationChannel] = None
):
    """Get notification statistics"""
    try:
        since = datetime.utcnow() - timedelta(days=days)
        
        filters = {"created_at": {"$gte": since}}
        if event:
            filters["event"] = event
        if channel:
            filters["channel"] = channel
        
        # Get total counts
        total_logs = await NotificationLog.find(filters).to_list()
        total_sent = len([log for log in total_logs if log.status == NotificationStatus.SENT])
        total_failed = len([log for log in total_logs if log.status == NotificationStatus.FAILED])
        
        success_rate = (total_sent / len(total_logs)) * 100 if total_logs else 0
        
        # Get stats by channel
        by_channel = {}
        for log in total_logs:
            channel_name = log.channel.value
            by_channel[channel_name] = by_channel.get(channel_name, 0) + 1
        
        # Get stats by event
        by_event = {}
        for log in total_logs:
            event_name = log.event.value
            by_event[event_name] = by_event.get(event_name, 0) + 1
        
        # Get recent activity (last 10 notifications)
        recent_logs = await NotificationLog.find(filters).sort("-created_at").limit(10).to_list()
        recent_activity = [
            {
                "event": log.event.value,
                "channel": log.channel.value,
                "recipient": log.recipient,
                "status": log.status.value,
                "created_at": log.created_at.isoformat()
            }
            for log in recent_logs
        ]
        
        return NotificationStatsResponse(
            total_sent=total_sent,
            total_failed=total_failed,
            success_rate=round(success_rate, 2),
            by_channel=by_channel,
            by_event=by_event,
            recent_activity=recent_activity
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/queue")
async def get_notification_queue(
    status: Optional[NotificationStatus] = None,
    limit: int = Query(50, le=200)
):
    """Get scheduled notifications queue"""
    try:
        filters = {}
        if status:
            filters["status"] = status
        
        queue_items = await NotificationQueue.find(filters).sort("scheduled_at").limit(limit).to_list()
        return {"queue": queue_items, "total": len(queue_items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-queue")
async def process_notification_queue(background_tasks: BackgroundTasks):
    """Process pending notifications in queue"""
    try:
        background_tasks.add_task(_process_queue_task)
        return {"success": True, "message": "Queue processing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Background task functions
async def _send_notification_task(request: ServiceNotificationRequest):
    """Background task to send notification"""
    try:
        result = await notification_service.send_notification(request)
        
        # Log the notification
        for channel, channel_result in result.get("results", {}).items():
            log = NotificationLog(
                event=request.event,
                channel=NotificationChannel(channel),
                recipient=request.recipient,
                status=NotificationStatus.SENT if channel_result.get("status") == "sent" else NotificationStatus.FAILED,
                priority=request.priority,
                body=str(request.data),
                data=request.data,
                provider_response=channel_result,
                error_message=channel_result.get("error"),
                sent_at=datetime.utcnow() if channel_result.get("status") == "sent" else None
            )
            await log.insert()
            
    except Exception as e:
        print(f"Background notification task failed: {str(e)}")

async def _send_order_notification_task(event: NotificationEvent, order_data: Dict[str, Any]):
    """Background task for order notifications"""
    try:
        await notification_service.send_order_notification(event, order_data)
    except Exception as e:
        print(f"Order notification task failed: {str(e)}")

async def _send_contact_notification_task(contact_data: Dict[str, Any]):
    """Background task for contact form notifications"""
    try:
        await notification_service.send_user_notification(
            NotificationEvent.CONTACT_FORM,
            contact_data,
            [NotificationChannel.EMAIL]
        )
    except Exception as e:
        print(f"Contact notification task failed: {str(e)}")

async def _process_queue_task():
    """Background task to process notification queue"""
    try:
        now = datetime.utcnow()
        
        # Get pending notifications that are due
        due_notifications = await NotificationQueue.find({
            "status": NotificationStatus.SCHEDULED,
            "scheduled_at": {"$lte": now}
        }).to_list()
        
        for notification in due_notifications:
            try:
                # Send the notification
                service_request = ServiceNotificationRequest(
                    event=notification.event,
                    channels=[notification.channel],
                    recipient=notification.recipient,
                    data=notification.data,
                    priority=notification.priority
                )
                
                result = await notification_service.send_notification(service_request)
                
                # Update queue item
                notification.status = NotificationStatus.SENT
                notification.processed_at = datetime.utcnow()
                await notification.save()
                
                # Log the notification
                log = NotificationLog(
                    event=notification.event,
                    channel=notification.channel,
                    recipient=notification.recipient,
                    status=NotificationStatus.SENT,
                    priority=notification.priority,
                    body=str(notification.data),
                    data=notification.data,
                    sent_at=datetime.utcnow()
                )
                await log.insert()
                
            except Exception as e:
                # Mark as failed and increment retry count
                notification.status = NotificationStatus.FAILED
                notification.error_message = str(e)
                notification.retry_count += 1
                await notification.save()
        
        # Clean up expired notifications
        await NotificationQueue.find({
            "expires_at": {"$lt": now}
        }).delete()
        
    except Exception as e:
        print(f"Queue processing task failed: {str(e)}")