"""
WhatsApp Fitness Bot - Main Flask Application
"""
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'

    app.run(host='0.0.0.0', port=port, debug=debug)
