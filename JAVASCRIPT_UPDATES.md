# JavaScript Updates Required for Random Mode

Since the HTML now calls `startGame('random')`, you need to update your JavaScript files to handle this.

## Changes Needed in your JS files

### 1. Update `startGame()` function

**Location:** Likely in `static/js/app.js` or `static/js/game.js`

**OLD CODE:**
```javascript
function startGame(mode) {
    if (mode === 'daily') {
        // Call API to get daily word
        fetch('/api/daily', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            currentGameMode = 'daily';
            startingWord = data.daily_word;
            initializeGame(startingWord);
        });
    }
}
```

**NEW CODE:**
```javascript
function startGame(mode) {
    if (mode === 'random') {
        // Call API to get random word
        fetch('/api/game/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentGameMode = 'random';
                startingWord = data.starting_word;
                initializeGame(startingWord);
            }
        });
    }
}
```

### 2. Update API endpoint

**Change:**
- OLD: `GET /api/daily`
- NEW: `POST /api/game/start`

**Response structure stays the same:**
```javascript
{
    "success": true,
    "starting_word": "fox",  // Different every time!
    "game_state": {
        "tower": ["fox"],
        "height": 1,
        "current_word": "fox"
    }
}
```

### 3. Update mode badge (optional)

If you have a mode badge showing "Daily Challenge", update it:

```javascript
// OLD:
document.getElementById('mode-badge').textContent = '📅 Daily Challenge';

// NEW:
document.getElementById('mode-badge').textContent = '🎲 Random Game';
```

## Quick Find & Replace

In your JavaScript files, search and replace:

1. **Find:** `/api/daily`  
   **Replace:** `/api/game/start`

2. **Find:** `method: 'GET'` (for the daily endpoint)  
   **Replace:** `method: 'POST'`

3. **Find:** `data.daily_word`  
   **Replace:** `data.starting_word`

4. **Find:** `mode === 'daily'`  
   **Replace:** `mode === 'random'`

## Testing

After updating:
1. Click the "PLAY" button
2. Should get a random 3-letter word
3. Click "Play Again" - should get a DIFFERENT word
4. Repeat - each game should have a unique starting word

## Example Complete Function

Here's a complete example of how your `startGame()` function should look:

```javascript
async function startGame(mode) {
    try {
        showLoading(true);
        
        if (mode === 'random') {
            // Get random starting word
            const response = await fetch('/api/game/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                currentGameMode = 'random';
                startingWord = data.starting_word;
                tower = [startingWord];
                
                // Update UI
                document.getElementById('mode-badge').textContent = '🎲 Random Game';
                showGameScreen();
                initializeGame();
            } else {
                showError('Failed to start game');
            }
        }
        
    } catch (error) {
        console.error('Error starting game:', error);
        showError('Network error - please try again');
    } finally {
        showLoading(false);
    }
}
```

## That's It!

The key changes are:
1. Change endpoint: `/api/daily` → `/api/game/start`
2. Change method: `GET` → `POST`
3. Change field: `data.daily_word` → `data.starting_word`
4. Change mode check: `'daily'` → `'random'`

Everything else stays the same! 🚀
