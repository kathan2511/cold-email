#!/usr/bin/env python3
import os
from config_manager import SecureConfigManager

def quick_setup():
    """Quick setup with your actual credentials."""
    
    # Your actual credentials - replace these with your real values
    EMAIL = "khrutwi@gmail.com"
    APP_PASSWORD = "vqphiszeukwopfpg"  # Replace with your actual app password
    
    print("🔐 Setting up email credentials...")
    
    # Method 1: Environment Variables (Recommended)
    os.environ['EMAIL_ADDRESS'] = EMAIL
    os.environ['EMAIL_PASSWORD'] = APP_PASSWORD
    print(f"✅ Environment variables set for current session")
    print(f"📧 Email: {EMAIL}")
    
    # Method 2: Also save to encrypted file as backup
    config_manager = SecureConfigManager()
    master_password = "your_master_password_123"  # You can change this
    config_manager.save_credentials(EMAIL, APP_PASSWORD, master_password)
    
    print("\n🎉 Credentials setup complete!")
    print("Your credentials are now stored securely using both methods.")
    
    # Test the credentials
    print("\n🧪 Testing credential retrieval...")
    email, password = config_manager.load_credentials(master_password)
    if email:
        print(f"✅ Successfully retrieved: {email}")
    else:
        print("❌ Failed to retrieve credentials")

if __name__ == "__main__":
    quick_setup() 