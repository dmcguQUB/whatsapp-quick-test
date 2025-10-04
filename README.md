# WhatsApp Fitness Bot

AI-powered fitness coaching delivered via WhatsApp that discovers individual failure patterns and adapts workout plans to improve consistency over a 14-day experiment.

## Overview

This bot uses Claude AI to:
- Discover why each user specifically fails at fitness routines
- Adapt workout plans to their chaotic life patterns
- Deliver personalized coaching via WhatsApp (no app download needed)

**Experiment Duration:** 14 days
**Initial Users:** 20 participants
**Tech Stack:** Python, Flask, PostgreSQL, Twilio WhatsApp API, Claude AI

## Prerequisites

- Python 3.11.7 or higher
- PostgreSQL database
- Twilio account with WhatsApp Business API access
- Anthropic Claude API key

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd bmad-whatsapp
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# OR use .env.local (both are supported)
cp .env.example .env.local
```

Edit `.env` (or `.env.local`) with your actual credentials.

📚 **For detailed step-by-step instructions on obtaining each credential, see [Environment Setup Guide](docs/environment_setup.md)**

Quick reference:
- **FLASK_SECRET_KEY**: Generate a secure random key
- **DATABASE_URL**: Your PostgreSQL connection string
- **TWILIO_ACCOUNT_SID**: From Twilio Console
- **TWILIO_AUTH_TOKEN**: From Twilio Console
- **TWILIO_WHATSAPP_NUMBER**: Your Twilio WhatsApp number
- **ANTHROPIC_API_KEY**: Your Claude API key

### 5. Run the application

```bash
python run.py
```

The server will start on `http://localhost:5001`

### 6. Test the health endpoint

```bash
curl http://localhost:5001/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "whatsapp-fitness-bot"
}
```

## Project Structure

```
bmad-whatsapp/
├── src/                        # Main application code
│   ├── __init__.py
│   ├── app.py                 # Flask app factory
│   ├── config.py              # Configuration management
│   ├── models/                # Database models (future)
│   │   └── __init__.py
│   ├── services/              # Business logic services (future)
│   │   └── __init__.py        # - twilio_service.py
│   │                          # - claude_service.py
│   │                          # - scheduler_service.py
│   ├── handlers/              # Message handlers (future)
│   │   └── __init__.py        # - onboarding.py
│   │                          # - checkin.py
│   └── utils/                 # Utility functions (future)
│       └── __init__.py        # - parsers.py
│                              # - message_formatter.py
├── tests/                     # Test files
│   └── __init__.py
├── docs/                      # Documentation
│   ├── prd.md                # Product Requirements Document
│   ├── implementation_plan.md # Development roadmap
│   └── changelog.md          # Change history
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python version specification
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## API Endpoints

- `GET /` - Root endpoint (service info)
- `GET /health` - Health check endpoint
- `POST /webhook/whatsapp` - Twilio WhatsApp webhook (receives incoming messages)

## Deployment

This application is designed to deploy on Railway:

1. Connect GitHub repository to Railway
2. Add PostgreSQL database service
3. Configure environment variables in Railway dashboard
4. Railway will auto-deploy on push to main branch

## Development Workflow

1. Create feature branch: `git checkout -b ticket-X.X-feature-name`
2. Implement feature
3. Test locally
4. Update `docs/changelog.md`
5. Commit and push
6. Create pull request to main

## Documentation

- [Product Requirements Document](docs/prd.md)
- [Implementation Plan](docs/implementation_plan.md)
- [Environment Setup Guide](docs/environment_setup.md) - **Step-by-step instructions for all credentials**
- [Changelog](docs/changelog.md)

## Tech Stack Details

- **Flask 3.0.0** - Web framework
- **SQLAlchemy 2.0.23** - ORM
- **PostgreSQL** - Database (via psycopg2-binary)
- **Twilio 8.10.0** - WhatsApp messaging
- **Anthropic SDK >=0.39.0** - Claude AI integration
- **APScheduler 3.10.4** - Scheduled messages
- **Flask-Migrate 4.0.5** - Database migrations

## License

Proprietary - BMad Fitness Experiment
