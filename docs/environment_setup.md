# Environment Setup Guide

This guide provides step-by-step instructions for obtaining and configuring all required environment variables for the WhatsApp Fitness Bot.

## Table of Contents

1. [Flask Secret Key](#1-flask-secret-key)
2. [Database URL (PostgreSQL)](#2-database-url-postgresql)
3. [Twilio WhatsApp Configuration](#3-twilio-whatsapp-configuration)
4. [Anthropic Claude API Key](#4-anthropic-claude-api-key)
5. [Application URL](#5-application-url)
6. [Final Configuration](#6-final-configuration)

---

## 1. Flask Secret Key

The Flask secret key is used for session management and security. Generate a cryptographically strong random key.

### Generate Secret Key (Recommended Method)

**Using Python secrets module (Python 3.6+):**

```bash
python -c 'import secrets; print(secrets.token_hex())'
```

**Output example:**
```
192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf
```

**Alternative method using os.urandom:**

```bash
python -c "import os; print(os.urandom(24).hex())"
```

### Configuration

Copy the generated key to your `.env` file:

```bash
FLASK_SECRET_KEY=192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf
```

⚠️ **Security Note:** Never commit this key to version control or share it publicly.

---

## 2. Database URL (PostgreSQL)

You need a PostgreSQL database for local development. In production, Railway will automatically provide this.

### Option A: Local PostgreSQL Installation

#### **For macOS:**

**Method 1: Homebrew (Recommended)**

```bash
# Install PostgreSQL
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Create database
createdb whatsapp_fitness_bot
```

**Method 2: Postgres.app**

1. Download from [https://postgresapp.com/](https://postgresapp.com/)
2. Open the app - PostgreSQL server starts automatically
3. Click "Initialize" to create a new server
4. Open terminal and create database:
   ```bash
   createdb whatsapp_fitness_bot
   ```

#### **For Windows:**

1. Download installer from [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer (PostgreSQL 16 recommended)
3. During installation:
   - Set a password for the postgres user (remember this!)
   - Default port: 5432
   - Select default locale
4. Open pgAdmin or command prompt:
   ```sql
   CREATE DATABASE whatsapp_fitness_bot;
   ```

#### **For Linux:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres createdb whatsapp_fitness_bot
```

### Database URL Format

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/whatsapp_fitness_bot
```

**Default credentials:**
- **macOS/Linux:** `postgresql://your_username@localhost:5432/whatsapp_fitness_bot`
- **Windows:** `postgresql://postgres:your_password@localhost:5432/whatsapp_fitness_bot`

### Option B: Railway PostgreSQL (Production)

Railway automatically provides `DATABASE_URL` when you add a PostgreSQL service. No manual configuration needed in production.

---

## 3. Twilio WhatsApp Configuration

Twilio provides WhatsApp Business API integration. You'll need three values: Account SID, Auth Token, and WhatsApp Number.

### Step 1: Create Twilio Account

1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Sign up for a free account
3. Verify your email and phone number
4. Complete the onboarding questions

### Step 2: Get Account SID and Auth Token

1. Log in to [Twilio Console](https://console.twilio.com/)
2. On your dashboard, you'll see **Project Info** section
3. Find and copy:
   - **Account SID** (starts with `AC...`)
   - **Auth Token** (click eye icon to reveal, then copy)

**Example:**
```
Account SID: AC1234567890abcdef1234567890abcd
Auth Token: your_32_character_auth_token_here
```

⚠️ **Security Note:** If your Auth Token is exposed, regenerate it in the Console under "Project Info" → "Auth Token" → "Create new Auth Token"

### Step 3: Set Up WhatsApp Sandbox (For Testing)

The Twilio Sandbox allows testing without WhatsApp Business approval.

1. In Twilio Console, navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**
2. You'll see:
   - **Sandbox Number:** `+1 415 523 8886` (or your region's number)
   - **Your Sandbox Code:** `join <your-code>` (e.g., `join orange-tiger`)
3. Click **Agree to Terms** and **Confirm**

### Step 4: Join the Sandbox (For Testing)

On your phone:
1. Open WhatsApp
2. Send a message to `+1 415 523 8886`
3. Message content: `join your-sandbox-code` (e.g., `join orange-tiger`)
4. You'll receive confirmation: "Twilio Sandbox: ✅ You are all set!"

**Alternative:** Scan the QR code shown in the Twilio Console

### Step 5: Configure Webhook (After Deployment)

1. In Twilio Console → **Messaging** → **Try it out** → **Send a WhatsApp message**
2. Scroll to **Sandbox Configuration**
3. Set **"When a message comes in"** to: `https://your-app-url.railway.app/webhook/whatsapp`
4. Save configuration

### Configuration

Add to your `.env` file:

```bash
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcd
TWILIO_AUTH_TOKEN=your_32_character_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886
```

### Production WhatsApp Number

For production (beyond testing):
1. Request WhatsApp Business API access in Twilio Console
2. Submit business verification to Meta
3. Get approved sender number (can take 1-2 weeks)
4. Update `TWILIO_WHATSAPP_NUMBER` with your approved number

**Sandbox Limitations:**
- ⚠️ Only users who joined your sandbox can receive messages
- ⚠️ Sandbox expires after 3 days (users must rejoin)
- ⚠️ Rate limit: 1 message per 3 seconds
- ⚠️ Not for production use

---

## 4. Anthropic Claude API Key

Claude AI powers the pattern analysis and personalized workout generation.

### Step 1: Create Anthropic Account

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Click **Sign Up** (or **Sign In** if you have an account)
3. Sign up with:
   - Google account, or
   - Email and password
4. Verify your email address

### Step 2: Set Up Billing (Required for API Access)

1. After logging in, navigate to **Settings** → **Billing**
2. Click **Add Payment Method**
3. Enter credit card information
4. Add initial credits (minimum $5 recommended)
   - Claude Sonnet 4.5: ~$3 per million input tokens
   - For 20 users × 14 days: Expect ~$10-20 total usage

💡 **Note:** New accounts may receive free credits (~$5) to get started.

### Step 3: Generate API Key

1. In [Anthropic Console](https://console.anthropic.com/), go to **API Keys**
   - Or directly: [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Click **Create Key**
3. Enter a name: `WhatsApp Fitness Bot` (or any descriptive name)
4. Click **Create Key**
5. **IMPORTANT:** Copy the API key immediately - it won't be shown again!

**API Key format:**
```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Monitor Usage

1. Go to **Settings** → **Billing** → **Usage**
2. Track token usage and costs
3. Set up usage alerts (recommended):
   - Go to **Settings** → **Billing** → **Notifications**
   - Set alert at $10, $20, etc.

### Configuration

Add to your `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **Security Note:** Never commit API keys to Git. Keep them in `.env` which is in `.gitignore`.

---

## 5. Application URL

The application URL is used for webhook callbacks and external integrations.

### Local Development

```bash
APP_URL=http://localhost:5001
```

### Production (Railway)

After deploying to Railway:
1. Railway provides a public URL: `https://your-app-name.up.railway.app`
2. Update in Railway environment variables:
   ```bash
   APP_URL=https://your-app-name.up.railway.app
   ```

### For Local Testing with Twilio (Optional)

Use **ngrok** to expose your local server:

1. Install ngrok: [https://ngrok.com/download](https://ngrok.com/download)
2. Run ngrok:
   ```bash
   ngrok http 5001
   ```
3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
4. Use this as your `APP_URL` for local testing with Twilio webhooks

---

## 6. Final Configuration

### Create .env File

You can use either `.env` or `.env.local` (both are supported and ignored by Git).

1. Copy the example file:
   ```bash
   cp .env.example .env
   # OR
   cp .env.example .env.local
   ```

2. Edit `.env` (or `.env.local`) with your actual values:

   > **Note:** If both files exist, `.env.local` takes precedence. This is useful for local overrides.

```bash
# Flask Configuration
FLASK_ENV=development
PORT=5001
FLASK_SECRET_KEY=192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/whatsapp_fitness_bot

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcd
TWILIO_AUTH_TOKEN=your_32_character_auth_token_here
TWILIO_WHATSAPP_NUMBER=+14155238886

# Anthropic Claude API Configuration
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Application URL
APP_URL=http://localhost:5001
```

### Verify Configuration

Run the application:

```bash
python run.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5001
 * Debug mode: on
```

Test the health endpoint:

```bash
curl http://localhost:5001/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "whatsapp-fitness-bot"
}
```

### Troubleshooting

**Issue: Missing environment variables warning**
- Check that all variables in `.env` match `.env.example`
- Ensure no typos in variable names

**Issue: Database connection error**
- Verify PostgreSQL is running: `pg_isready`
- Check DATABASE_URL format and credentials

**Issue: Port 5001 already in use**
- Change PORT in `.env` to another value (e.g., 5002)
- Or stop the process using port 5001

**Issue: Twilio webhook not receiving messages**
- Ensure webhook URL is HTTPS (use ngrok for local testing)
- Check Twilio Console logs for delivery errors

---

## Railway Production Setup

When deploying to Railway:

1. **Add PostgreSQL Service** in Railway
   - Railway auto-populates `DATABASE_URL`

2. **Set Environment Variables** in Railway dashboard:
   ```
   FLASK_ENV=production
   FLASK_SECRET_KEY=<your-production-secret-key>
   TWILIO_ACCOUNT_SID=<your-twilio-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-token>
   TWILIO_WHATSAPP_NUMBER=<your-whatsapp-number>
   ANTHROPIC_API_KEY=<your-claude-api-key>
   APP_URL=https://your-app.up.railway.app
   ```

3. **Update Twilio Webhook** with your Railway URL:
   ```
   https://your-app.up.railway.app/webhook/whatsapp
   ```

---

## Security Checklist

- [ ] `.env` file is in `.gitignore` (already configured)
- [ ] Never commit API keys or secrets to Git
- [ ] Use different secret keys for development and production
- [ ] Regenerate tokens if accidentally exposed
- [ ] Monitor API usage and set billing alerts
- [ ] Use HTTPS for all webhook URLs in production
- [ ] Restrict database access to application only

---

## Cost Estimates (20 Users, 14 Days)

- **Twilio WhatsApp (Sandbox):** Free for testing
- **Twilio WhatsApp (Production):** ~$0.005 per message → ~$20-30 total
- **Claude API:** ~$10-20 for pattern analysis and responses
- **Railway Hosting:** Free tier sufficient for 20 users
- **PostgreSQL:** Included with Railway

**Total estimated cost for MVP:** $30-50

---

## Support Resources

- **Twilio Docs:** [https://www.twilio.com/docs/whatsapp](https://www.twilio.com/docs/whatsapp)
- **Anthropic Docs:** [https://docs.anthropic.com/](https://docs.anthropic.com/)
- **Flask Docs:** [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Railway Docs:** [https://docs.railway.app/](https://docs.railway.app/)
- **PostgreSQL Docs:** [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

---

**Last Updated:** October 2025
**Version:** 1.0
