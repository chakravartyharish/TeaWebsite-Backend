"""
Enhanced template engine for notification service using Jinja2
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, BaseLoader, Template
import logging

logger = logging.getLogger(__name__)

class NotificationTemplateEngine:
    """Enhanced template engine with Jinja2 features"""
    
    def __init__(self):
        # Create Jinja2 environment
        self.env = Environment(
            loader=BaseLoader(),
            autoescape=True,  # Prevent XSS attacks
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self._add_custom_filters()
    
    def _add_custom_filters(self):
        """Add custom Jinja2 filters for notifications"""
        
        def currency_format(value, currency="₹"):
            """Format currency with Indian formatting"""
            try:
                amount = float(value)
                return f"{currency}{amount:,.0f}"
            except (ValueError, TypeError):
                return f"{currency}{value}"
        
        def phone_format(value):
            """Format phone number"""
            if not value:
                return ""
            # Remove non-digits
            digits = ''.join(filter(str.isdigit, str(value)))
            if len(digits) == 10:
                return f"+91 {digits[:5]} {digits[5:]}"
            elif len(digits) == 12 and digits.startswith('91'):
                return f"+91 {digits[2:7]} {digits[7:]}"
            return value
        
        def date_format(value, format="%B %d, %Y"):
            """Format date"""
            if isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                except:
                    return value
            if isinstance(value, datetime):
                return value.strftime(format)
            return value
        
        def truncate_words(value, length=50):
            """Truncate text to word boundary"""
            if not value or len(value) <= length:
                return value
            return value[:length].rsplit(' ', 1)[0] + '...'
        
        def order_status_emoji(status):
            """Get emoji for order status"""
            status_emojis = {
                'placed': '📦',
                'confirmed': '✅',
                'shipped': '🚚',
                'delivered': '🎉',
                'cancelled': '❌'
            }
            return status_emojis.get(str(status).lower(), '📋')
        
        # Register filters
        self.env.filters['currency'] = currency_format
        self.env.filters['phone'] = phone_format
        self.env.filters['date'] = date_format
        self.env.filters['truncate_words'] = truncate_words
        self.env.filters['order_emoji'] = order_status_emoji
    
    def render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Render template with data"""
        try:
            template = self.env.from_string(template_content)
            return template.render(**data)
        except Exception as e:
            logger.error(f"Template rendering failed: {str(e)}")
            # Fallback to simple replacement
            return self._fallback_render(template_content, data)
    
    def _fallback_render(self, template_content: str, data: Dict[str, Any]) -> str:
        """Fallback rendering with simple string replacement"""
        result = template_content
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result
    
    def get_base_email_template(self) -> str:
        """Get base email template with Jinja2 features"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ email_title | default("Inner Veda Notification") }}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8f9fa; font-family: Arial, sans-serif;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #2d5a45, #3b7057); padding: 30px; text-align: center; color: white;">
            <h1 style="margin: 0; font-size: 28px;">🍃 Inner Veda</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">{{ email_subtitle | default("Ancient wisdom for modern living") }}</p>
        </div>
        
        <!-- Content -->
        <div style="padding: 30px;">
            {% block content %}
            <h2>Hello {{ customer_name | default("Valued Customer") }},</h2>
            <p>{{ message | default("Thank you for choosing Inner Veda!") }}</p>
            {% endblock %}
        </div>
        
        <!-- Footer -->
        <div style="background-color: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #e9ecef;">
            <p style="margin: 0; color: #6c757d; font-size: 14px;">
                <strong>🍃 innerveda.in</strong> • Made with ❤️ for your wellness journey
            </p>
            <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 12px;">
                Contact us: <a href="mailto:innervedacare@gmail.com" style="color: #2d5a45;">innervedacare@gmail.com</a> • 
                <a href="tel:+919113920980" style="color: #2d5a45;">+91 9113920980</a>
            </p>
            {% if unsubscribe_url %}
            <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 11px;">
                <a href="{{ unsubscribe_url }}" style="color: #6c757d;">Unsubscribe</a>
            </p>
            {% endif %}
        </div>
    </div>
</body>
</html>
        '''
    
    def get_order_template(self) -> str:
        """Enhanced order template with Jinja2 features"""
        return '''
{% extends base_template %}
{% block content %}
<h2>Hello {{ customer_name | title }},</h2>

{% if event == 'order_placed' %}
<p>🎉 Thank you for your order! Your wellness journey continues with Inner Veda.</p>
{% elif event == 'order_shipped' %}
<p>🚚 Great news! Your order is on its way to you.</p>
{% elif event == 'order_delivered' %}
<p>🎉 Your order has been delivered! We hope you love your Inner Veda products.</p>
{% endif %}

<!-- Order Details Card -->
<div style="background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; margin: 20px 0;">
    <h3 style="margin-top: 0; color: #2d5a45;">{{ order_status | order_emoji }} Order Details</h3>
    
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Order ID:</td>
            <td style="padding: 8px 0; font-family: monospace; background: #e9ecef; padding: 4px 8px; border-radius: 4px;">{{ order_id }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Total Amount:</td>
            <td style="padding: 8px 0; font-size: 18px; font-weight: bold; color: #2d5a45;">{{ amount | currency }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Order Date:</td>
            <td style="padding: 8px 0;">{{ order_date | date }}</td>
        </tr>
        {% if tracking_id %}
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Tracking ID:</td>
            <td style="padding: 8px 0; font-family: monospace;">{{ tracking_id }}</td>
        </tr>
        {% endif %}
        {% if delivery_date %}
        <tr>
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Expected Delivery:</td>
            <td style="padding: 8px 0;">{{ delivery_date | date }}</td>
        </tr>
        {% endif %}
    </table>
</div>

{% if order_items %}
<!-- Order Items -->
<div style="background-color: #fff; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; margin: 20px 0;">
    <h3 style="margin-top: 0; color: #2d5a45;">📦 Order Items</h3>
    <table style="width: 100%; border-collapse: collapse;">
        <thead>
            <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Product</th>
                <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">Qty</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Price</th>
            </tr>
        </thead>
        <tbody>
            {% for item in order_items %}
            <tr style="border-bottom: 1px solid #e9ecef;">
                <td style="padding: 10px;">
                    <strong>{{ item.name }}</strong>
                    {% if item.description %}
                    <br><small style="color: #6c757d;">{{ item.description | truncate_words(30) }}</small>
                    {% endif %}
                </td>
                <td style="padding: 10px; text-align: center;">{{ item.quantity }}</td>
                <td style="padding: 10px; text-align: right; font-weight: bold;">{{ item.price | currency }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endif %}

{% if tracking_url %}
<div style="text-align: center; margin: 30px 0;">
    <a href="{{ tracking_url }}" style="background-color: #2d5a45; color: white; padding: 12px 24px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
        📱 Track Your Order
    </a>
</div>
{% endif %}

{% if customer_phone %}
<p style="background-color: #e8f5e8; padding: 15px; border-radius: 8px; border-left: 4px solid #2d5a45;">
    💬 We'll also send updates to {{ customer_phone | phone }}
</p>
{% endif %}

<p>Thank you for choosing Inner Veda for your wellness journey!</p>
{% endblock %}
        '''
    
    def get_contact_template(self) -> str:
        """Enhanced contact form template"""
        return '''
{% extends base_template %}
{% block content %}
<h2>Dear {{ name | title }},</h2>

<p>Thank you for contacting us regarding <strong>{{ category | title }}</strong>.</p>

<p>We've received your inquiry and our specialized team will respond within 
{% if category in ['order', 'health', 'wholesale'] %}6-12 hours{% else %}24 hours{% endif %}.</p>

<!-- Inquiry Details -->
<div style="background-color: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; margin: 20px 0;">
    <h3 style="margin-top: 0; color: #2d5a45;">📋 Your Inquiry Details</h3>
    
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 8px 0; font-weight: bold; color: #495057; width: 30%;">Reference ID:</td>
            <td style="padding: 8px 0; font-family: monospace; background: #e9ecef; padding: 4px 8px; border-radius: 4px;">{{ reference_id }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Category:</td>
            <td style="padding: 8px 0; text-transform: capitalize;">{{ category }}</td>
        </tr>
        <tr style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Subject:</td>
            <td style="padding: 8px 0;">{{ subject }}</td>
        </tr>
        <tr>
            <td style="padding: 8px 0; font-weight: bold; color: #495057;">Submitted:</td>
            <td style="padding: 8px 0;">{{ timestamp | date('%B %d, %Y at %I:%M %p') }}</td>
        </tr>
    </table>
</div>

{% if category in ['order', 'health', 'wholesale'] %}
<!-- High Priority Notice -->
<div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 15px; margin: 20px 0; text-align: center;">
    <strong style="color: #856404;">🔥 High Priority Inquiry</strong>
    <p style="margin: 5px 0 0 0; color: #856404;">Your {{ category }} inquiry will be prioritized for faster response.</p>
</div>
{% endif %}

<p>For urgent matters, please don't hesitate to call us at 
<a href="tel:+919113920980" style="color: #2d5a45; font-weight: bold;">+91 9113920980</a>.</p>

<p>Thank you for choosing Inner Veda!</p>
{% endblock %}
        '''

# Global template engine instance
template_engine = NotificationTemplateEngine()