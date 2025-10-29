# WordRise Enhanced 🏗️💎

An advanced word-building tower game with user authentication, token economy, powerups, difficulty levels, and comprehensive statistics tracking.

## ✨ New Features

### 1. **User Authentication System** 🔐
- Secure registration and login with JWT tokens
- Password hashing for security
- Session management
- User profiles

### 2. **Token Economy** 💎
- Start with 100 free tokens
- Earn tokens by completing games (10 base + 2 per tower level)
- Spend tokens on powerups and hints
- Track token transactions

### 3. **Difficulty Levels** 🎯
- **Easy**: Start with 1-letter words
- **Medium**: Start with 2-letter words  
- **Hard**: Start with 3-letter words (classic)

### 4. **Powerups** ⚡
- **Hint** (10 tokens): Get a clue for the next word
- **Remove Letter** (25 tokens): Go back one letter to find alternative paths
- **Skip Word** (50 tokens): Choose a different word at the same level

### 5. **User Statistics** 📊
- Total games played and completed
- Highest score and tallest tower
- Average score calculation
- Total play time tracking
- Most used letters and words
- Longest word used
- Fastest game completion
- Game history with all details

### 6. **Leaderboard** 🏆
- Global rankings by highest score
- View top players and their achievements

## 🗂️ Project Structure

```
wordrise-enhanced/
├── app/
│   ├── __init__.py
│   ├── game_engine.py          # Enhanced game logic with powerups
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # Database models (User, GameSession, UserStats, etc.)
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth_utils.py       # JWT authentication utilities
│   └── api/
│       ├── __init__.py
│       └── routes.py           # All API endpoints
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── enhanced-game.js    # Frontend JavaScript
├── data/
│   ├── words.json              # Word dictionary
│   └── words_by_length.json   # Indexed words
├── index.html                  # Main HTML file
├── run.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── setup_words.py              # Word database setup script
└── README.md                   # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Local Development

1. **Clone or download the project**
   ```bash
   cd wordrise-enhanced
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup word database**
   ```bash
   python setup_words.py
   ```
   This downloads NLTK word corpus and creates the word database.

5. **Initialize database**
   ```bash
   python -c "from run import app, db; app.app_context().push(); db.create_all()"
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Open in browser**
   ```
   http://localhost:5000
   ```

### Environment Variables

Create a `.env` file (optional for local dev):
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///wordrise.db
PORT=5000
```

For production, use a strong SECRET_KEY and PostgreSQL DATABASE_URL.

## 🚂 Railway Deployment

