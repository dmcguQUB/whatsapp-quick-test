# Railway Deployment Guide

Complete step-by-step guide to deploy the WhatsApp Fitness Bot to Railway.

## Prerequisites

- GitHub account with this repository pushed
- Railway account (free tier available at https://railway.app)
- All environment variables ready (see Environment Setup Guide)

---

## Step 1: Create Railway Account & Project

### 1.1 Sign Up for Railway

1. Go to https://railway.app
2. Click **"Start a New Project"** or **"Login"**
3. Sign in with your GitHub account
4. Authorize Railway to access your GitHub repositories

### 1.2 Create New Project

1. Click **"New Project"** in Railway dashboard
2. Select **"Deploy from GitHub repo"**
3. Choose the repository: `bmad-whatsapp`
4. Railway will automatically detect it's a Python application

---

## Step 2: Add PostgreSQL Database

### 2.1 Add Database Service

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"**
3. Choose **"PostgreSQL"**
4. Railway will automatically:
   - Create a PostgreSQL instance
   - Generate `DATABASE_URL` environment variable
   - Link it to your application

### 2.2 Verify Database Connection

1. Click on the **PostgreSQL service** in your project
2. Go to **"Variables"** tab
3. You should see variables like:
   - `DATABASE_URL`
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`

**Note:** Railway automatically injects `DATABASE_URL` into your Flask app. No manual configuration needed!

---

## Step 3: Configure Environment Variables

### 3.1 Add Application Variables

1. Click on your **Flask application service** (not the database)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add the following variables one by one:

#### Required Variables:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=<generate-secure-key>

# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=+14155238886

# Anthropic Claude API Configuration
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Application URL (set after deployment - see Step 5)
APP_URL=https://your-app.up.railway.app
```

#### How to Generate FLASK_SECRET_KEY:

```bash
# On your local machine, run:
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as `FLASK_SECRET_KEY`.

### 3.2 Verify DATABASE_URL

1. Railway automatically creates `DATABASE_URL` from PostgreSQL service
2. **Do NOT manually set DATABASE_URL** - it's auto-populated
3. Verify it exists in the Variables tab

---

## Step 4: Deploy Application

### 4.1 Trigger Deployment

Railway automatically deploys when you push to your GitHub repository's main branch.

**Manual Deployment:**
1. Go to **"Deployments"** tab
2. Click **"Deploy"** button
3. Railway will:
   - Clone your repository
   - Detect Python application
   - Install dependencies from `requirements.txt`
   - Use `Procfile` to start the app with Gunicorn
   - Run on the PORT Railway provides (automatic)

### 4.2 Monitor Deployment

1. Click on the active deployment
2. Watch the **Build Logs** to ensure:
   - Dependencies install successfully
   - No errors during build
   - App starts with Gunicorn

**Expected log output:**
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:5001
[INFO] Using worker: sync
```

### 4.3 Check Deployment Status

1. Deployment should show **"Success"** status
2. Service should show **"Active"** in green

---

## Step 5: Configure Public Domain

### 5.1 Generate Public URL

1. Click on your **Flask service**
2. Go to **"Settings"** tab
3. Scroll to **"Networking"** section
4. Click **"Generate Domain"**
5. Railway will provide a URL like: `https://bmad-whatsapp-production.up.railway.app`

### 5.2 Update APP_URL Variable

1. Copy the generated domain URL
2. Go back to **"Variables"** tab
3. Update `APP_URL` with your Railway domain (without trailing slash)
4. Example: `APP_URL=https://bmad-whatsapp-production.up.railway.app`
5. Railway will automatically redeploy

---

## Step 6: Verify Deployment

### 6.1 Test Health Endpoint

1. Open your browser
2. Navigate to: `https://your-app.up.railway.app/health`
3. You should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-04T12:00:00Z"
}
```

### 6.2 Check Application Logs

1. In Railway dashboard, click on your Flask service
2. Go to **"Deployments"** tab → Click active deployment
3. View **"Deploy Logs"** to check for errors
4. Check **"View Logs"** for runtime logs

**Success indicators:**
- ✅ Build completed successfully
- ✅ Gunicorn started without errors
- ✅ Health endpoint returns 200 OK
- ✅ No database connection errors

---

## Step 7: Configure Auto-Deploy from GitHub

### 7.1 Verify Auto-Deploy Settings

1. In Railway project, click on Flask service
2. Go to **"Settings"** tab
3. Scroll to **"Service"** section
4. Verify **"Branch"** is set to `main`
5. Ensure **"Automatic deploys"** is enabled (should be default)

### 7.2 Test Auto-Deploy

1. Make a small change to your repository (e.g., update README.md)
2. Commit and push to `main` branch:
```bash
git add .
git commit -m "test: Verify Railway auto-deploy"
git push origin main
```
3. Go to Railway dashboard → **"Deployments"** tab
4. You should see a new deployment triggered automatically
5. Wait for deployment to complete

---

## Step 8: Run Database Migrations (When Needed)

### 8.1 Initial Migration Setup

When you add database models (Ticket 2.1), you'll need to run migrations:

1. In Railway dashboard, click on Flask service
2. Click **"Settings"** tab
3. Add a **"Deploy Command"** or use Railway CLI

**Option 1: Railway CLI (Recommended)**

```bash
# Install Railway CLI locally
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run migration command
railway run flask db upgrade
```

**Option 2: One-Time Manual Run**

1. Go to project settings
2. Add temporary build command:
```bash
flask db upgrade && gunicorn "src.app:create_app()"
```
3. Redeploy
4. Remove build command after migration completes

### 8.2 Future Migrations

Every time you create new database models:

```bash
# Locally create migration
flask db migrate -m "Add new model"

