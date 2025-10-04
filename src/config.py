"""
Configuration management for WhatsApp Fitness Bot
"""
import os

# Load environment variables from .env files (only in development)
# In production (Railway), env vars are injected directly
try:
    from dotenv import load_dotenv
    load_dotenv('.env.local')
    load_dotenv()
except ImportError:
    # python-dotenv not installed (shouldn't happen, but safe fallback)
    pass


class Config:
    """Base configuration"""

    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') != 'production'

    # Server
    PORT = int(os.getenv('PORT', 5001))  # Default 5001 to avoid macOS AirPlay Receiver conflict
    HOST = '0.0.0.0'

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', '')

    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '')

    # Anthropic Claude
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

    # Application
    APP_URL = os.getenv('APP_URL', 'http://localhost:5001')

    @staticmethod
    def validate():
        """Validate required configuration"""
        required_vars = [
            'TWILIO_ACCOUNT_SID',
            'TWILIO_AUTH_TOKEN',
            'TWILIO_WHATSAPP_NUMBER',
            'ANTHROPIC_API_KEY'
        ]

        missing = [var for var in required_vars if not os.getenv(var)]

        if missing:
            print(f"Warning: Missing environment variables: {', '.join(missing)}")
            print("The app will run but some features may not work.")
