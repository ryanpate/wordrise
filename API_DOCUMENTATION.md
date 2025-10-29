# 📡 WordRise Enhanced - API Documentation

Complete API reference for all endpoints.

## Base URL

- **Local Development**: `http://localhost:5000/api`
- **Production**: `https://your-app.railway.app/api`

## Authentication

Most endpoints require authentication using JWT tokens.

### Headers
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

### Getting a Token
Login or register to receive a JWT token. Include it in the Authorization header for protected routes.

---

## 🔐 Authentication Endpoints

### Register New User

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "username": "player123",
  "email": "player@example.com",
  "password": "securepassword123"
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Registration successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "player123",
    "email": "player@example.com",
    "tokens": 100,
    "total_tokens_earned": 100,
    "total_tokens_spent": 0,
    "created_at": "2025-01-15T10:30:00",
    "last_login": "2025-01-15T10:30:00"
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "errors": [
    "Username already exists",
    "Email already registered"
  ]
}
```

---

### Login

**POST** `/auth/login`

Authenticate and receive JWT token.

**Request Body:**
```json
{
  "username": "player123",
  "password": "securepassword123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "player123",
    "email": "player@example.com",
    "tokens": 150,
    "total_tokens_earned": 200,
    "total_tokens_spent": 50,
    "created_at": "2025-01-15T10:30:00",
    "last_login": "2025-01-16T14:20:00"
  }
}
```

**Error Response (401):**
```json
{
  "success": false,
  "message": "Invalid username or password"
}
```

---

### Get Current User

**GET** `/auth/me`

Get authenticated user's information.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "player123",
    "email": "player@example.com",
    "tokens": 150,
    "total_tokens_earned": 200,
    "total_tokens_spent": 50,
    "created_at": "2025-01-15T10:30:00",
    "last_login": "2025-01-16T14:20:00"
  }
}
```

---

## 🎮 Game Endpoints

### Start New Game

**POST** `/game/start`

Start a new game session with chosen difficulty.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "difficulty": "hard"
}
```

**Difficulty Options:**
- `"easy"` - Start with 1 letter
- `"medium"` - Start with 2 letters
- `"hard"` - Start with 3 letters (default)

**Success Response (200):**
```json
{
  "success": true,
  "session_id": 42,
  "starting_word": "art",
  "difficulty": "hard",
  "game_state": {
    "tower": ["art"],
    "height": 1,
    "current_word": "art",
    "starting_word": "art",
    "difficulty": "hard",
    "hints_used": 0,
    "powerups_used": {
      "letter_removals": 0,
      "word_skips": 0
    },
    "is_active": true
  },
  "user_tokens": 150
}
```

---

### Add Word to Tower

**POST** `/game/<session_id>/add-word`

Add a new word to the current game tower.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "word": "cart"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Great! Added 'CART' using letter C",
  "game_state": {
    "tower": ["art", "cart"],
    "height": 2,
    "current_word": "cart",
    "starting_word": "art",
    "difficulty": "hard",
    "hints_used": 0,
    "powerups_used": {
      "letter_removals": 0,
      "word_skips": 0
    },
    "is_active": true
  },
  "added_letter": "c"
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "'xyz' is not a valid word"
}
```

---

### Get Hint (Powerup)

**POST** `/game/<session_id>/hint`

Get a hint for the next word. Costs 10 tokens.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Request Body (Optional):**
```json
{
  "hint_type": "starts_with"
}
```

**Hint Types:**
- `"starts_with"` - Shows first letter
- `"contains"` - Shows a middle letter
- `"definition"` - Shows partial word
- `"length"` - Shows target length

**Success Response (200):**
```json
{
  "success": true,
  "hint": "Try a word starting with 'C'",
  "possible_words_count": 15,
  "tokens_spent": 10,
  "tokens_remaining": 140
}
```

**Error Response (402):**
```json
{
  "success": false,
  "message": "Insufficient tokens. Need 10 tokens.",
  "tokens_needed": 10,
  "tokens_available": 5
}
```

---

### Remove Letter (Powerup)

**POST** `/game/<session_id>/remove-letter`

