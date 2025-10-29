# WordRise Enhanced - Quick Start Guide 🚀

## 🎯 What's New?

Your WordRise game now includes:

1. **User Accounts** - Register and login to track your progress
2. **Token System** - Earn tokens by playing, spend on powerups
3. **Difficulty Levels** - Choose Easy (1 letter), Medium (2), or Hard (3)
4. **Powerups**:
   - 💡 Hint (10 tokens) - Get a clue
   - ⬅️ Remove Letter (25 tokens) - Go back one
   - ⏭️ Skip Word (50 tokens) - Try a different word
5. **Statistics** - Track scores, play time, favorite words/letters
6. **Leaderboard** - Compete with other players

## ⚡ Quick Setup (5 minutes)

### Local Development

```bash
# 1. Navigate to project
cd wordrise-enhanced

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run setup (creates word database and initializes DB)
python setup.py

# 5. Start the server
python run.py

# 6. Open browser
# Go to: http://localhost:5000
```

That's it! You're ready to play! 🎮

### First Time Playing

1. **Register** a new account
2. You start with **100 tokens** 💎
3. Choose your **difficulty**
4. Start building your word tower!
5. Use **powerups** strategically
6. Complete games to **earn more tokens**

## 🚂 Deploy to Railway (Production)

### Method 1: Via GitHub

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose your repository
   - Add environment variable: `SECRET_KEY=<random-string>`
   - Railway auto-adds PostgreSQL database
   - Click "Deploy"

3. **Setup word database** (one-time)
   - In Railway dashboard, click on your service
   - Go to "Variables" tab
   - Click "RAW Editor"
   - Add: `SETUP_WORDS=true`
   - Redeploy once
   - Remove the variable after first successful deployment

### Method 2: Via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Add environment variable
railway variables set SECRET_KEY=$(openssl rand -hex 32)

# Deploy
railway up

# Open in browser
railway open
```

## 💡 Tips & Tricks

### Token Management
- Start with 100 free tokens
- Each completed game gives you: 10 + (2 × tower_height) tokens
- A 5-level tower = 20 tokens earned!

### Powerup Strategy
- **Hints** (10 tokens) - Use when stuck
- **Remove Letter** (25 tokens) - Great for fixing mistakes
- **Skip Word** (50 tokens) - When you know the next letter but can't find words

### Difficulty Selection
- **Easy** (1 letter): Perfect for learning, e.g., a → at → art
- **Medium** (2 letters): Balanced challenge, e.g., at → art → cart
- **Hard** (3 letters): Classic mode, e.g., art → cart → craft

## 📊 Tracking Your Progress

- **Stats Page**: View all your statistics
- **Leaderboard**: See top players globally
- **Game History**: Review past games
- **Token History**: Track earnings and spending

## 🔧 Troubleshooting

### "Word database not found"
```bash
python setup_words.py
```

### "Database not initialized"
```bash
python setup.py
```

### Reset everything (fresh start)
```bash
rm wordrise.db
python setup.py
```

### Railway: Word database missing
- Add `SETUP_WORDS=true` environment variable
- Redeploy once
- Remove the variable

## 📱 Mobile & Desktop

The game is fully responsive and works on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktop computers

## 🎮 Game Rules Reminder

1. Start with a word (1-3 letters based on difficulty)
2. Add **exactly ONE** new letter
3. Use **ALL** letters from previous word
4. Letters can be **rearranged**
5. Build as high as possible!

### Scoring
- Points = Word Length × Level
- Bonus for rare letters (Q, X, Z, J, K)
- Bonus for speed

## 🔐 Security Notes

For production deployment:
- Use a strong `SECRET_KEY` (32+ random characters)
- Use PostgreSQL (not SQLite)
- Keep your `.env` file secret
- Never commit sensitive data to GitHub

## 📧 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review API endpoints for integration
- Check database models for customization

## 🎉 Have Fun!

Remember: The game gets more rewarding as you play!
- Complete games to earn tokens
- Use tokens wisely for powerups
- Track your improvement over time
- Compete on the leaderboard

Happy word building! 🏗️💎
