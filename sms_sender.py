"""
SMS Sender for ALYVON Rental Management System
Supports multiple SMS gateway providers
"""
import requests
import os
from typing import Optional, Dict

class SMSSender:
    def __init__(self):
        """Initialize SMS sender with configuration from environment or config"""
        # Default SMS gateway configuration
        # Can be overridden via environment variables or config file
        self.gateway = os.getenv('SMS_GATEWAY', 'disabled')  # Options: twilio, africastalking, smsgh, custom
        self.api_key = os.getenv('SMS_API_KEY', '')
        self.api_secret = os.getenv('SMS_API_SECRET', '')
        self.sender_id = os.getenv('SMS_SENDER_ID', 'ALYVON')
        self.api_url = os.getenv('SMS_API_URL', '')
        
    def send_sms(self, phone_number: str, message: str, receipt_path: Optional[str] = None) -> Dict[str, bool]:
        """
        Send SMS to phone number
        
        Args:
            phone_number: Phone number (with country code, e.g., +233XXXXXXXXX for Ghana)
            message: SMS message text
            receipt_path: Optional path to PDF receipt (for MMS support in future)
        
        Returns:
            Dictionary with 'success' (bool) and 'message' (str) keys
        """
        if not phone_number:
            return {'success': False, 'message': 'Phone number is required'}
        
        if not message:
            return {'success': False, 'message': 'Message is required'}
        
        # Clean phone number
        phone_number = phone_number.strip().replace(' ', '').replace('-', '')
        
        # Add country code if not present (assuming Ghana +233)
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                phone_number = '+233' + phone_number[1:]
            elif phone_number.startswith('233'):
                phone_number = '+' + phone_number
            else:
                phone_number = '+233' + phone_number
        
        try:
            if self.gateway == 'twilio':
                return self._send_via_twilio(phone_number, message)
            elif self.gateway == 'africastalking':
                return self._send_via_africastalking(phone_number, message)
            elif self.gateway == 'smsgh':
                return self._send_via_smsgh(phone_number, message)
            elif self.gateway == 'custom':
                return self._send_via_custom(phone_number, message)
            else:
                return {'success': False, 'message': f'Unknown SMS gateway: {self.gateway}'}
        except Exception as e:
            return {'success': False, 'message': f'Error sending SMS: {str(e)}'}
    
    def _send_via_twilio(self, phone_number: str, message: str) -> Dict[str, bool]:
        """Send SMS via Twilio"""
        if not self.api_key or not self.api_secret:
            return {'success': False, 'message': 'Twilio API credentials not configured'}
        
        account_sid = self.api_key
        auth_token = self.api_secret
        twilio_phone = self.sender_id  # Your Twilio phone number
        
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)
            
            message_obj = client.messages.create(
                body=message,
                from_=twilio_phone,
                to=phone_number
            )
            
            return {'success': True, 'message': f'SMS sent successfully. SID: {message_obj.sid}'}
        except ImportError:
            return {'success': False, 'message': 'Twilio library not installed. Run: pip install twilio'}
        except Exception as e:
            return {'success': False, 'message': f'Twilio error: {str(e)}'}
    
    def _send_via_africastalking(self, phone_number: str, message: str) -> Dict[str, bool]:
        """Send SMS via Africa's Talking"""
        if not self.api_key or not self.api_secret:
            return {'success': False, 'message': 'Africa\'s Talking API credentials not configured'}
        
        username = self.api_key
        api_key = self.api_secret
        
        url = "https://api.africastalking.com/version1/messaging"
        headers = {
            "ApiKey": api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        data = {
            "username": username,
            "to": phone_number,
            "message": message,
            "from": self.sender_id
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 201:
                return {'success': True, 'message': 'SMS sent successfully via Africa\'s Talking'}
            else:
                return {'success': False, 'message': f'Africa\'s Talking error: {response.text}'}
        except Exception as e:
            return {'success': False, 'message': f'Africa\'s Talking error: {str(e)}'}
    
    def _send_via_smsgh(self, phone_number: str, message: str) -> Dict[str, bool]:
        """Send SMS via SMSGH (Ghana-based)"""
        if not self.api_key:
            return {'success': False, 'message': 'SMSGH API key not configured'}
        
        api_key = self.api_key
        api_url = self.api_url or "https://api.smsgh.com/v3/messages"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "From": self.sender_id,
            "To": phone_number,
            "Content": message,
            "Type": "text"
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data)
            if response.status_code in [200, 201]:
                return {'success': True, 'message': 'SMS sent successfully via SMSGH'}
            else:
                return {'success': False, 'message': f'SMSGH error: {response.text}'}
        except Exception as e:
            return {'success': False, 'message': f'SMSGH error: {str(e)}'}
    
    def _send_via_custom(self, phone_number: str, message: str) -> Dict[str, bool]:
        """Send SMS via custom HTTP API"""
        if not self.api_url:
            return {'success': False, 'message': 'Custom SMS API URL not configured'}
        
        try:
            # Custom API format - adjust based on your provider
            # This is a template - modify according to your SMS gateway's API
            data = {
                "phone": phone_number,
                "message": message,
                "sender": self.sender_id
            }
            
            response = requests.post(
                self.api_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                return {'success': True, 'message': 'SMS sent successfully'}
            else:
                return {'success': False, 'message': f'Custom API error: {response.text}'}
        except Exception as e:
            return {'success': False, 'message': f'Custom API error: {str(e)}'}
    
    def send_receipt_notification(self, phone_number: str, customer_name: str, 
                                 rental_id: str, total_amount: float, 
                                 return_date: str, currency: str = "GHS") -> Dict[str, bool]:
        """
        Send a formatted receipt notification SMS
        
        Args:
            phone_number: Customer phone number
            customer_name: Customer name
            rental_id: Rental ID
            total_amount: Total rental amount
            return_date: Return date
            currency: Currency symbol
        
        Returns:
            Dictionary with 'success' and 'message' keys
        """
        message = f"""Hello {customer_name},

Your rental receipt #{rental_id} is ready!

Total Amount: {currency} {total_amount:.2f}
Return Date: {return_date}

Thank you for choosing ALYVON Rentals!"""
        
        return self.send_sms(phone_number, message)

