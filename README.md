# 🎲 WordRise - Random Mode Update

Your WordRise game has been updated to give a **random 3-letter word every time** instead of one daily challenge!

## 🎯 What Changed

### Before (Daily Challenge Mode) ❌
- One starting word per day
- Same word for everyone
- Had to wait until tomorrow for new word
- Used date-based seeding

### After (Random Mode) ✅
- **Different random word every time you start**
- **Unlimited games** - play as much as you want!
- Each game is unique
- True randomization

## 📦 Files Included

1. **game_engine.py** - Updated core game engine
   - Changed `get_daily_word()` → `get_random_starting_word()`
   - Removes date-based seeding
   - Returns truly random 3-letter word each time

2. **api_routes.py** - Updated API endpoints
   - `/api/game/start` - Gets random starting word
   - All other routes stay the same

3. **frontend_example.js** - Example JavaScript
   - Shows how to start random games
   - Complete game logic included

4. **index.html** - Example HTML interface
   - Beautiful UI with random mode
   - Ready to customize

5. **test_random_mode.py** - Test script
   - Verifies random words work
   - Shows 10 different starting words

6. **RANDOM_MODE_UPDATE.md** - Detailed documentation
   - Complete explanation of changes
   - Migration guide
   - Testing checklist

## 🚀 Quick Start

### Option 1: Test It First

```bash
# 1. Navigate to this folder
cd wordrise_random_mode

# 2. Run test script (requires your words.json data files)
python test_random_mode.py
```

You should see 10 different random starting words!

### Option 2: Deploy to Your App

```bash
# 1. Back up your current files
cp your-app/game_engine.py your-app/game_engine.py.backup

# 2. Copy new files
cp game_engine.py your-app/
cp api_routes.py your-app/

# 3. Update your frontend to use the new "New Game" button
#    (See frontend_example.js for reference)

# 4. Test locally
python your-app/run.py

# 5. Deploy
git add .
git commit -m "Update: Random word mode"
git push
```

## 🔧 Integration Guide

### Backend Changes (Required)

**1. Replace game_engine.py method:**

The only change in the game engine is one method:

```python
# OLD (remove):
@staticmethod
def get_daily_word(day: Optional[date] = None) -> str:
    # ... date-based logic ...

# NEW (use this):
@staticmethod
def get_random_starting_word() -> str:
    """Get a random 3-letter word for starting a new game"""
    validator = WordValidator()
    three_letter_words = validator.get_words_of_length(3)
    return random.choice(three_letter_words)
```

**2. Update API route:**

In your API routes file, change:

```python
# OLD:
starting_word = WordRiseGame.get_daily_word()

# NEW:
starting_word = WordRiseGame.get_random_starting_word()
```

### Frontend Changes (Required)

**1. Update button text:**

```html
<!-- OLD: -->
<button id="dailyChallengeBtn">📅 Daily Challenge</button>

<!-- NEW: -->
<button id="newGameBtn">🎲 New Random Game</button>
```

**2. Update JavaScript function:**

```javascript
// OLD:
async function startDailyChallenge() {
    const response = await fetch('/api/daily', { method: 'GET' });
    // ...
}

// NEW:
async function startNewGame() {
    const response = await fetch('/api/game/start', { method: 'POST' });
    const data = await response.json();
    
    if (data.success) {
        startingWord = data.starting_word;
        tower = [startingWord];
        updateUI();
    }
}
```

**That's it!** Everything else stays the same.

## ✅ Testing Checklist

After deploying, verify:

- [ ] Click "New Game" multiple times
- [ ] Each time gives a different starting word
- [ ] Can play unlimited games without waiting
- [ ] All game mechanics still work (add words, scoring, hints)
- [ ] Tower building rules still apply
- [ ] Word validation works correctly

## 🎮 Example Usage

```javascript
// Start 5 random games - each with different word
for (let i = 0; i < 5; i++) {
    const word = WordRiseGame.get_random_starting_word();
    console.log(`Game ${i+1}: ${word}`);
}

// Output:
// Game 1: fox
// Game 2: zen
// Game 3: cat
// Game 4: joy
// Game 5: oak
```

## 📊 Benefits

### For Players:
- 🎮 Unlimited games (no daily limit)
- 🎲 Every game is different
- ⚡ Instant replay
- 🔥 More addictive "just one more" gameplay

### For You:
- 📈 Higher engagement
- 🚀 Better retention
- 💰 More ad impressions
- 🎯 Simpler code (no date tracking)

## 🤔 Troubleshooting

### "Getting the same word every time"
- Check that you're using `random.choice()` without a seed
- Make sure not calling `random.seed()` anywhere
- Verify `get_random_starting_word()` is being called (not old method)

### "Frontend not updating"
- Clear browser cache (Ctrl+F5)
- Check browser console for errors
- Verify API endpoint is `/api/game/start` (POST)

### "Words not validating"
- Ensure `data/words.json` exists
- Check `data/words_by_length.json` exists
- Verify word list has 3-letter words

## 📝 Rollback

If needed, restore the old daily challenge mode:

```bash
# Restore backup
cp game_engine.py.backup game_engine.py

# Or revert git commit
git revert HEAD
git push
```

## 🎉 That's It!

The change is super simple - just one method renamed and frontend updated. Everything else works exactly the same!

**Questions?** The change is:
1. One method: `get_daily_word()` → `get_random_starting_word()`
2. Frontend calls new endpoint
3. Done! 🚀

Enjoy your unlimited random word games! 🎲🗼
