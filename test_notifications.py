"""
Comprehensive notification service testing script
"""

import asyncio
import httpx
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@innerveda.in"  # Change to your test email
TEST_PHONE = "+919876543210"  # Change to your test phone

class NotificationTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    async def test_api_health(self):
        """Test if API is running"""
        print("🔍 Testing API Health...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    print("✅ API is healthy")
                    return True
                else:
                    print(f"❌ API health check failed: {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Failed to connect to API: {str(e)}")
            return False
    
    async def test_notification_endpoints(self):
        """Test notification endpoints availability"""
        print("\n🔍 Testing Notification Endpoints...")
        
        endpoints = [
            "/notifications/templates",
            "/notifications/stats",
            "/notifications/logs",
            "/notifications/queue"
        ]
        
        async with httpx.AsyncClient() as client:
            for endpoint in endpoints:
                try:
                    response = await client.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 200:
                        print(f"✅ {endpoint} - Working")
                    else:
                        print(f"⚠️ {endpoint} - Status: {response.status_code}")
                except Exception as e:
                    print(f"❌ {endpoint} - Error: {str(e)}")
    
    async def test_send_order_notification(self):
        """Test order placed notification"""
        print("\n📦 Testing Order Placed Notification...")
        
        order_data = {
            "order_id": f"TEST{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "customer_name": "Test Customer",
            "customer_email": TEST_EMAIL,
            "customer_phone": TEST_PHONE,
            "amount": 1299,
            "order_date": datetime.now().strftime("%B %d, %Y")
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/notifications/send/order-placed",
                    json=order_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Order notification sent: {result}")
                    return True
                else:
                    print(f"❌ Order notification failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Order notification error: {str(e)}")
            return False
    
    async def test_send_contact_form_notification(self):
        """Test contact form notification"""
        print("\n💬 Testing Contact Form Notification...")
        
        contact_data = {
            "name": "Test User",
            "email": TEST_EMAIL,
            "phone": TEST_PHONE,
            "category": "product",
            "subject": "Test inquiry about A-ZEN",
            "message": "This is a test message for the notification service.",
            "reference_id": f"REF{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/notifications/send/contact-form",
                    json=contact_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Contact form notification sent: {result}")
                    return True
                else:
                    print(f"❌ Contact form notification failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Contact form notification error: {str(e)}")
            return False
    
    async def test_custom_notification(self):
        """Test custom notification"""
        print("\n🔧 Testing Custom Notification...")
        
        notification_data = {
            "event": "user_registered",
            "channels": ["email"],
            "recipient": TEST_EMAIL,
            "data": {
                "user_name": "Test User",
                "welcome_message": "Welcome to Inner Veda!",
                "login_url": "https://innerveda.in/sign-in"
            },
            "priority": "medium"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/notifications/send",
                    json=notification_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Custom notification sent: {result}")
                    return True
                else:
                    print(f"❌ Custom notification failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Custom notification error: {str(e)}")
            return False
    
    async def test_user_preferences(self):
        """Test user preference management"""
        print("\n⚙️ Testing User Preferences...")
        
        test_user_id = "test_user_notifications"
        
        try:
            async with httpx.AsyncClient() as client:
                # Get preferences
                response = await client.get(f"{self.base_url}/notifications/preferences/{test_user_id}")
                
                if response.status_code == 200:
                    preferences = response.json()
                    print(f"✅ Got user preferences: {preferences.get('preferences', {})}")
                    
                    # Update preferences
                    updated_preferences = {
                        "preferences": {
                            "email_enabled": True,
                            "sms_enabled": False,
                            "whatsapp_enabled": True,
                            "push_enabled": False,
                            "order_notifications": True,
                            "marketing_notifications": False,
                            "support_notifications": True,
                            "inventory_notifications": True
                        }
                    }
                    
                    update_response = await client.put(
                        f"{self.base_url}/notifications/preferences/{test_user_id}",
                        json=updated_preferences
                    )
                    
                    if update_response.status_code == 200:
                        print("✅ User preferences updated successfully")
                        return True
                    else:
                        print(f"❌ Failed to update preferences: {update_response.status_code}")
                        return False
                else:
                    print(f"❌ Failed to get preferences: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ User preferences test error: {str(e)}")
            return False
    
    async def test_notification_stats(self):
        """Test notification statistics"""
        print("\n📊 Testing Notification Statistics...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/notifications/stats?days=7")
                
                if response.status_code == 200:
                    stats = response.json()
                    print(f"✅ Notification Stats:")
                    print(f"   📧 Total Sent: {stats.get('total_sent', 0)}")
                    print(f"   ❌ Total Failed: {stats.get('total_failed', 0)}")
                    print(f"   📈 Success Rate: {stats.get('success_rate', 0)}%")
                    print(f"   📱 By Channel: {stats.get('by_channel', {})}")
                    print(f"   🎯 By Event: {stats.get('by_event', {})}")
                    return True
                else:
                    print(f"❌ Failed to get stats: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Stats test error: {str(e)}")
            return False
    
    async def test_notification_logs(self):
        """Test notification logs"""
        print("\n📋 Testing Notification Logs...")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/notifications/logs?limit=10")
                
                if response.status_code == 200:
                    logs_data = response.json()
                    logs = logs_data.get('logs', [])
                    print(f"✅ Retrieved {len(logs)} notification logs")
                    
                    if logs:
                        latest_log = logs[0]
                        print(f"   Latest: {latest_log.get('event')} to {latest_log.get('recipient')} - {latest_log.get('status')}")
                    
                    return True
                else:
                    print(f"❌ Failed to get logs: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Logs test error: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all notification tests"""
        print("🚀 Starting Comprehensive Notification Service Tests...")
        print("=" * 60)
        
        tests = [
            ("API Health", self.test_api_health),
            ("Endpoints", self.test_notification_endpoints),
            ("Order Notification", self.test_send_order_notification),
            ("Contact Form Notification", self.test_send_contact_form_notification),
            ("Custom Notification", self.test_custom_notification),
            ("User Preferences", self.test_user_preferences),
            ("Statistics", self.test_notification_stats),
            ("Logs", self.test_notification_logs),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results[test_name] = result
            except Exception as e:
                print(f"❌ {test_name} failed with exception: {str(e)}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Notification service is working perfectly.")
        else:
            print("⚠️ Some tests failed. Check the configuration and logs above.")
        
        return results

async def main():
    """Main test runner"""
    print(f"📧 Test Email: {TEST_EMAIL}")
    print(f"📱 Test Phone: {TEST_PHONE}")
    print(f"🌐 API URL: {API_BASE_URL}")
    print("\n⚠️ Make sure your backend server is running with: uvicorn app.main:app --reload")
    
    input("\nPress Enter to start testing...")
    
    tester = NotificationTester(API_BASE_URL)
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())