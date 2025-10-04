#!/usr/bin/env python3
"""
WhatsApp Fitness Bot - Application Entry Point
"""
from src.app import create_app
from src.config import Config

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
