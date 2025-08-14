"""
Seed notification templates and test data for the notification service
"""

import asyncio
from datetime import datetime, timedelta
from app.core.mongodb import connect_to_mongo
from app.models.notification_models import (
    NotificationTemplate, 
    NotificationEvent, 
    NotificationChannel,
    UserNotificationPreferences,
    NotificationPreferences
)

async def seed_notification_templates():
    """Seed default notification templates"""
    
    templates = [
        # Email templates
        {
            "name": "order_placed_email",
            "event": NotificationEvent.ORDER_PLACED,
            "channel": NotificationChannel.EMAIL,
            "subject": "🍃 Order Confirmation - Inner Veda #{{order_id}}",
            "body": """Dear {{customer_name}},

Thank you for your order! Your wellness journey continues with Inner Veda.

Order Details:
- Order ID: {{order_id}}
- Total Amount: ₹{{amount}}
- Order Date: {{order_date}}

We'll notify you once your order is shipped. For any questions, contact us at innervedacare@gmail.com or +91 9113920980.

Thank you for choosing Inner Veda!

Best regards,
The Inner Veda Team""",
            "html_body": """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #2d5a45, #3b7057); padding: 30px; text-align: center; color: white;">
                    <h1 style="margin: 0;">🍃 Inner Veda</h1>
                    <p>Order Confirmation</p>
                </div>
                <div style="padding: 30px; background: white;">
                    <h2>Dear {{customer_name}},</h2>
                    <p>Thank you for your order! Your wellness journey continues with Inner Veda.</p>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3>Order Details</h3>
                        <p><strong>Order ID:</strong> {{order_id}}</p>
                        <p><strong>Total Amount:</strong> ₹{{amount}}</p>
                        <p><strong>Order Date:</strong> {{order_date}}</p>
                    </div>
                    <p>We'll notify you once your order is shipped.</p>
                    <p>Thank you for choosing Inner Veda!</p>
                </div>
            </div>
            """,
            "variables": ["customer_name", "order_id", "amount", "order_date"]
        },
        {
            "name": "order_shipped_email",
            "event": NotificationEvent.ORDER_SHIPPED,
            "channel": NotificationChannel.EMAIL,
            "subject": "📦 Your Order is on the way! - Inner Veda #{{order_id}}",
            "body": """Dear {{customer_name}},

Great news! Your order #{{order_id}} has been shipped and is on its way to you.

Shipping Details:
- Tracking ID: {{tracking_id}}
- Expected Delivery: {{delivery_date}}
- Track your order: {{tracking_url}}

We hope you'll love your Inner Veda products!

Best regards,
The Inner Veda Team""",
            "html_body": """
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
            """,
            "variables": ["customer_name", "order_id", "tracking_id", "delivery_date", "tracking_url"]
        },
        {
            "name": "contact_form_email",
            "event": NotificationEvent.CONTACT_FORM,
            "channel": NotificationChannel.EMAIL,
            "subject": "🍃 Thank you for contacting Inner Veda",
            "body": """Dear {{name}},

Thank you for contacting us regarding {{category}}.

We've received your inquiry and our team will respond within 24 hours.

Reference ID: {{reference_id}}
Subject: {{subject}}

For urgent matters, please call us at +91 9113920980.

Thank you for choosing Inner Veda!

Best regards,
The Inner Veda Team""",
            "html_body": """
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
            """,
            "variables": ["name", "category", "reference_id", "subject"]
        },
    ]
    
    print("Seeding notification templates...")
    
    for template_data in templates:
        try:
            # Check if template already exists
            existing = await NotificationTemplate.find_one({
                "event": template_data["event"],
                "channel": template_data["channel"]
            })
            
            if existing:
                print(f"Template {template_data['name']} already exists, updating...")
                existing.subject = template_data["subject"]
                existing.body = template_data["body"]
                existing.html_body = template_data.get("html_body")
                existing.variables = template_data["variables"]
                existing.updated_at = datetime.utcnow()
                await existing.save()
            else:
                print(f"Creating template {template_data['name']}...")
                template = NotificationTemplate(**template_data)
                await template.insert()
                
        except Exception as e:
            print(f"Error seeding template {template_data['name']}: {str(e)}")
    
    print("Notification templates seeded successfully!")

