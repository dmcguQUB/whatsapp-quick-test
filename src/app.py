"""
WhatsApp Fitness Bot - Flask Application Factory
"""
from flask import Flask, request, jsonify
from src.config import Config


def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Validate configuration (optional - won't prevent startup)
    try:
        Config.validate()
    except Exception as e:
        print(f"Config validation warning: {e}")

    # Register routes
    register_routes(app)

    return app


def register_routes(app):
    """Register all application routes"""

    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for deployment monitoring"""
        return jsonify({
            'status': 'healthy',
            'service': 'whatsapp-fitness-bot'
        }), 200

    @app.route('/webhook/whatsapp', methods=['POST'])
    def whatsapp_webhook():
        """
        Twilio WhatsApp webhook endpoint
        Receives incoming messages from users
        """
        incoming_msg = request.form.get('Body', '').strip()
        user_id = request.form.get('From', '')

        # TODO: Implement message processing in future tickets
        app.logger.info(f"Received message from {user_id}: {incoming_msg}")

        # Return 200 OK immediately to prevent timeout
        return '', 200

    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint"""
        return jsonify({
            'service': 'WhatsApp Fitness Bot',
            'status': 'running',
            'version': '1.0.0'
        }), 200
