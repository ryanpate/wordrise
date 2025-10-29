# Railway Deployment Checklist

## ✅ Files to Download and Add to Your wordrise Folder

Download these files and place them in your wordrise root:

1. ✅ run.py (replaces existing)
2. ✅ requirements.txt (replaces existing) 
3. ✅ Procfile (new file)
4. ✅ railway.json (new file)
5. ✅ index.html (already updated with correct paths)

## ✅ Quick Deploy Commands

```bash
# 1. Navigate to your wordrise folder
cd ~/path/to/wordrise

# 2. Add all files
git add run.py requirements.txt Procfile railway.json index.html

# 3. Commit
git commit -m "Deploy to Railway"

# 4. Push to GitHub
git push
```

## ✅ Deploy on Railway

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select `ryanpate/wordrise` repository
4. Wait 2-3 minutes for deployment
5. Get your URL: `https://your-app.railway.app`

## ✅ Test Your Deployment

- [ ] Homepage loads with styling
- [ ] Daily Challenge button works
- [ ] Practice Mode button works
- [ ] Can play a full game
- [ ] Word validation works

## 🎉 Done!

Your entire WordRise game is live!
