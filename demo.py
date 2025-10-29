#!/usr/bin/env python3
"""
Interactive WordRise Demo
Play a quick game in the terminal to test the game engine
"""
import sys
from datetime import date
from app.game_engine import WordRiseGame


def print_tower(tower):
    """Print the tower visually"""
    print("\n" + "="*50)
    print("YOUR TOWER:")
    print("="*50)
    for i, word in enumerate(reversed(tower), 1):
        level = len(tower) - i + 1
        spaces = " " * (10 - len(word))
        print(f"Level {level}: {spaces}[ {word.upper()} ]")
    print("="*50 + "\n")


def print_game_info(game):
    """Print current game information"""
    state = game.get_game_state()
    print(f"\n📊 Current Word: {state['current_word'].upper()}")
    print(f"📏 Next word must be: {len(state['current_word']) + 1} letters")
    print(f"🔤 Must use these letters: {', '.join(sorted(state['current_word'].upper()))}")
    print(f"💡 Hints used: {state['hints_used']}")


def play_game():
    """Main game loop"""
    print("\n" + "🏗️ "*20)
    print("WELCOME TO WORDRISE!")
    print("🏗️ "*20)
    
    print("\n📖 HOW TO PLAY:")
    print("1. Build a tower by stacking words")
    print("2. Each new word must use ALL letters from the word below")
    print("3. Add EXACTLY ONE new letter")
    print("4. Rearrange letters in any order")
    print("\nCommands: 'hint' for help, 'undo' to go back, 'quit' to end")
    
    # Choose game mode
    print("\n" + "="*50)
    mode = input("Play (d)aily challenge or (p)ractice mode? [d/p]: ").lower()
    
    if mode == 'd':
        starting_word = WordRiseGame.get_daily_word()
        print(f"\n🗓️  Today's Daily Challenge #{date.today().strftime('%Y%m%d')}")
    else:
        # Let user choose or random
        choice = input("Enter starting word (3 letters) or press Enter for random: ").lower()
        if choice and len(choice) == 3:
            starting_word = choice
        else:
            game_temp = WordRiseGame()
            starting_word = game_temp.validator.get_random_word(3)
    
    # Create game
    game = WordRiseGame(starting_word=starting_word)
    
    print(f"\n✨ Starting word: {starting_word.upper()}")
    print_tower(game.tower)
    
    # Game loop
    while True:
        print_game_info(game)
        
        # Get user input
        user_input = input("\n➤ Enter your word: ").lower().strip()
        
        # Handle commands
        if not user_input:
            continue
        
        if user_input == 'quit':
            print("\n👋 Thanks for playing!")
            break
        
        elif user_input == 'hint':
            hint_result = game.get_hint('starts_with')
            if hint_result['success']:
                print(f"\n💡 HINT: {hint_result['hint']}")
                print(f"   (There are {hint_result['possible_words_count']} possible words)")
            else:
                print(f"\n🎉 {hint_result['message']}")
            continue
        
        elif user_input == 'undo':
            undo_result = game.undo_last_word()
            if undo_result['success']:
                print(f"\n↩️  {undo_result['message']}")
                print_tower(game.tower)
            else:
                print(f"\n❌ {undo_result['message']}")
            continue
        
        elif user_input == 'reset':
            game.reset_game()
            print("\n🔄 Game reset!")
            print_tower(game.tower)
            continue
        
        # Try to add word
        result = game.add_word(user_input)
        
        if result['success']:
            print(f"\n✅ SUCCESS! {result['message']}")
            print(f"   Tower height: {result['tower_height']} levels")
            print_tower(game.tower)
            
            # Check if no more moves possible
            hint_check = game.get_hint()
            if not hint_check['success']:
                print("\n🎊 AMAZING! You've reached the maximum height!")
                print("   No more words can be added!")
                break
        else:
            print(f"\n❌ {result['message']}")
            print("   Try again or type 'hint' for help!")
    
    # End game and show results
    print("\n" + "🎉 "*20)
    results = game.end_game()
    
    print("\nFINAL RESULTS")
    print("="*50)
    print(f"🏗️  Tower Height: {results['height']} levels")
    print(f"⏱️  Time Taken: {results['time_seconds']}s")
    print(f"💡 Hints Used: {results['hints_used']}")
    print(f"🎯 Final Score: {results['total_score']} points")
    print("="*50)
    
    print("\n📊 SCORE BREAKDOWN:")
    print("-"*50)
    for item in results['breakdown']:
        bonus_str = f" (+{item['letter_bonus']} bonus)" if item['letter_bonus'] > 0 else ""
        print(f"Level {item['level']}: {item['word'].upper():10} = {item['base_points']:3} pts{bonus_str}")
    print("-"*50)
    print(f"Base Score:     {results['base_score']:3} pts")
    print(f"Letter Bonuses: {results['letter_bonus']:3} pts")
    print(f"Speed Bonus:    {results['speed_bonus']:3} pts")
    print(f"TOTAL SCORE:    {results['total_score']:3} pts")
    print("="*50)
    
    print("\n📤 Share your score:")
    print(f"🏗️ WordRise #{date.today().strftime('%m/%d/%Y')}")
    print(f"{'🟩' * results['height']} ({results['height']} levels, {results['total_score']} pts)")
    print("wordrise.app")
    
    # Play again?
    print("\n")
    again = input("Play again? [y/n]: ").lower()
    if again == 'y':
        print("\n" * 2)
        play_game()


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing WordRise!")
        sys.exit(0)
