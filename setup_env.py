"""
Setup script to create .env file with Twilio credentials
Run this once on each PC to set up your environment variables
"""
import os

def create_env_file():
    """Create .env file with Twilio credentials"""
    print("Enter your Twilio credentials:")
    account_sid = input("Twilio Account SID: ").strip()
    auth_token = input("Twilio Auth Token: ").strip()
    phone_number = input("Twilio Phone Number (e.g., +12526296448): ").strip()
    
    if not account_sid or not auth_token or not phone_number:
        print("❌ All fields are required!")
        return
    
    env_content = f"""# ALYVON Rental Management System - Environment Variables
# This file contains your actual credentials - DO NOT COMMIT TO GIT!

# SMS Gateway Configuration
SMS_GATEWAY=twilio

# Twilio Configuration
TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_PHONE_NUMBER={phone_number}
"""
    
    env_file = '.env'
    
    if os.path.exists(env_file):
        response = input(f"{env_file} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled. Keeping existing .env file.")
            return
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file} file successfully!")
        print("⚠️  Remember: This file is NOT committed to Git (it's in .gitignore)")
        print("📝 You can edit it manually if needed.")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    print("Setting up .env file for ALYVON Rental Management System...")
    print()
    create_env_file()

