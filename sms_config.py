"""
SMS Configuration for ALYVON Rental Management System
Update these settings based on your SMS gateway provider

IMPORTANT: Credentials should be set via .env file or environment variables.
See .env.example for template.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SMS Gateway Configuration
# Options: 'twilio', 'africastalking', 'smsgh', 'custom', 'disabled'
# IMPORTANT: Set credentials via .env file or environment variables (see .env.example)
SMS_GATEWAY = os.getenv('SMS_GATEWAY', 'twilio')  # Set to 'disabled' to turn off SMS

# Twilio Configuration (if using Twilio)
# Load from .env file - DO NOT put credentials directly in this file!
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')  # Your Twilio phone number

# Africa's Talking Configuration (if using Africa's Talking)
AT_API_KEY = os.getenv('AT_API_KEY', '')
AT_USERNAME = os.getenv('AT_USERNAME', '')

# SMSGH Configuration (if using SMSGH)
SMSGH_API_KEY = os.getenv('SMSGH_API_KEY', '')
SMSGH_API_URL = os.getenv('SMSGH_API_URL', 'https://api.smsgh.com/v3/messages')

# Custom SMS Gateway Configuration
CUSTOM_SMS_API_URL = os.getenv('CUSTOM_SMS_API_URL', '')
CUSTOM_SMS_API_KEY = os.getenv('CUSTOM_SMS_API_KEY', '')

# SMS Settings
SMS_SENDER_ID = os.getenv('SMS_SENDER_ID', 'ALYVON')
SMS_ENABLED = SMS_GATEWAY != 'disabled' and SMS_GATEWAY != ''

# Company Information for Receipts
COMPANY_NAME = "ALYVON Rentals"
COMPANY_PHONE = "0264509400"  # Add your company phone number
COMPANY_EMAIL = "info@alyvonrentals.com"  # Add your company email
COMPANY_ADDRESS = "P.O. Box GA-143-2769, Accra, Ghana"  # Add your company address

def get_sms_config():
    """Get SMS configuration based on selected gateway"""
    if SMS_GATEWAY == 'twilio':
        return {
            'gateway': 'twilio',
            'api_key': TWILIO_ACCOUNT_SID,
            'api_secret': TWILIO_AUTH_TOKEN,
            'sender_id': TWILIO_PHONE_NUMBER
        }
    elif SMS_GATEWAY == 'africastalking':
        return {
            'gateway': 'africastalking',
            'api_key': AT_USERNAME,
            'api_secret': AT_API_KEY,
            'sender_id': SMS_SENDER_ID
        }
    elif SMS_GATEWAY == 'smsgh':
        return {
            'gateway': 'smsgh',
            'api_key': SMSGH_API_KEY,
            'api_secret': '',
            'sender_id': SMS_SENDER_ID,
            'api_url': SMSGH_API_URL
        }
    elif SMS_GATEWAY == 'custom':
        return {
            'gateway': 'custom',
            'api_key': CUSTOM_SMS_API_KEY,
            'api_secret': '',
            'sender_id': SMS_SENDER_ID,
            'api_url': CUSTOM_SMS_API_URL
        }
    else:
        return {
            'gateway': 'disabled',
            'api_key': '',
            'api_secret': '',
            'sender_id': SMS_SENDER_ID
        }


