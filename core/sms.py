"""
SMS and WhatsApp notification functions using Twilio
"""
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfile
import logging

logger = logging.getLogger(__name__)


def send_sms(phone_number, message):
    """
    Send SMS message using Twilio
    
    Args:
        phone_number: Phone number in E.164 format (e.g., +420123456789)
        message: Message text to send
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not getattr(settings, 'ENABLE_SMS_NOTIFICATIONS', False):
        logger.info('SMS notifications are disabled')
        return False
    
    if not getattr(settings, 'TWILIO_ACCOUNT_SID', None) or not getattr(settings, 'TWILIO_AUTH_TOKEN', None):
        logger.warning('Twilio credentials not configured')
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Ensure phone number is in E.164 format
        if not phone_number.startswith('+'):
            # Try to add country code (default to +420 for Czech Republic)
            phone_number = f'+420{phone_number.lstrip("0")}'
        
        twilio_phone = getattr(settings, 'TWILIO_PHONE_NUMBER', '')
        if not twilio_phone:
            logger.error('TWILIO_PHONE_NUMBER not configured')
            return False
        
        message_obj = client.messages.create(
            body=message,
            from_=twilio_phone,
            to=phone_number
        )
        
        logger.info(f'SMS sent successfully to {phone_number}: {message_obj.sid}')
        return True
        
    except ImportError:
        logger.error('Twilio library not installed. Install with: pip install twilio')
        return False
    except Exception as e:
        logger.error(f'Failed to send SMS to {phone_number}: {e}')
        return False


def send_whatsapp(phone_number, message):
    """
    Send WhatsApp message using Twilio WhatsApp Business API
    
    Args:
        phone_number: Phone number in E.164 format (e.g., +420123456789)
        message: Message text to send
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not getattr(settings, 'ENABLE_WHATSAPP_NOTIFICATIONS', False):
        logger.info('WhatsApp notifications are disabled')
        return False
    
    if not getattr(settings, 'TWILIO_ACCOUNT_SID', None) or not getattr(settings, 'TWILIO_AUTH_TOKEN', None):
        logger.warning('Twilio credentials not configured')
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Ensure phone number is in E.164 format and add whatsapp: prefix
        if not phone_number.startswith('whatsapp:'):
            if not phone_number.startswith('+'):
                # Try to add country code (default to +420 for Czech Republic)
                phone_number = f'+420{phone_number.lstrip("0")}'
            phone_number = f'whatsapp:{phone_number}'
        
        twilio_whatsapp = getattr(settings, 'TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        if not twilio_whatsapp:
            logger.error('TWILIO_WHATSAPP_NUMBER not configured')
            return False
        
        message_obj = client.messages.create(
            body=message,
            from_=twilio_whatsapp,
            to=phone_number
        )
        
        logger.info(f'WhatsApp message sent successfully to {phone_number}: {message_obj.sid}')
        return True
        
    except ImportError:
        logger.error('Twilio library not installed. Install with: pip install twilio')
        return False
    except Exception as e:
        logger.error(f'Failed to send WhatsApp message to {phone_number}: {e}')
        return False


def format_phone_number(phone_number):
    """
    Format phone number to E.164 format
    
    Args:
        phone_number: Phone number in various formats
    
    Returns:
        str: Phone number in E.164 format or None if invalid
    """
    if not phone_number:
        return None
    
    # Remove all non-digit characters except +
    cleaned = ''.join(c for c in phone_number if c.isdigit() or c == '+')
    
    # If it doesn't start with +, assume it's a local number
    if not cleaned.startswith('+'):
        # Default to Czech Republic (+420)
        cleaned = f'+420{cleaned.lstrip("0")}'
    
    return cleaned