async def seed_user_preferences():
    """Seed test user notification preferences"""
    
    test_users = [
        {
            "user_id": "test_user_1",
            "email": "test1@innerveda.in",
            "phone": "+919876543210",
            "preferences": NotificationPreferences(
                email_enabled=True,
                whatsapp_enabled=True,
                sms_enabled=False,
                order_notifications=True,
                marketing_notifications=True,
                support_notifications=True
            )
        },
        {
            "user_id": "test_user_2", 
            "email": "test2@innerveda.in",
            "phone": "+919876543211",
            "preferences": NotificationPreferences(
                email_enabled=True,
                whatsapp_enabled=False,
                sms_enabled=True,
                order_notifications=True,
                marketing_notifications=False,
                support_notifications=True
            )
        }
    ]
    
    print("Seeding user notification preferences...")
    
    for user_data in test_users:
        try:
            existing = await UserNotificationPreferences.find_one({
                "user_id": user_data["user_id"]
            })
            
            if existing:
                print(f"User preferences for {user_data['user_id']} already exist, skipping...")
                continue
                
            user_prefs = UserNotificationPreferences(**user_data)
            await user_prefs.insert()
            print(f"Created preferences for user {user_data['user_id']}")
            
        except Exception as e:
            print(f"Error seeding preferences for {user_data['user_id']}: {str(e)}")
    
    print("User notification preferences seeded successfully!")

async def test_notification_system():
    """Test the notification system with sample data"""
    from app.services.notification_service import notification_service, NotificationEvent, NotificationChannel, NotificationPriority
    from app.services.notification_service import NotificationRequest as ServiceNotificationRequest
    
    print("Testing notification system...")
    
    # Test order placed notification
    try:
        print("Testing order placed notification...")
        order_data = {
            "order_id": "TEST001",
            "customer_name": "Test Customer",
            "customer_email": "test@innerveda.in",
            "customer_phone": "+919876543210",
            "amount": 1299,
            "order_date": datetime.now().strftime("%B %d, %Y")
        }
        
        request = ServiceNotificationRequest(
            event=NotificationEvent.ORDER_PLACED,
            channels=[NotificationChannel.EMAIL],
            recipient=order_data["customer_email"],
            data=order_data,
            priority=NotificationPriority.HIGH
        )
        
        result = await notification_service.send_notification(request)
        print(f"Order notification result: {result}")
        
    except Exception as e:
        print(f"Error testing order notification: {str(e)}")
    
    # Test contact form notification
    try:
        print("Testing contact form notification...")
        contact_data = {
            "name": "Test User",
            "email": "test@innerveda.in",
            "category": "product",
            "subject": "Test inquiry",
            "message": "This is a test message",
            "reference_id": "REF001"
        }
        
        request = ServiceNotificationRequest(
            event=NotificationEvent.CONTACT_FORM,
            channels=[NotificationChannel.EMAIL],
            recipient=contact_data["email"],
            data=contact_data,
            priority=NotificationPriority.MEDIUM
        )
        
        result = await notification_service.send_notification(request)
        print(f"Contact form notification result: {result}")
        
    except Exception as e:
        print(f"Error testing contact form notification: {str(e)}")
    
    print("Notification system testing completed!")

async def main():
    """Main function to run all seeding operations"""
    print("Starting notification service seeding...")
    
    try:
        # Connect to MongoDB
        await connect_to_mongo()
        
        # Seed templates
        await seed_notification_templates()
        
        # Seed user preferences
        await seed_user_preferences()
        
        # Test the system
        await test_notification_system()
        
        print("Notification service seeding completed successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        raise e

if __name__ == "__main__":
    asyncio.run(main())