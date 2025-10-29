# 🚀 WordRise - Quick Start Guide

Get your WordRise game up and running in 5 minutes!

## What's Included

✅ Complete Flask backend with REST API
✅ Modern frontend with beautiful UI
✅ 3,154 word database
✅ Daily challenge system
✅ Practice mode
✅ Hint system
✅ Responsive design (mobile, tablet, desktop)

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser

## Installation Steps

### 1. Extract the Project

```bash
unzip wordrise_complete.zip
cd wordrise_project
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- Flask
- Flask-CORS

### 3. Start the Server

```bash
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### 4. Open Your Browser

Navigate to: **http://localhost:5000**

🎉 **That's it!** You're ready to play!

## First Steps

### Try Daily Challenge
1. Click "Daily Challenge" on the home page
2. Everyone gets the same word today
3. Build the tallest tower you can!

### Try Practice Mode
1. Click "Practice Mode"
2. Enter a 3-letter starting word (e.g., "cat", "art", "dog")
3. Click "Start Game"
4. Build your tower!

## How to Play

### Basic Rules
1. **Start** with a 3-letter word
2. **Add** exactly ONE letter to create a new word
3. **Use** ALL letters from the previous word
4. **Build** the highest tower possible!

### Example Game
```
ART (3 letters)
  ↓ +T
TART (4 letters)
  ↓ +S
START (5 letters)
  ↓ +M
STREAM (6 letters)
```

### Scoring
- **Base Points** = Word Length × Level Number
- **Bonuses** for uncommon letters (Q, X, Z, J, K)
- **Speed Bonus** for completing quickly

Example:
- Level 1 (ART, 3 letters): 3 × 1 = 3 points
- Level 2 (TART, 4 letters): 4 × 2 = 8 points
- Level 3 (START, 5 letters): 5 × 3 = 15 points
- **Total: 26 points**

## Features Guide

### Hints 💡
Stuck? Click the "Hint" button for help:
- Shows possible starting letters
- Counts how many words are possible
- Use sparingly for higher scores!

### Undo ↶
Made a mistake? Click "Undo" to remove the last word.

### Reset 🔄
Start over from the beginning word.

### Finish 🏁
End your game and see your final score and statistics.

## Keyboard Shortcuts

- **Enter** - Submit word
- **Esc** - Close modals
- **Tab** - Navigate elements

## Troubleshooting

### Server Won't Start

**Problem**: Port 5000 already in use
```bash
# Use a different port
python -c "from app import create_app; app = create_app(); app.run(port=5001)"
```

**Problem**: Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Game Not Loading

**Problem**: Blank page
1. Check browser console (F12) for errors
2. Ensure server is running
3. Try clearing browser cache
4. Try a different browser

**Problem**: API errors
1. Check that backend is running
2. Look for error messages in terminal
3. Verify all files extracted correctly

### Words Not Working

**Problem**: Word rejected
- Make sure you're using ALL letters from the previous word
- Check that you're adding exactly ONE letter
- Verify it's a valid English word in the dictionary

## Project Structure

```
wordrise_project/
├── static/              # Frontend files
│   ├── index.html      # Main page
│   ├── css/
│   │   └── style.css   # Styling
│   └── js/
│       ├── config.js   # Settings
│       ├── api.js      # API client
│       ├── game.js     # Game logic
│       └── app.js      # UI controller
├── app/                # Backend
│   ├── __init__.py     # Flask app
│   ├── game_engine.py  # Game engine
│   ├── session_manager.py
│   └── api/
│       └── routes.py   # API endpoints
├── data/               # Word database
│   ├── words.json
│   └── words_by_length.json
├── run.py             # Start server
└── requirements.txt   # Dependencies
```

## Customization

### Change Starting Port

Edit `run.py`:
```python
app.run(host='0.0.0.0', port=3000, debug=True)
```

### Change Colors

