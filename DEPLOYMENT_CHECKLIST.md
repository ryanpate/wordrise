# 🚀 Deployment Checklist

Use this checklist to deploy WordRise Enhanced to production.

## 📋 Pre-Deployment

### Local Testing
- [ ] Activate virtual environment
- [ ] Install all dependencies (`pip install -r requirements.txt`)
- [ ] Run setup script (`python setup.py`)
- [ ] Start local server (`python run.py`)
- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test game with all 3 difficulties
- [ ] Test all 3 powerups
- [ ] Test game completion
- [ ] Verify token earning
- [ ] Check statistics page
- [ ] View leaderboard
- [ ] Test on mobile device/browser

### Code Review
- [ ] Review `.env.example` - no secrets committed
- [ ] Check `.gitignore` includes: `*.db`, `.env`, `venv/`, `__pycache__/`
- [ ] Verify all file paths use proper separators
- [ ] Confirm Railway.json is present and correct

## 🔧 Railway Setup

### Initial Configuration
- [ ] Create Railway account at railway.app
- [ ] Install Railway CLI (optional): `npm install -g @railway/cli`
- [ ] Create new project on Railway
- [ ] Connect GitHub repository (or upload via CLI)

### Environment Variables
Set these in Railway dashboard → Variables:

- [ ] `SECRET_KEY` = Generate random string (min 32 characters)
  ```bash
  # Generate with:
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

- [ ] `DATABASE_URL` = Auto-set by Railway when you add PostgreSQL
- [ ] `PORT` = Auto-set by Railway (usually 8080 or dynamic)

### Database Setup
- [ ] Add PostgreSQL from Railway marketplace
- [ ] Railway auto-connects DATABASE_URL
- [ ] Verify connection in Railway logs

### First Deployment
- [ ] Push code to GitHub (if using GitHub method)
- [ ] Trigger deployment in Railway
- [ ] Watch build logs for errors
- [ ] Wait for "Deploy successful" message
- [ ] Note the deployment URL (e.g., yourapp.railway.app)

### Post-Deployment Setup (Critical!)

The word database needs to be initialized on first deploy:

**Method 1: Automatic (Recommended)**
Railway.json is configured to run `setup_words.py` automatically on build.
- [ ] Check deployment logs for "Word list saved" message
- [ ] If successful, skip to Testing section

**Method 2: Manual (If automatic fails)**
- [ ] In Railway dashboard, click on your service
- [ ] Click "Settings" → "Build Command"
- [ ] Run: `python setup_words.py`
- [ ] Redeploy service
- [ ] OR connect to Railway shell:
  ```bash
  railway run bash
  python setup_words.py
  exit
  ```

## ✅ Post-Deployment Testing

### Smoke Tests
- [ ] Visit your Railway URL
- [ ] Registration works
- [ ] Login works
- [ ] Can start game in all difficulties
- [ ] Words validate correctly
- [ ] Powerups work
- [ ] Game completes successfully
- [ ] Tokens awarded correctly
- [ ] Stats page loads
- [ ] Leaderboard displays

### Performance Checks
- [ ] Page loads in < 3 seconds
- [ ] API responses < 500ms
- [ ] No console errors in browser
- [ ] Mobile responsive design works
- [ ] All images/assets load

### Security Verification
- [ ] HTTPS enabled (Railway auto-provides)
- [ ] SECRET_KEY is strong and secret
- [ ] No debug mode in production
- [ ] No sensitive data in logs
- [ ] CORS configured correctly

## 🐛 Troubleshooting

### Common Issues & Solutions

#### "Word not found" errors
**Problem**: Word database not initialized
**Solution**: 
```bash
railway run bash
python setup_words.py
exit
```

#### "Database connection failed"
**Problem**: PostgreSQL not connected
**Solution**: 
- Add PostgreSQL plugin in Railway
- Verify DATABASE_URL is set
- Redeploy

#### "Internal Server Error"
**Problem**: Various causes
**Solution**:
- Check Railway logs: Dashboard → Deployments → View Logs
- Look for Python stack traces
- Common causes:
  - Missing environment variables
  - Word database not setup
  - Database migration needed

#### "Cannot import module"
**Problem**: Missing dependencies
**Solution**:
- Verify requirements.txt is complete
- Check Railway build logs
- Ensure all packages installed

#### Slow first request
**Problem**: Railway cold start
**Solution**: Normal behavior, subsequent requests fast

## 📊 Monitoring

### Ongoing Checks (Daily/Weekly)

- [ ] Check error logs in Railway dashboard
- [ ] Monitor user registrations
- [ ] Verify game completions
- [ ] Check token economy balance
- [ ] Review database size
- [ ] Test backup/restore procedures

### Metrics to Track

User Engagement:
- Daily active users
- Games per user
- Average session length
- Completion rate

Technical:
- API response times
- Error rates
- Database query performance
- Server resource usage

Economy:
- Average tokens per user
- Powerup usage distribution
- Token earn vs spend ratio

## 🔄 Updates & Maintenance

### Making Changes

1. Test locally first
2. Commit to GitHub
3. Railway auto-deploys (if configured)
4. Monitor deployment logs
5. Test production immediately

### Database Migrations

When changing models:
```bash
# Local:
flask db migrate -m "description"
flask db upgrade

# Railway:
railway run flask db upgrade
```

### Rollback Procedure

If deployment fails:
1. Go to Railway → Deployments
2. Find last successful deployment
3. Click "Redeploy"

## 🎉 Launch Checklist

### Before Public Launch

- [ ] All features tested
- [ ] Documentation reviewed
- [ ] Error handling tested
- [ ] Mobile tested thoroughly
- [ ] Backup strategy in place
- [ ] Monitoring setup
- [ ] Support plan ready

### Marketing Prep

- [ ] Screenshot games/features
- [ ] Create demo video
- [ ] Write launch post
- [ ] Prepare social media
- [ ] Set up analytics (optional)

## 📈 Scale Preparation

### When User Growth Happens

- [ ] Monitor Railway resource usage
- [ ] Consider upgrading Railway plan
- [ ] Implement caching (Redis)
- [ ] Add rate limiting
- [ ] Optimize database queries
- [ ] Consider CDN for assets

## 🛡️ Security Checklist

- [ ] Strong SECRET_KEY in production
- [ ] PostgreSQL (not SQLite) in production
- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] No secrets in code/logs
- [ ] Regular security updates
- [ ] Backup strategy tested

## 📝 Documentation

- [ ] README.md updated with production URL
- [ ] API documentation if needed
- [ ] User guide available
- [ ] Admin procedures documented

## ✨ You're Ready!

Once all checkboxes are complete:
- ✅ Your app is production-ready
- ✅ Users can register and play
- ✅ Everything is monitored
- ✅ You're prepared for growth

**Congratulations on your deployment!** 🎉

---

## 🆘 Emergency Contacts

- Railway Support: help@railway.app
- Railway Status: status.railway.app
- Railway Docs: docs.railway.app

## 📞 Quick Commands Reference

```bash
# View logs
railway logs

# Open in browser
railway open

# Connect to shell
railway run bash

# Run migrations
railway run flask db upgrade

# Check environment
railway variables

# Redeploy
railway up --detach
```

---

**Last Updated**: Check this list before each deployment!
