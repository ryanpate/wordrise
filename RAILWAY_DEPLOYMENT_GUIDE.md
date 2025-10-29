# WordRise - Railway Deployment Guide

## Quick Deploy Steps

### 1. Update Your Files

Download and replace these files in your `wordrise` root directory:

✅ `run.py` - Updated Flask app that serves static files + API
✅ `requirements.txt` - Updated with gunicorn and flask-cors
✅ `Procfile` - Tells Railway how to start your app
✅ `railway.json` - Railway configuration (optional)
✅ `index.html` - Fixed paths to static/css and static/js

### 2. Verify Your File Structure

Your wordrise folder should look like this:

```
wordrise/
├── run.py                  ← NEW/UPDATED
├── requirements.txt        ← NEW/UPDATED
├── Procfile                ← NEW
├── railway.json            ← NEW (optional)
├── index.html              ← UPDATED (static paths)
├── config.py
├── app/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── session_manager.py
│   └── api/
│       ├── __init__.py
│       └── routes.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── config.js
│       ├── api.js
│       ├── game.js
│       └── app.js
└── data/
    ├── words.json
    └── words_by_length.json
```

### 3. Push to GitHub

```bash
cd ~/path/to/wordrise

# Add all new/updated files
git add run.py requirements.txt Procfile railway.json index.html
git commit -m "Prepare for Railway deployment"
git push
```

### 4. Deploy on Railway

#### Option A: New Project
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `wordrise` repository
5. Railway will auto-detect Flask and deploy!
6. Once deployed, click on your project to get the URL

#### Option B: Existing Project
1. Go to your Railway dashboard
2. Select your existing project
3. Click "Settings" → "Source" → Change repo to wordrise
4. Railway will redeploy

### 5. Access Your Site

After deployment completes (2-3 minutes):
- Your site will be at: `https://your-app-name.railway.app`
- Both frontend AND backend will work from the same URL!

### 6. Custom Domain (Optional)

1. In Railway project settings
2. Go to "Settings" → "Domains"
3. Click "Generate Domain" for free subdomain
4. Or add your custom domain (wordrise.app)

## Environment Variables (if needed)

If your app needs environment variables:
1. In Railway → Select your service
2. Go to "Variables" tab
3. Add any variables your app needs

## Troubleshooting

**If deployment fails:**
1. Check Railway logs (click on deployment)
2. Ensure all files are committed and pushed to GitHub
3. Verify requirements.txt has Flask, Flask-CORS, and gunicorn

**If static files don't load:**
1. Check that index.html uses `static/css/style.css` paths
2. Verify static folder is in your repo
3. Check Railway logs for 404 errors

**If API doesn't work:**
1. Check app/api/routes.py exists
2. Verify Flask blueprints are registered in run.py
3. Check Railway logs for Python errors

## What Railway Does

✅ Installs Python packages from requirements.txt
✅ Runs gunicorn to serve your Flask app
✅ Serves static files from /static folder
✅ Serves index.html at root URL (/)
✅ Handles API calls at /api/* endpoints
✅ Provides HTTPS automatically
✅ Auto-restarts on code changes

## Success! 🎉

Once deployed, test:
- Homepage loads with styling: `https://your-app.railway.app/`
- Daily Challenge button works
- Practice mode works
- All API calls function

Your entire WordRise game is now live on Railway!