Edit `static/css/style.css`:
```css
:root {
    --primary: #6366f1;      /* Your color here */
    --secondary: #10b981;    /* Your color here */
}
```

### Add More Words

Edit `data/words.json` or run:
```bash
python create_words.py
```

## API Documentation

Full API docs available at: `API_DOCUMENTATION.md`

Quick reference:
- `POST /api/game/start` - Start new game
- `POST /api/game/{id}/add-word` - Add word
- `GET /api/game/{id}/hint` - Get hint
- `POST /api/game/{id}/end` - End game
- `GET /api/daily/word` - Get daily word

## Testing the API

Using curl:
```bash
# Get daily word
curl http://localhost:5000/api/daily/word

# Check health
curl http://localhost:5000/api/health

# Get stats
curl http://localhost:5000/api/stats
```

## Development Mode

Enable detailed logging:
```bash
export FLASK_ENV=development
python run.py
```

This enables:
- Auto-reload on file changes
- Detailed error messages
- Debug toolbar

## Mobile Usage

The game works great on mobile!

1. Start the server on your computer
2. Find your computer's IP address
3. On your phone, visit `http://YOUR_IP:5000`
4. Add to home screen for app-like experience!

## Next Steps

### Enhance Your Game
- [ ] Add user accounts
- [ ] Set up database (PostgreSQL)
- [ ] Deploy to the web
- [ ] Add leaderboards
- [ ] Create achievements

### Deploy Online
See `PROJECT_SUMMARY.md` for deployment guides:
- Heroku (free tier)
- Railway
- AWS
- Digital Ocean

### Get Domain
Register **wordrise.app** or similar domain and point it to your deployed app!

## Need Help?

1. **Check Documentation**
   - `README.md` - Overview
   - `API_DOCUMENTATION.md` - API reference
   - `FRONTEND_README.md` - Frontend details
   - `PROJECT_SUMMARY.md` - Full roadmap

2. **Common Issues**
   - Check the Troubleshooting section above
   - Look for error messages in browser console
   - Check terminal for backend errors

3. **Still Stuck?**
   - Check GitHub Issues
   - Email: support@wordrise.app
   - Review the example in `demo.py`

## Tips for Best Experience

### For Players
- 🎯 Start with common words for more options
- 💡 Use hints strategically
- ⏱️ Play daily challenges to compete with others
- 📝 Keep a list of your best towers!

### For Developers
- 🔧 Use DevTools (F12) to debug
- 📊 Check API responses in Network tab
- 🎨 Customize colors to match your brand
- 🚀 Deploy to show friends!

## What's Next?

After you've played a few games:

1. **Share with friends** - Let them try the daily challenge!
2. **Customize** - Make it your own with colors and branding
3. **Deploy** - Put it online for everyone to play
4. **Enhance** - Add the features you want to see

## Success Checklist

- [ ] Server starts without errors
- [ ] Can access http://localhost:5000
- [ ] Landing page displays correctly
- [ ] Can start a daily challenge game
- [ ] Can start a practice mode game
- [ ] Can add words to the tower
- [ ] Can get hints
- [ ] Can undo words
- [ ] Can finish game and see results
- [ ] Mobile responsive design works

## Quick Commands Reference

```bash
# Start server
python run.py

# Run tests
python tests/test_game_engine.py

# Test API
python test_api.py

# Create new word database
python create_words.py

# Run demo
python demo.py
```

## Performance Tips

For the best experience:
- Use Chrome, Firefox, or Safari (latest versions)
- Enable JavaScript
- Allow pop-ups for sharing results
- Use WiFi for faster responses
- Close unnecessary browser tabs

## Enjoy Playing WordRise! 🎮

Remember:
- There's a new daily challenge every day!
- Practice mode lets you play unlimited games
- Share your high scores with friends
- Build the highest tower you can!

---

**Happy Word Building!** 🏗️

Made with ❤️ for word game lovers
