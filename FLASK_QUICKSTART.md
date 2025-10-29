# 🚀 WordRise Flask API - Quick Start Guide

## What You Have Now

✅ **Complete REST API** with 13 endpoints
✅ **Game session management**
✅ **Daily challenge system**
✅ **CORS enabled** for frontend integration
✅ **Error handling**
✅ **API documentation**

---

## 📦 Installation

### 1. Install Dependencies

```bash
cd wordrise
pip install -r requirements.txt
```

### 2. Set Up Environment (Optional)

```bash
cp .env.example .env
# Edit .env if needed
```

---

## 🎯 Start the Server

### Development Mode

```bash
python3 run.py
```

The server will start on http://localhost:5000

You should see:
```
🏗️  WordRise API Server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Environment: development
Port: 5000
Debug: True

API Endpoints:
- GET  /                          Root info
- GET  /api/health                Health check
...

🚀 Server starting on http://localhost:5000
```

---

## 🧪 Test the API

### Quick Test

```bash
# In a new terminal, test the health endpoint
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "wordrise-api"
}
```

### Full Test Suite

```bash
# Make sure server is running, then:
python3 test_api.py
```

This will test all 13 endpoints and show you the responses!

---

## 🎮 Try It Out

### 1. Start a Game

```bash
curl -X POST http://localhost:5000/api/game/start \
  -H "Content-Type: application/json" \
  -d '{"mode": "practice", "starting_word": "art"}'
```

**Save the `session_id` from the response!**

### 2. Add Words

```bash
# Replace <session_id> with your actual session ID
curl -X POST http://localhost:5000/api/game/<session_id>/add-word \
  -H "Content-Type: application/json" \
  -d '{"word": "tart"}'
```

### 3. Get Hint

```bash
curl "http://localhost:5000/api/game/<session_id>/hint?hint_type=starts_with"
```

### 4. End Game

```bash
curl -X POST http://localhost:5000/api/game/<session_id>/end
```

You'll see your final score and tower!

---

## 📁 Project Structure

```
wordrise/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── game_engine.py        # Core game logic ✅
│   ├── session_manager.py    # Session management ✅
│   └── api/
│       ├── __init__.py
│       └── routes.py         # API endpoints ✅
│
├── data/
│   ├── words.json            # Word database
│   └── words_by_length.json  # Indexed words
│
├── tests/
│   └── test_game_engine.py   # Game engine tests
│
├── config.py                 # Flask configuration ✅
├── requirements.txt          # Dependencies ✅
├── run.py                    # App runner ✅
├── test_api.py               # API test script ✅
├── API_DOCUMENTATION.md      # Complete API docs ✅
└── .env.example              # Environment template ✅
```

---

## 🔧 Available Endpoints

### Game Management
```
POST   /api/game/start                # Start new game
GET    /api/game/<id>/state           # Get game state
POST   /api/game/<id>/add-word        # Add word
GET    /api/game/<id>/hint            # Get hint
POST   /api/game/<id>/undo            # Undo word
POST   /api/game/<id>/reset           # Reset game
POST   /api/game/<id>/end             # End game
```

### Daily Challenge
```
GET    /api/daily/word                # Get daily word
```

### Utilities
```
POST   /api/validate-word             # Check word validity
GET    /api/stats                     # Server stats
GET    /api/health                    # Health check
```

---

## 📖 Example Usage

### Python

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Start game
response = requests.post(f"{BASE_URL}/game/start",
    json={"mode": "practice", "starting_word": "art"})
session_id = response.json()['session_id']
print(f"Game started: {session_id}")

# Add words
requests.post(f"{BASE_URL}/game/{session_id}/add-word",
    json={"word": "tart"})
print("Added: tart")

requests.post(f"{BASE_URL}/game/{session_id}/add-word",
    json={"word": "start"})
print("Added: start")

# Get final results
results = requests.post(f"{BASE_URL}/game/{session_id}/end")
final = results.json()['results']
print(f"\nFinal Score: {final['total_score']}")
print(f"Tower: {' → '.join(final['tower'])}")
```

### JavaScript (Frontend)

```javascript
const API_URL = 'http://localhost:5000/api';

// Start game
const startResponse = await fetch(`${API_URL}/game/start`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({mode: 'practice', starting_word: 'art'})
});
const {session_id} = await startResponse.json();

// Add word
await fetch(`${API_URL}/game/${session_id}/add-word`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({word: 'tart'})
});

// Get state
const stateResponse = await fetch(`${API_URL}/game/${session_id}/state`);
const state = await stateResponse.json();
console.log('Tower:', state.tower);

// End game
const endResponse = await fetch(`${API_URL}/game/${session_id}/end`, {
  method: 'POST'
});
const {results} = await endResponse.json();
console.log('Score:', results.total_score);
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
class Config:
    # Session timeout
    GAME_TIMEOUT_MINUTES = 30
    
    # Free tier hints
    MAX_HINTS_FREE = 3
    
    # Secret key (change in production!)
    SECRET_KEY = 'your-secret-key'
```

---

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Use different port
PORT=8000 python3 run.py
```

### Import Errors

```bash
# Make sure you're in wordrise directory
cd wordrise
python3 run.py
```

### CORS Issues

If you have CORS issues, check `app/__init__.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## 🎯 Next Steps

### Phase 1: Test Everything ✅
- [x] Install dependencies
- [x] Run server
- [x] Test all endpoints

### Phase 2: Build Frontend (Next!)
- [ ] Create HTML/CSS/JS interface
- [ ] Connect to API
- [ ] Add game UI
- [ ] Add leaderboards

### Phase 3: Add Database
- [ ] Set up PostgreSQL
- [ ] Add user accounts
- [ ] Save game history
- [ ] Add authentication

### Phase 4: Deploy
- [ ] Set up production server
- [ ] Configure domain (wordrise.app)
- [ ] Add SSL certificate
- [ ] Launch! 🚀

---

## 📚 Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference
- **[README.md](README.md)** - Project overview
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Roadmap

---

## 🔥 What's Working

✅ **Complete game logic** - All rules implemented
✅ **Session management** - Games persist across requests
✅ **Daily challenges** - Same word for all players
✅ **Hint system** - 4 types of hints
✅ **Score calculation** - With bonuses
✅ **Error handling** - Clear error messages
✅ **CORS enabled** - Ready for frontend
✅ **API documentation** - Complete reference

---

## 💡 Tips

### During Development

```bash
# Terminal 1: Run server
python3 run.py

# Terminal 2: Test API
python3 test_api.py

# Terminal 3: Make requests
curl http://localhost:5000/api/health
```

### For Production

```bash
# Use gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Or with environment
FLASK_ENV=production gunicorn run:app
```

---

## 🎉 Success!

Your Flask API is ready! The backend is complete and tested.

**What you can do now:**
1. ✅ Start the server: `python3 run.py`
2. ✅ Test the API: `python3 test_api.py`
3. ✅ Read the docs: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
4. 🎨 Build the frontend next!

---

**WordRise API is live!** 🚀

Next up: Create the frontend interface to connect to your API!

---

**WordRise** - Build Your Word Tower
**wordrise.app**
