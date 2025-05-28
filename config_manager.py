#!/usr/bin/env python3
import os
import json
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureConfigManager:
    def __init__(self, config_file=".email_config.enc"):
        self.config_file = config_file
        self.salt_file = ".config_salt"
        
    def _generate_key(self, password: str, salt: bytes) -> bytes:
        """Generate encryption key from password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _get_or_create_salt(self) -> bytes:
        """Get existing salt or create new one."""
        if os.path.exists(self.salt_file):
            with open(self.salt_file, 'rb') as f:
                return f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
            return salt
    
    def save_credentials(self, email: str, password: str, master_password: str = None):
        """Save email credentials securely."""
        if not master_password:
            master_password = getpass.getpass("Enter a master password to encrypt your credentials: ")
        
        # Create salt and encryption key
        salt = self._get_or_create_salt()
        key = self._generate_key(master_password, salt)
        fernet = Fernet(key)
        
        # Prepare credentials
        credentials = {
            "email": email,
            "password": password
        }
        
        # Encrypt and save
        encrypted_data = fernet.encrypt(json.dumps(credentials).encode())
        with open(self.config_file, 'wb') as f:
            f.write(encrypted_data)
        
        print(f"✅ Credentials saved securely to {self.config_file}")
        print("💡 You can also set environment variables EMAIL_ADDRESS and EMAIL_PASSWORD")
    
    def load_credentials(self, master_password: str = None) -> tuple:
        """Load email credentials. Returns (email, password) or (None, None) if not found."""
        
        # First, try environment variables (most secure for local dev)
        env_email = os.getenv('EMAIL_ADDRESS')
        env_password = os.getenv('EMAIL_PASSWORD')
        if env_email and env_password:
            return env_email, env_password
        
        # If no env vars, try encrypted file
        if not os.path.exists(self.config_file):
            return None, None
        
        if not master_password:
            master_password = getpass.getpass("Enter master password to decrypt credentials: ")
        
        try:
            # Load salt and create key
            salt = self._get_or_create_salt()
            key = self._generate_key(master_password, salt)
            fernet = Fernet(key)
            
            # Decrypt credentials
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            
            return credentials['email'], credentials['password']
            
        except Exception as e:
            print(f"❌ Failed to decrypt credentials: {e}")
            return None, None
    
    def delete_credentials(self):
        """Delete stored credentials."""
        files_to_remove = [self.config_file, self.salt_file]
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️  Removed {file}")
        print("✅ All stored credentials deleted")
    
    def credentials_exist(self) -> bool:
        """Check if credentials are available (env vars or encrypted file)."""
        env_available = bool(os.getenv('EMAIL_ADDRESS') and os.getenv('EMAIL_PASSWORD'))
        file_available = os.path.exists(self.config_file)
        return env_available or file_available

def setup_credentials():
    """Interactive setup for email credentials."""
    config_manager = SecureConfigManager()
    
    print("🔐 Email Credentials Setup")
    print("=" * 40)
    print("Choose your preferred method:")
    print("1. Environment Variables (Recommended)")
    print("2. Encrypted File Storage")
    print("3. Both (Most Flexible)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    email = input("Enter your email address: ").strip()
    password = getpass.getpass("Enter your app password: ")
    
    if choice in ['1', '3']:
        print("\n📝 Setting up environment variables...")
        print("Add these lines to your shell profile (~/.zshrc, ~/.bashrc, etc.):")
        print(f"export EMAIL_ADDRESS='{email}'")
        print(f"export EMAIL_PASSWORD='{password}'")
        print("\nThen run: source ~/.zshrc (or restart terminal)")
        
        # For immediate use in current session
        os.environ['EMAIL_ADDRESS'] = email
        os.environ['EMAIL_PASSWORD'] = password
        print("✅ Environment variables set for current session")
    
    if choice in ['2', '3']:
        print("\n🔒 Setting up encrypted file storage...")
        config_manager.save_credentials(email, password)
    
    print("\n🎉 Setup complete! Your credentials are now stored securely.")

if __name__ == "__main__":
    setup_credentials() 