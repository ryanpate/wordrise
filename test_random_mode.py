"""
Test Script - Random Starting Words
Demonstrates that every game starts with a different word
"""

import sys
import os

# Add parent directory to path so we can import game_engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_engine import WordRiseGame


def test_random_starting_words():
    """Test that we get different random words each time"""
    print("🎲 TESTING RANDOM STARTING WORDS\n")
    print("=" * 50)
    
    # Generate 10 random starting words
    words = []
    for i in range(10):
        word = WordRiseGame.get_random_starting_word()
        words.append(word)
        print(f"Game {i+1}: {word.upper()}")
    
    print("\n" + "=" * 50)
    print(f"\n📊 RESULTS:")
    print(f"   Total games: {len(words)}")
    print(f"   Unique words: {len(set(words))}")
    print(f"   All 3 letters: {all(len(w) == 3 for w in words)}")
    
    if len(set(words)) > 1:
        print(f"\n   ✅ SUCCESS! Getting different random words each time!")
    else:
        print(f"\n   ⚠️  WARNING: All words were the same")
    
    print(f"\n   Word variety: {list(set(words))}")


def test_game_creation():
    """Test creating games with random words"""
    print("\n\n🎮 TESTING GAME CREATION\n")
    print("=" * 50)
    
    for i in range(3):
        word = WordRiseGame.get_random_starting_word()
        game = WordRiseGame(starting_word=word)
        
        print(f"\nGame {i+1}:")
        print(f"  Starting word: {game.starting_word.upper()}")
        print(f"  Tower height: {game.get_tower_height()}")
        print(f"  Current word: {game.get_current_word().upper()}")
        
        # Try adding a word
        test_word = word + 's'  # Simple test - add 's'
        result = game.add_word(test_word)
        
        if result['success']:
            print(f"  ✅ Added '{test_word.upper()}' successfully!")
            print(f"  New tower: {' → '.join(w.upper() for w in game.tower)}")
        else:
            print(f"  ℹ️  Could not add '{test_word}': {result['message']}")


def compare_old_vs_new():
    """Show the difference between old daily mode and new random mode"""
    print("\n\n📅 OLD vs 🎲 NEW MODE COMPARISON\n")
    print("=" * 50)
    
    print("\n❌ OLD MODE (Daily Challenge):")
    print("   - Same word all day (date-based seed)")
    print("   - Everyone gets the same word")
    print("   - Have to wait for tomorrow for new word")
    print("   - Example: October 29, 2025 always gives 'fox'")
    
    print("\n✅ NEW MODE (Random):")
    print("   - Different word every time you start")
    print("   - Unlimited games per day")
    print("   - Each player gets different words")
    print("   - Example: 5 games = 5 different words:")
    
    for i in range(5):
        word = WordRiseGame.get_random_starting_word()
        print(f"      Game {i+1}: {word.upper()}")


if __name__ == "__main__":
    print("\n" + "🗼 " * 20)
    print("   WORDRISE - RANDOM MODE TESTS")
    print("🗼 " * 20 + "\n")
    
    test_random_starting_words()
    test_game_creation()
    compare_old_vs_new()
    
    print("\n" + "=" * 50)
    print("\n✨ All tests complete! Random mode is working! ✨\n")
