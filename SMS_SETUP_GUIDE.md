# SMS Setup Guide for ALYVON Rental Management System

This guide will help you configure SMS sending for receipt notifications.

## 📱 Supported SMS Gateways

The system supports multiple SMS gateway providers:

1. **Twilio** (International - Recommended for testing)
2. **Africa's Talking** (Popular in Africa)
3. **SMSGH** (Ghana-based)
4. **Custom HTTP API** (Any SMS gateway with HTTP API)

## ⚙️ Configuration

### Step 1: Choose Your SMS Gateway

Edit `sms_config.py` and set your preferred gateway:

```python
SMS_GATEWAY = 'twilio'  # Options: 'twilio', 'africastalking', 'smsgh', 'custom', 'disabled'
```

### Step 2: Configure Gateway Credentials

#### Option A: Twilio (Recommended for International)

1. Sign up at [twilio.com](https://www.twilio.com)
2. Get your Account SID and Auth Token
3. Get a Twilio phone number

Edit `sms_config.py`:

```python
SMS_GATEWAY = 'twilio'
TWILIO_ACCOUNT_SID = 'your_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_auth_token_here'
TWILIO_PHONE_NUMBER = '+1234567890'  # Your Twilio phone number
```

**OR** set environment variables:

```cmd
set TWILIO_ACCOUNT_SID=your_account_sid
set TWILIO_AUTH_TOKEN=your_auth_token
set TWILIO_PHONE_NUMBER=+1234567890
```

**Install Twilio library:**
```cmd
pip install twilio
```

#### Option B: Africa's Talking (Popular in Africa)

1. Sign up at [africastalking.com](https://africastalking.com)
2. Get your API Key and Username

Edit `sms_config.py`:

```python
SMS_GATEWAY = 'africastalking'
AT_API_KEY = 'your_api_key_here'
AT_USERNAME = 'your_username_here'
SMS_SENDER_ID = 'ALYVON'
```

#### Option C: SMSGH (Ghana-based)

1. Sign up at [smsgh.com](https://smsgh.com)
2. Get your API Key

Edit `sms_config.py`:

```python
SMS_GATEWAY = 'smsgh'
SMSGH_API_KEY = 'your_api_key_here'
SMSGH_API_URL = 'https://api.smsgh.com/v3/messages'
SMS_SENDER_ID = 'ALYVON'
```

#### Option D: Custom HTTP API

If you have a custom SMS gateway, edit `sms_config.py`:

```python
SMS_GATEWAY = 'custom'
CUSTOM_SMS_API_URL = 'https://your-sms-api.com/send'
CUSTOM_SMS_API_KEY = 'your_api_key'
SMS_SENDER_ID = 'ALYVON'
```

You may need to modify `sms_sender.py` to match your API's format.

### Step 3: Disable SMS (If Not Using)

If you don't want to use SMS, simply:

```python
SMS_GATEWAY = 'disabled'
```

The receipt generation will still work, but SMS sending will be disabled.

## 🔒 Security Best Practices

**Never commit your API keys to Git!**

1. Use environment variables for sensitive data
2. Add `sms_config.py` to `.gitignore` (if it contains secrets)
3. Or use a separate `.env` file with `python-dotenv`

## 📝 Testing SMS

1. Create a test rental
2. Check "Send Receipt via SMS" checkbox
3. Make sure customer has a valid phone number
4. Create the rental
5. Check the success message for SMS status

## ⚠️ Troubleshooting

### "SMS is disabled" message
- Check that `SMS_GATEWAY` is not set to 'disabled'
- Verify API credentials are configured

### "SMS gateway not configured"
- Make sure API key and credentials are set in `sms_config.py`
- Check environment variables if using them

### "Phone number invalid"
- Phone numbers should include country code (e.g., +233XXXXXXXXX for Ghana)
- System auto-adds +233 if number starts with 0

### "Twilio library not installed"
- Run: `pip install twilio`

## 💡 Phone Number Format

The system automatically formats phone numbers:
- `0244123456` → `+233244123456` (Ghana)
- `233244123456` → `+233244123456`
- Already formatted numbers are used as-is

## 📞 Company Information for Receipts

Don't forget to update company info in `sms_config.py`:

```python
COMPANY_NAME = "ALYVON Rentals"
COMPANY_PHONE = "+233XXXXXXXXX"
COMPANY_EMAIL = "info@alyvonrentals.com"
COMPANY_ADDRESS = "Your Business Address"
```

This information will appear on the PDF receipts.

## ✅ Quick Setup Checklist

- [ ] Choose SMS gateway provider
- [ ] Get API credentials from provider
- [ ] Update `sms_config.py` with credentials
- [ ] Install required libraries (`pip install -r requirements.txt`)
- [ ] Update company information in `sms_config.py`
- [ ] Test with a sample rental
- [ ] Verify SMS is received

---

**Need Help?** Contact your SMS gateway provider's support for API documentation.


