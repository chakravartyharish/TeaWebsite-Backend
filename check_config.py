"""
Configuration checker for notification service
"""

import os
from dotenv import load_dotenv

def check_notification_config():
    """Check notification service configuration"""
    load_dotenv()
    
    print("🔍 Checking Notification Service Configuration...")
    print("=" * 50)
    
    # Email configuration
    print("\n📧 EMAIL CONFIGURATION:")
    email_vars = {
        "EMAIL_HOST": os.getenv("EMAIL_HOST"),
        "EMAIL_PORT": os.getenv("EMAIL_PORT"), 
        "EMAIL_USER": os.getenv("EMAIL_USER"),
        "EMAIL_PASSWORD": "***" if os.getenv("EMAIL_PASSWORD") else None,
        "EMAIL_FROM": os.getenv("EMAIL_FROM"),
        "EMAIL_FROM_NAME": os.getenv("EMAIL_FROM_NAME"),
        "ADMIN_EMAIL": os.getenv("ADMIN_EMAIL")
    }
    
    for key, value in email_vars.items():
        status = "✅" if value else "❌"
        print(f"  {status} {key}: {value or 'NOT SET'}")
    
    # WhatsApp configuration
    print("\n💬 WHATSAPP CONFIGURATION:")
    whatsapp_vars = {
        "WHATSAPP_TOKEN": "***" if os.getenv("WHATSAPP_TOKEN") else None,
        "WHATSAPP_PHONE_ID": os.getenv("WHATSAPP_PHONE_ID")
    }
    
    for key, value in whatsapp_vars.items():
        status = "✅" if value else "❌"
        print(f"  {status} {key}: {value or 'NOT SET'}")
    
    # SMS configuration (optional)
    print("\n📱 SMS CONFIGURATION (Optional):")
    sms_vars = {
        "SMS_API_KEY": "***" if os.getenv("SMS_API_KEY") else None,
        "SMS_SENDER_ID": os.getenv("SMS_SENDER_ID")
    }
    
    for key, value in sms_vars.items():
        status = "✅" if value else "⚠️"
        print(f"  {status} {key}: {value or 'NOT SET'}")
    
    # MongoDB configuration
    print("\n🗄️ DATABASE CONFIGURATION:")
    db_vars = {
        "MONGODB_URL": "***" if os.getenv("MONGODB_URL") else None,
        "MONGODB_DB": os.getenv("MONGODB_DB")
    }
    
    for key, value in db_vars.items():
        status = "✅" if value else "❌"
        print(f"  {status} {key}: {value or 'NOT SET'}")
    
    # Summary
    print("\n" + "=" * 50)
    
    email_configured = all(os.getenv(var) for var in ["EMAIL_HOST", "EMAIL_USER", "EMAIL_PASSWORD", "EMAIL_FROM"])
    whatsapp_configured = all(os.getenv(var) for var in ["WHATSAPP_TOKEN", "WHATSAPP_PHONE_ID"])
    db_configured = all(os.getenv(var) for var in ["MONGODB_URL", "MONGODB_DB"])
    
    print("📊 CONFIGURATION STATUS:")
    print(f"  {'✅' if email_configured else '❌'} Email Service: {'Ready' if email_configured else 'Needs Configuration'}")
    print(f"  {'✅' if whatsapp_configured else '❌'} WhatsApp Service: {'Ready' if whatsapp_configured else 'Needs Configuration'}")
    print(f"  {'✅' if db_configured else '❌'} Database: {'Ready' if db_configured else 'Needs Configuration'}")
    
    if email_configured and db_configured:
        print("\n🎉 Core notification service is ready for testing!")
    else:
        print("\n⚠️ Please configure the missing variables in your .env file")
    
    print("\n📝 NEXT STEPS:")
    if not email_configured:
        print("  1. Set up Gmail App Password (see instructions above)")
        print("  2. Add EMAIL_* variables to .env file")
    if not whatsapp_configured:
        print("  3. Set up WhatsApp Business API")
        print("  4. Add WHATSAPP_* variables to .env file")
    if db_configured and (email_configured or whatsapp_configured):
        print("  5. Run: python test_notifications.py")

if __name__ == "__main__":
    check_notification_config()