Remove one letter from current word. Costs 25 tokens.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Removed a letter! New word: CART",
  "new_word": "cart",
  "tower_height": 2,
  "tokens_spent": 25,
  "tokens_remaining": 125,
  "game_state": {
    "tower": ["art", "cart"],
    "height": 2,
    "current_word": "cart",
    "powerups_used": {
      "letter_removals": 1,
      "word_skips": 0
    }
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "Cannot remove letter from starting word"
}
```

---

### Skip Word (Powerup)

**POST** `/game/<session_id>/skip-word`

Replace current word with alternative at same level. Costs 50 tokens.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Skipped to: CARE",
  "new_word": "care",
  "tower_height": 2,
  "tokens_spent": 50,
  "tokens_remaining": 100,
  "game_state": {
    "tower": ["art", "care"],
    "height": 2,
    "current_word": "care",
    "powerups_used": {
      "letter_removals": 0,
      "word_skips": 1
    }
  }
}
```

---

### End Game

**POST** `/game/<session_id>/end`

Complete the game and calculate final score.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "final_result": {
    "tower": ["art", "cart", "craft", "crafts"],
    "height": 4,
    "starting_word": "art",
    "difficulty": "hard",
    "time_seconds": 180,
    "hints_used": 1,
    "powerups_used": {
      "letter_removals": 0,
      "word_skips": 0
    },
    "total_score": 156,
    "base_score": 140,
    "letter_bonus": 8,
    "time_bonus": 8,
    "breakdown": [
      {
        "level": 1,
        "word": "art",
        "base_points": 3,
        "letter_bonus": 0
      },
      {
        "level": 2,
        "word": "cart",
        "base_points": 8,
        "letter_bonus": 0
      }
    ]
  },
  "tokens_earned": 18,
  "tokens_total": 168,
  "session_id": 42
}
```

---

## 📊 Statistics Endpoints

### Get User Statistics

**GET** `/stats/me`

Get current user's complete statistics.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "stats": {
    "user_id": 1,
    "total_games_played": 25,
    "total_games_completed": 20,
    "total_play_time_seconds": 3600,
    "highest_score": 245,
    "highest_tower": 8,
    "total_score": 2450,
    "average_score": 122.5,
    "most_used_letters": [
      ["e", 156],
      ["a", 142],
      ["r", 98]
    ],
    "most_used_words": [
      ["art", 15],
      ["cart", 12],
      ["care", 10]
    ],
    "longest_word_used": "craftsman",
    "fastest_game_seconds": 90,
    "updated_at": "2025-01-16T14:30:00"
  }
}
```

---

### Get Game History

**GET** `/stats/history?limit=10&offset=0`

Get user's game history with pagination.

**Query Parameters:**
- `limit` (integer, default: 10) - Number of games to return
- `offset` (integer, default: 0) - Pagination offset

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "games": [
    {
      "id": 42,
      "user_id": 1,
      "starting_word": "art",
      "difficulty": "hard",
      "tower": ["art", "cart", "craft"],
      "final_score": 156,
      "tower_height": 3,
      "hints_used": 1,
      "powerups_used": {
        "letter_removals": 0,
        "word_skips": 0
      },
      "started_at": "2025-01-16T14:00:00",
      "ended_at": "2025-01-16T14:05:00",
      "play_time_seconds": 300,
      "is_completed": true
    }
  ],
  "total": 25
}
```

---

### Get Leaderboard

**GET** `/stats/leaderboard?limit=10`

Get global leaderboard (public endpoint).

**Query Parameters:**
- `limit` (integer, default: 10) - Number of top players

**Success Response (200):**
```json
{
  "success": true,
  "leaderboard": [
    {
      "rank": 1,
      "username": "wordmaster",
      "highest_score": 489,
      "highest_tower": 12,
      "total_games": 150
    },
    {
      "rank": 2,
      "username": "player123",
      "highest_score": 356,
      "highest_tower": 10,
      "total_games": 85
    }
  ]
}
```

---

## 💎 Token Endpoints

### Get Token Balance

**GET** `/tokens/balance`

Get user's current token balance.

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "tokens": 168,
  "total_earned": 300,
  "total_spent": 132
}
```