# Push to GitHub
git add .
git commit -m "chore: Add database migration"
git push origin main

# Railway auto-deploys, then run:
railway run flask db upgrade
```

---

## Troubleshooting

### Issue: Build Fails

**Solution:**
1. Check **Deploy Logs** for specific error
2. Verify all dependencies in `requirements.txt` are valid
3. Ensure `runtime.txt` specifies correct Python version (3.11.7)
4. Check if `Procfile` syntax is correct

### Issue: App Crashes After Deploy

**Solution:**
1. Check **View Logs** for runtime errors
2. Verify all environment variables are set correctly
3. Check `DATABASE_URL` is populated (should be automatic)
4. Ensure PORT environment variable is not hardcoded (Railway sets it automatically)

### Issue: Health Endpoint Returns 503 or Times Out

**Solution:**
1. Verify app is actually running (check logs)
2. Ensure domain is generated in Networking settings
3. Check if Gunicorn started successfully
4. Verify no errors in startup logs

### Issue: DATABASE_URL Not Found

**Solution:**
1. Ensure PostgreSQL service is created in same project
2. Check if services are linked (Railway does this automatically)
3. Try removing and re-adding PostgreSQL service
4. Check Variables tab to confirm `DATABASE_URL` exists

### Issue: Environment Variables Not Loading

**Solution:**
1. Verify variables are set in **Flask service** (not PostgreSQL)
2. Check for typos in variable names
3. Redeploy after adding new variables (Railway should auto-redeploy)
4. Use Railway CLI to verify: `railway variables`

---

## Cost Estimates

### Free Tier (Hobby Plan)
- **Execution time:** 500 hours/month ($5 credit)
- **Database:** PostgreSQL included
- **Bandwidth:** 100 GB outbound

### For 20-User MVP:
- **Expected usage:** ~100-150 hours/month
- **Database size:** <100 MB
- **Estimated cost:** **FREE** (within free tier limits)

**Note:** Monitor usage in Railway dashboard under "Usage" tab.

---

## Security Checklist

Before launching to users:

- [ ] `FLASK_ENV=production` (not development)
- [ ] Strong `FLASK_SECRET_KEY` generated (64+ characters)
- [ ] All API keys are valid and have appropriate permissions
- [ ] `APP_URL` is set to Railway domain (HTTPS)
- [ ] Database backups enabled (Railway does this automatically)
- [ ] No `.env` files committed to GitHub (check `.gitignore`)
- [ ] All secrets stored in Railway Variables (not hardcoded)

---

## Next Steps After Deployment

1. ✅ Verify health endpoint is accessible
2. ✅ Test WhatsApp webhook (Ticket 1.3)
3. ✅ Configure Twilio webhook to point to Railway URL
4. ✅ Run database migrations when models are created (Ticket 2.1)
5. ✅ Monitor logs for first 24 hours to catch any issues

---

## Useful Railway Commands

```bash
# View logs in real-time
railway logs

# View environment variables
railway variables

# Run one-off commands
railway run <command>

# Deploy specific branch
railway up

# Open project in browser
railway open
```

---

## Support & Resources

- **Railway Documentation:** https://docs.railway.com
- **Railway Discord:** https://discord.gg/railway
- **Railway Status:** https://status.railway.app
- **GitHub Issues:** Report issues in this repository

---

**Last Updated:** 2025-10-04
**Ticket:** 1.2 - Configure Railway Deployment
