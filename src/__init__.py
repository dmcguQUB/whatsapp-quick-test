"""
WhatsApp Fitness Bot - Main Package
"""
__version__ = '1.0.0'

# Create app instance for gunicorn
from src.app import create_app
app = create_app()