---

### Get Token History

**GET** `/tokens/history?limit=20`

Get user's token transaction history.

**Query Parameters:**
- `limit` (integer, default: 20) - Number of transactions

**Headers Required:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "transactions": [
    {
      "id": 1,
      "user_id": 1,
      "amount": 18,
      "transaction_type": "earn",
      "reason": "Completed game 42",
      "created_at": "2025-01-16T14:05:00"
    },
    {
      "id": 2,
      "user_id": 1,
      "amount": -10,
      "transaction_type": "spend",
      "reason": "Hint for game 42",
      "created_at": "2025-01-16T14:02:30"
    }
  ]
}
```

---

### Get Powerup Prices

**GET** `/tokens/prices`

Get current prices for all powerups (public endpoint).

**Success Response (200):**
```json
{
  "success": true,
  "prices": {
    "hint": {
      "cost": 10,
      "description": "Get a hint for the next word"
    },
    "remove_letter": {
      "cost": 25,
      "description": "Remove one letter from the current word"
    },
    "skip_word": {
      "cost": 50,
      "description": "Choose a new word to build from"
    }
  }
}
```

---

## 🏥 Utility Endpoints

### Health Check

**GET** `/health`

Check API health status (public endpoint).

**Success Response (200):**
```json
{
  "status": "healthy",
  "service": "wordrise-enhanced",
  "features": [
    "authentication",
    "tokens",
    "powerups",
    "statistics"
  ]
}
```

---

## ❌ Error Responses

### Common HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created (e.g., user registration)
- **400 Bad Request** - Invalid input
- **401 Unauthorized** - Missing or invalid authentication
- **402 Payment Required** - Insufficient tokens
- **403 Forbidden** - Account inactive
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

### Error Response Format

```json
{
  "success": false,
  "message": "Error description",
  "error": "Technical details (optional)"
}
```

---

## 📝 Rate Limiting

Currently no rate limiting implemented. Consider adding for production:
- Authentication endpoints: 5 requests/minute
- Game endpoints: 30 requests/minute
- Stats endpoints: 10 requests/minute

---

## 🔒 Security Notes

1. **Always use HTTPS** in production
2. **Store tokens securely** (localStorage or httpOnly cookies)
3. **Validate all inputs** client-side before sending
4. **Handle token expiration** (tokens expire after 7 days)
5. **Don't log sensitive data** (passwords, tokens)

---

## 📚 Code Examples

### JavaScript (Fetch API)

```javascript
// Register
const registerUser = async (username, email, password) => {
  const response = await fetch('https://your-app.railway.app/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ username, email, password })
  });
  
  const data = await response.json();
  
  if (data.success) {
    localStorage.setItem('token', data.token);
    return data.user;
  } else {
    throw new Error(data.errors.join(', '));
  }
};

// Start Game
const startGame = async (difficulty) => {
  const token = localStorage.getItem('token');
  
  const response = await fetch('https://your-app.railway.app/api/game/start', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ difficulty })
  });
  
  return await response.json();
};
```

### Python (Requests)

```python
import requests

# Login
def login(username, password):
    response = requests.post(
        'https://your-app.railway.app/api/auth/login',
        json={'username': username, 'password': password}
    )
    
    data = response.json()
    
    if data['success']:
        return data['token']
    else:
        raise Exception(data['message'])

# Add Word
def add_word(session_id, word, token):
    response = requests.post(
        f'https://your-app.railway.app/api/game/{session_id}/add-word',
        headers={'Authorization': f'Bearer {token}'},
        json={'word': word}
    )
    
    return response.json()
```

---

## 🧪 Testing

### Postman Collection

Import these examples into Postman for easy testing:

1. Create environment with:
   - `base_url`: `http://localhost:5000/api` or production URL
   - `token`: Your JWT token (set after login)

2. Add requests following the endpoint documentation above

3. Use `{{base_url}}` and `{{token}}` variables in requests

---

## 📞 Support

For API issues or questions:
- Check this documentation
- Review error messages
- Check server logs
- Open GitHub issue

---

**API Version**: 1.0.0  
**Last Updated**: January 2025