### Option 1: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Add environment variables**
   ```bash
   railway variables set SECRET_KEY=<your-random-secret-key>
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### Option 2: Deploy via GitHub

1. **Push code to GitHub repository**

2. **Go to [Railway](https://railway.app)**

3. **Create New Project** → **Deploy from GitHub**

4. **Select your repository**

5. **Add environment variables**:
   - `SECRET_KEY`: Generate a random secret key
   - Railway will automatically set `DATABASE_URL` with PostgreSQL

6. **Deploy**

### Railway Configuration

The project includes `railway.json` for automatic configuration:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn run:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Post-Deployment Setup

After deployment, you need to setup the word database:

1. **Connect to Railway shell**:
   ```bash
   railway run bash
   ```

2. **Run setup script**:
   ```bash
   python setup_words.py
   ```

Or create a one-time service that runs setup_words.py on first deployment.

## 📊 Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Hashed password
- `tokens`: Current token balance
- `total_tokens_earned`: Lifetime tokens earned
- `total_tokens_spent`: Lifetime tokens spent
- `created_at`, `last_login`, `is_active`

### GameSessions
- `id`: Primary key
- `user_id`: Foreign key to User
- `starting_word`: Initial word
- `difficulty`: easy/medium/hard
- `tower`: JSON array of words
- `final_score`, `tower_height`
- `hints_used`: Number of hints used
- `powerups_used`: JSON tracking powerup usage
- `started_at`, `ended_at`, `play_time_seconds`
- `is_completed`: Boolean

### UserStats
- `user_id`: Foreign key to User
- Game statistics (games played, highest score, etc.)
- `most_used_letters`: JSON object
- `most_used_words`: JSON object
- `longest_word_used`, `fastest_game_seconds`

### TokenTransactions
- `id`: Primary key
- `user_id`: Foreign key to User
- `amount`: Tokens (positive=earn, negative=spend)
- `transaction_type`: 'earn' or 'spend'
- `reason`: Description
- `created_at`: Timestamp

### TokenPrices
- `item_type`: Unique (hint, remove_letter, skip_word, etc.)
- `cost`: Token cost
- `description`: Item description

## 🎮 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Game
- `POST /api/game/start` - Start new game (with difficulty)
- `POST /api/game/<session_id>/add-word` - Add word to tower
- `POST /api/game/<session_id>/hint` - Get hint (costs tokens)
- `POST /api/game/<session_id>/remove-letter` - Remove letter powerup
- `POST /api/game/<session_id>/skip-word` - Skip word powerup
- `POST /api/game/<session_id>/end` - End game and get results

### Statistics
- `GET /api/stats/me` - Get user statistics
- `GET /api/stats/history` - Get game history
- `GET /api/stats/leaderboard` - Get global leaderboard

### Tokens
- `GET /api/tokens/balance` - Get token balance
- `GET /api/tokens/history` - Get transaction history
- `GET /api/tokens/prices` - Get powerup prices

## 🎯 Game Rules

1. **Start** with a word (1, 2, or 3 letters based on difficulty)
2. **Add ONE letter** to create a new word
3. **Use ALL letters** from the previous word
4. **Build higher** to maximize your score
5. **Use powerups** strategically to overcome challenges

### Scoring
- Base: Word Length × Level Number
- Bonuses: Uncommon letters (Q, X, Z, J, K) and fast completion
- Penalties: None! But hints and powerups cost tokens

## 💡 Token Strategy Tips

1. **Save tokens early** - Build as high as you can without powerups
2. **Use hints wisely** - When stuck, a hint is cheaper than giving up
3. **Remove Letter** - Great for recovering from difficult words
4. **Skip Word** - Perfect when you know the next letter but can't find the word
5. **Complete games** - Finish games to earn more tokens

## 🔧 Configuration

### Token Prices (Default)
- Hint: 10 tokens
- Remove Letter: 25 tokens
- Skip Word: 50 tokens

These can be adjusted in the database through the `TokenPrices` table.

### Starting Tokens
New users start with 100 tokens (configurable in `models.py`).

### Token Rewards
- Base: 10 tokens per completed game
- Bonus: 2 tokens per tower level
- Example: A 5-level tower = 10 + (5 × 2) = 20 tokens

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database (caution: deletes all data)
rm wordrise.db
python -c "from run import app, db; app.app_context().push(); db.create_all()"
```

### Word Data Missing
```bash
python setup_words.py
```

### Token Prices Not Initialized
```bash
python -c "from run import app, db; from app.models.models import TokenPrice; app.app_context().push(); TokenPrice.initialize_prices()"
```

## 📝 Future Enhancements

- [ ] Daily challenges with special rewards
- [ ] Achievement system with badges
- [ ] Friend system and private leaderboards
- [ ] Token purchase with real money (microtransactions)
- [ ] Custom word packs for different languages
- [ ] Multiplayer competitive mode
- [ ] Mobile app version
- [ ] Social media sharing integration

## 📄 License

MIT License - Feel free to use and modify for your own projects!

## 🙏 Credits

- Word database: NLTK Words Corpus
- Word validation: Datamuse API (fallback)
- Built with Flask, SQLAlchemy, and vanilla JavaScript

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Happy word building!** 🏗️💎
