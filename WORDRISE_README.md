# 🏗️ WordRise - Word Tower Game Engine

A Python-based game engine for **WordRise**, an addictive word-building game where players build towers by stacking words.

🌐 **wordrise.app**

## 🎮 Game Concept

Build the tallest word tower possible by:
1. Starting with a base word (e.g., "ART")
2. Adding ONE new letter to create a new word
3. Using ALL letters from the previous word
4. Rearranging letters in any order

**Example Tower:**
```
START  (5 letters) +S
TART   (4 letters) +T  
ART    (3 letters) [BASE]
```

## ✨ Features Implemented

### Core Game Engine
- ✅ **Word Validation** - 3,000+ curated English words
- ✅ **Tower Building Logic** - Validates proper letter usage
- ✅ **Scoring System** - Level multipliers + bonuses
- ✅ **Daily Challenge** - Deterministic daily starting words
- ✅ **Hint System** - Multiple hint types
- ✅ **Game State Management** - Save/load, undo, reset

## 🚀 Quick Start

```python
from app.game_engine import WordRiseGame

# Start a new game
game = WordRiseGame(starting_word='art')

# Add words
result = game.add_word('tart')
print(result)  # {'success': True, ...}

# Get score
final = game.end_game()
print(f"Score: {final['total_score']}")
```

## 📊 Scoring System

- **Base:** `word_length × level_number`
- **Uncommon Letters:** +5 points each (Q, Z, X, J, K)
- **Speed Bonus:** +10% if under 5 minutes

## 🧪 Testing

```bash
python3 tests/test_game_engine.py
```

✅ 27 tests - 100% passing

## 🎯 Game Rules

1. ✅ Must use ALL letters from previous word
2. ✅ Must add EXACTLY ONE new letter  
3. ✅ Letters can be rearranged
4. ✅ No duplicate words

## 📁 Project Structure

```
wordrise/
├── app/game_engine.py         # Core engine (500+ lines)
├── data/
│   ├── words.json             # 3,154 words
│   └── words_by_length.json   # Indexed
├── tests/test_game_engine.py  # 27 unit tests
└── demo.py                    # Interactive demo
```

## 🔧 API Reference

```python
game = WordRiseGame(starting_word='art')
game.add_word('tart')           # Add word to tower
game.undo_last_word()           # Remove last word
game.get_hint()                 # Get gameplay hint
game.reset_game()               # Start over
game.end_game()                 # Get final score
WordRiseGame.get_daily_word()   # Today's challenge
```

---

**WordRise** - Build Your Word Tower  
**wordrise.app**
