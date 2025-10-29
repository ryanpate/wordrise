# 🏗️ WordRise API Documentation

## Base URL
```
Development: http://localhost:5000/api
Production: https://wordrise.app/api
```

## Response Format

All API responses follow this format:

```json
{
  "success": true,
  "...": "response data"
}
```

On error:
```json
{
  "success": false,
  "error": "Error message"
}
```

---

## Endpoints

### 🏠 Root & Health

#### GET `/`
Get API information

**Response:**
```json
{
  "name": "WordRise API",
  "version": "1.0.0",
  "description": "REST API for WordRise word tower game",
  "endpoints": {...}
}
```

#### GET `/api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "service": "wordrise-api"
}
```

---

### 🎮 Game Endpoints

#### POST `/api/game/start`
Start a new game session

**Request Body:**
```json
{
  "mode": "daily" | "practice",
  "starting_word": "art"  // Optional, only for practice mode
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "mode": "practice",
  "starting_word": "art",
  "tower": ["art"],
  "height": 1,
  "current_word": "art"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/game/start \
  -H "Content-Type: application/json" \
  -d '{"mode": "practice", "starting_word": "art"}'
```

---

#### GET `/api/game/<session_id>/state`
Get current game state

**Response:**
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "tower": ["art", "tart"],
  "height": 2,
  "current_word": "tart",
  "starting_word": "art",
  "hints_used": 0,
  "is_active": true
}
```

**Example:**
```bash
curl http://localhost:5000/api/game/<session_id>/state
```

---

#### POST `/api/game/<session_id>/add-word`
Add a word to the tower

**Request Body:**
```json
{
  "word": "tart"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Added letter: T",
  "word": "tart",
  "added_letter": "t",
  "tower_height": 2,
  "current_letters": ["a", "r", "t", "t"]
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "'xyz' is not a valid word"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/game/<session_id>/add-word \
  -H "Content-Type: application/json" \
  -d '{"word": "tart"}'
```

---

#### GET `/api/game/<session_id>/hint`
Get a hint for the next possible word

**Query Parameters:**
- `hint_type` (optional): `starts_with` | `contains` | `length` | `definition`
  - Default: `starts_with`

**Response:**
```json
{
  "success": true,
  "hint": "Try a word starting with 'T'",
  "possible_words_count": 15,
  "hints_used": 1
}
```

**Example:**
```bash
curl "http://localhost:5000/api/game/<session_id>/hint?hint_type=starts_with"
```

---

#### POST `/api/game/<session_id>/undo`
Undo the last word added

**Response:**
```json
{
  "success": true,
  "message": "Removed 'tart'",
  "tower_height": 1,
  "current_word": "art"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/game/<session_id>/undo
```

---

#### POST `/api/game/<session_id>/reset`
Reset the game to starting word

**Response:**
```json
{
  "success": true,
  "message": "Game reset",
  "starting_word": "art",
  "tower": ["art"],
  "height": 1
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/game/<session_id>/reset
```

---

#### POST `/api/game/<session_id>/end`
End the game and get final results

**Response:**
```json
{
  "success": true,
  "results": {
    "tower": ["art", "tart", "start"],
    "height": 3,
    "starting_word": "art",
    "total_score": 26,
    "base_score": 26,
    "letter_bonus": 0,
    "speed_bonus": 0,
    "time_seconds": 120,
    "hints_used": 0,
    "breakdown": [
      {
        "level": 1,
        "word": "art",
        "length": 3,
        "multiplier": 1,
        "base_points": 3,
        "letter_bonus": 0
      },
      ...
    ]
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/game/<session_id>/end
```

---

### 📅 Daily Challenge

#### GET `/api/daily/word`
Get the daily challenge word

**Query Parameters:**
- `date` (optional): YYYY-MM-DD format
  - Default: today

**Response:**
```json
{
  "success": true,
  "date": "2025-10-29",
  "word": "cat",
  "challenge_number": 302
}
```

**Example:**
```bash
# Get today's word
curl http://localhost:5000/api/daily/word

# Get word for specific date
curl "http://localhost:5000/api/daily/word?date=2025-10-29"
```

---

### 🛠️ Utility Endpoints

#### POST `/api/validate-word`
Check if a word is valid

**Request Body:**
```json
{
  "word": "hello"
}
```

**Response:**
```json
{
  "success": true,
  "word": "hello",
  "is_valid": true
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/validate-word \
  -H "Content-Type: application/json" \
  -d '{"word": "hello"}'
```

---

#### GET `/api/stats`
Get server statistics

**Response:**
```json
{
  "success": true,
  "active_sessions": 42,
  "total_words": 3154
}
```

**Example:**
```bash
curl http://localhost:5000/api/stats
```

---

## Game Flow Example

Here's a typical game flow:

### 1. Start Game
```bash
POST /api/game/start
{
  "mode": "practice",
  "starting_word": "art"
}

# Save the session_id from response
```

### 2. Add Words
```bash
POST /api/game/<session_id>/add-word
{"word": "tart"}

POST /api/game/<session_id>/add-word
{"word": "start"}

POST /api/game/<session_id>/add-word
{"word": "stream"}
```

### 3. Get Help (if needed)
```bash
GET /api/game/<session_id>/hint?hint_type=starts_with
```

### 4. End Game
```bash
POST /api/game/<session_id>/end

# Get final score and tower details
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created (new game session) |
| 400 | Bad Request (invalid input) |
| 404 | Not Found (session not found) |
| 405 | Method Not Allowed |
| 500 | Internal Server Error |

---

## Common Errors

### Session Not Found
```json
{
  "success": false,
  "error": "Session not found"
}
```
**Solution:** Start a new game session

### Invalid Word
```json
{
  "success": false,
  "message": "'xyz' is not a valid word"
}
```
**Solution:** Try a different word

### Game Already Ended
```json
{
  "success": false,
  "error": "Game has ended"
}
```
**Solution:** Start a new game

---

## Rate Limiting

Currently no rate limiting. In production:
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

---

## CORS

CORS is enabled for all `/api/*` endpoints.

Allowed origins in development: `*`

In production, configure specific origins in `config.py`

---

## Session Management

- Sessions are stored in memory (temporary)
- Sessions expire after 30 minutes of inactivity
- In production, use Redis for session storage

---

## Testing the API

### Using curl

```bash
# Start a game
SESSION_ID=$(curl -s -X POST http://localhost:5000/api/game/start \
  -H "Content-Type: application/json" \
  -d '{"mode": "practice", "starting_word": "art"}' \
  | jq -r '.session_id')

# Add a word
curl -X POST http://localhost:5000/api/game/$SESSION_ID/add-word \
  -H "Content-Type: application/json" \
  -d '{"word": "tart"}'

# Get state
curl http://localhost:5000/api/game/$SESSION_ID/state

# End game
curl -X POST http://localhost:5000/api/game/$SESSION_ID/end
```

### Using Python

```python
import requests

# Start game
response = requests.post('http://localhost:5000/api/game/start',
    json={'mode': 'practice', 'starting_word': 'art'})
session_id = response.json()['session_id']

# Add word
requests.post(f'http://localhost:5000/api/game/{session_id}/add-word',
    json={'word': 'tart'})

# Get state
state = requests.get(f'http://localhost:5000/api/game/{session_id}/state')
print(state.json())

# End game
results = requests.post(f'http://localhost:5000/api/game/{session_id}/end')
print(results.json())
```

### Using JavaScript

```javascript
// Start game
const response = await fetch('http://localhost:5000/api/game/start', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({mode: 'practice', starting_word: 'art'})
});
const {session_id} = await response.json();

// Add word
await fetch(`http://localhost:5000/api/game/${session_id}/add-word`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({word: 'tart'})
});

// Get state
const state = await fetch(`http://localhost:5000/api/game/${session_id}/state`);
console.log(await state.json());

// End game
const results = await fetch(`http://localhost:5000/api/game/${session_id}/end`, {
  method: 'POST'
});
console.log(await results.json());
```

---

## Next Steps

1. **Add Authentication** - User accounts and JWT tokens
2. **Add Database** - PostgreSQL for persistent storage
3. **Add Leaderboards** - Track high scores
4. **Add User Profiles** - Save game history and stats
5. **Add Redis** - For session management
6. **Add WebSockets** - For real-time features

---

## Support

For issues or questions:
- GitHub: [wordrise/api](https://github.com/wordrise/api)
- Email: support@wordrise.app
- Docs: https://wordrise.app/api/docs

---

**WordRise API v1.0.0**
wordrise.app
