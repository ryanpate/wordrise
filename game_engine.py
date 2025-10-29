"""
WordRise Game Engine
Core game logic for word tower building

Enhanced with Hybrid Word Validation:
- Primary: Local JSON cache (3,154 curated words) - instant validation
- Fallback: Datamuse API (100,000+ words) - for extended vocabulary
"""
import json
import os
from collections import Counter
from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
import random
from functools import lru_cache
import requests


import requests


class DatamuseAPIValidator:
    """
    Datamuse API word validator with caching
    Used as fallback when word not in local cache
    """
    
    BASE_URL = "https://api.datamuse.com/words"
    
    @staticmethod
    @lru_cache(maxsize=10000)  # Cache up to 10,000 API lookups
    def is_valid_word(word: str) -> bool:
        """
        Check if a word is valid using Datamuse API
        
        Args:
            word: Word to validate
            
        Returns:
            True if word is valid, False otherwise
        """
        word = word.lower().strip()
        
        try:
            response = requests.get(
                DatamuseAPIValidator.BASE_URL,
                params={"sp": word, "max": 1},
                timeout=2  # 2 second timeout
            )
            
            if response.status_code == 200:
                results = response.json()
                # Check for exact match (case-insensitive)
                return len(results) > 0 and results[0]['word'].lower() == word
            
            return False
            
        except requests.exceptions.RequestException:
            # If API fails, return False (don't block gameplay)
            # The local cache should handle most words anyway
            return False
    
    @staticmethod
    @lru_cache(maxsize=1000)
    def get_word_frequency(word: str) -> float:
        """
        Get word frequency score from Datamuse
        Higher score = more common word
        
        Args:
            word: Word to check frequency for
            
        Returns:
            Frequency score (0.0 if not found or API fails)
        """
        try:
            response = requests.get(
                DatamuseAPIValidator.BASE_URL,
                params={"sp": word, "md": "f", "max": 1},
                timeout=2
            )
            
            if response.status_code == 200:
                results = response.json()
                if results and 'tags' in results[0]:
                    for tag in results[0].get('tags', []):
                        if tag.startswith('f:'):
                            return float(tag.split(':')[1])
            
            return 0.0
            
        except:
            return 0.0


class WordValidator:
    """Handles word validation and dictionary lookups with hybrid local + API approach"""
    
    def __init__(self, data_dir: str = None, use_api_fallback: bool = True):
        """
        Initialize word validator
        
        Args:
            data_dir: Path to word data directory
            use_api_fallback: If True, uses Datamuse API when word not in local cache
        """
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        self.data_dir = data_dir
        self.use_api_fallback = use_api_fallback
        self.words_set = self._load_words()
        self.words_by_length = self._load_words_by_length()
        self.api_validator = DatamuseAPIValidator() if use_api_fallback else None
        
        # Statistics tracking
        self.stats = {
            'local_hits': 0,
            'api_hits': 0,
            'api_misses': 0
        }
    
    def _load_words(self) -> set:
        """Load all valid words into a set for fast lookup"""
        words_file = os.path.join(self.data_dir, 'words.json')
        with open(words_file, 'r') as f:
            data = json.load(f)
            return set(data['words'])
    
    def _load_words_by_length(self) -> Dict[int, List[str]]:
        """Load words organized by length"""
        index_file = os.path.join(self.data_dir, 'words_by_length.json')
        with open(index_file, 'r') as f:
            data = json.load(f)
            # Convert string keys to integers
            return {int(k): v for k, v in data.items()}
    
    def is_valid_word(self, word: str) -> bool:
        """
        Check if a word is valid using hybrid approach:
        1. Check local cache first (instant - 3,154 curated words)
        2. If not found and API enabled, check Datamuse API (100,000+ words)
        
        Args:
            word: Word to validate
            
        Returns:
            True if word is valid
        """
        word_lower = word.lower()
        
        # First, check local cache (instant)
        if word_lower in self.words_set:
            self.stats['local_hits'] += 1
            return True
        
        # If not in local cache and API fallback enabled, check API
        if self.use_api_fallback and self.api_validator:
            is_valid = self.api_validator.is_valid_word(word_lower)
            if is_valid:
                self.stats['api_hits'] += 1
                # Optionally: add to local cache for next time
                self.words_set.add(word_lower)
            else:
                self.stats['api_misses'] += 1
            return is_valid
        
        # Not found in local cache and no API fallback
        return False
    
    def get_words_of_length(self, length: int) -> List[str]:
        """Get all words of a specific length"""
        return self.words_by_length.get(length, [])
    
    def get_random_word(self, length: int) -> Optional[str]:
        """Get a random word of specific length"""
        words = self.get_words_of_length(length)
        return random.choice(words) if words else None
    
    def get_validation_stats(self) -> Dict:
        """
        Get statistics about word validation performance
        
        Returns:
            Dict with local_hits, api_hits, api_misses counts
        """
        total = sum(self.stats.values())
        return {
            **self.stats,
            'total_validations': total,
            'local_hit_rate': f"{(self.stats['local_hits'] / total * 100):.1f}%" if total > 0 else "0%",
            'api_enabled': self.use_api_fallback
        }
    
    def set_api_fallback(self, enabled: bool):
        """
        Enable or disable API fallback
        
        Args:
            enabled: True to enable Datamuse API fallback, False for local-only
        """
        self.use_api_fallback = enabled
        if enabled and not self.api_validator:
            self.api_validator = DatamuseAPIValidator()


class TowerValidator:
    """Validates tower building rules"""
    
    @staticmethod
    def can_build_word(base_word: str, new_word: str) -> Tuple[bool, str]:
        """
        Check if new_word can be built on top of base_word
        
        Rules:
        1. Must use ALL letters from base_word
        2. Must add exactly ONE new letter
        3. Can rearrange letters in any order
        
        Returns:
            (is_valid, message) tuple
        """
        base_word = base_word.lower()
        new_word = new_word.lower()
        
        # Check length
        if len(new_word) != len(base_word) + 1:
            return False, f"Word must be exactly {len(base_word) + 1} letters long"
        
        # Count letters in each word
        base_counter = Counter(base_word)
        new_counter = Counter(new_word)
        
        # Check if base letters are all present in new word
        for letter, count in base_counter.items():
            if new_counter[letter] < count:
                return False, f"Must use all letters from '{base_word}'"
        
        # Check if exactly one letter was added
        added_letters = []
        for letter, count in new_counter.items():
            base_count = base_counter.get(letter, 0)
            if count > base_count:
                added_letters.extend([letter] * (count - base_count))
        
        if len(added_letters) != 1:
            return False, "Must add exactly one new letter"
        
        return True, f"Added letter: {added_letters[0].upper()}"
    
    @staticmethod
    def get_added_letter(base_word: str, new_word: str) -> Optional[str]:
        """Get the letter that was added to create new_word"""
        base_counter = Counter(base_word.lower())
        new_counter = Counter(new_word.lower())
        
        for letter, count in new_counter.items():
            base_count = base_counter.get(letter, 0)
            if count > base_count:
                return letter
        
        return None


class ScoreCalculator:
    """Calculates scores for towers"""
    
    # Letter rarity bonuses
    UNCOMMON_LETTERS = {'q', 'z', 'x', 'j', 'k'}
    UNCOMMON_BONUS = 5
    
    @staticmethod
    def calculate_tower_score(tower: List[str], time_seconds: Optional[int] = None) -> Dict:
        """
        Calculate total score for a tower
        
        Score = Sum of (word_length × level_multiplier) + bonuses
        
        Returns dict with detailed scoring breakdown
        """
        if not tower:
            return {
                'total_score': 0,
                'base_score': 0,
                'letter_bonus': 0,
                'speed_bonus': 0,
                'height': 0,
                'breakdown': []
            }
        
        base_score = 0
        letter_bonus = 0
        breakdown = []
        
        # Calculate base score and letter bonuses
        for level, word in enumerate(tower, 1):
            word_score = len(word) * level
            base_score += word_score
            
            # Letter rarity bonus
            word_letter_bonus = 0
            for letter in word.lower():
                if letter in ScoreCalculator.UNCOMMON_LETTERS:
                    word_letter_bonus += ScoreCalculator.UNCOMMON_BONUS
            
            letter_bonus += word_letter_bonus
            
            breakdown.append({
                'level': level,
                'word': word,
                'length': len(word),
                'multiplier': level,
                'base_points': word_score,
                'letter_bonus': word_letter_bonus
            })
        
        # Speed bonus (10% if completed in under 5 minutes)
        speed_bonus = 0
        if time_seconds and time_seconds < 300:  # 5 minutes
            speed_bonus = int((base_score + letter_bonus) * 0.1)
        
        total_score = base_score + letter_bonus + speed_bonus
        
        return {
            'total_score': total_score,
            'base_score': base_score,
            'letter_bonus': letter_bonus,
            'speed_bonus': speed_bonus,
            'height': len(tower),
            'time_seconds': time_seconds,
            'breakdown': breakdown
        }


class WordRiseGame:
    """Main game engine for WordRise"""
    
    def __init__(self, starting_word: Optional[str] = None, data_dir: str = None):
        """
        Initialize a new game
        
        Args:
            starting_word: Initial word (if None, will use daily word or random)
            data_dir: Path to word data directory
        """
        self.validator = WordValidator(data_dir)
        self.tower_validator = TowerValidator()
        self.score_calculator = ScoreCalculator()
        
        # Game state
        self.tower: List[str] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.hints_used: int = 0
        
        # Initialize with starting word
        if starting_word:
            self.starting_word = starting_word.lower()
        else:
            # Use 3-letter word as default
            self.starting_word = self.validator.get_random_word(3) or 'cat'
        
        self.tower.append(self.starting_word)
        self.start_time = datetime.now()
    
    def get_current_word(self) -> str:
        """Get the current top word of the tower"""
        return self.tower[-1] if self.tower else ""
    
    def get_tower_height(self) -> int:
        """Get current tower height"""
        return len(self.tower)
    
    def add_word(self, word: str) -> Dict:
        """
        Attempt to add a word to the tower
        
        Returns dict with success status and message
        """
        word = word.lower().strip()
        
        # Validate word exists
        if not self.validator.is_valid_word(word):
            return {
                'success': False,
                'message': f"'{word}' is not a valid word"
            }
        
        # Check if word already used
        if word in self.tower:
            return {
                'success': False,
                'message': f"'{word}' has already been used"
            }
        
        # Validate tower building rules
        current_word = self.get_current_word()
        is_valid, message = self.tower_validator.can_build_word(current_word, word)
        
        if not is_valid:
            return {
                'success': False,
                'message': message
            }
        
        # Add word to tower
        self.tower.append(word)
        added_letter = self.tower_validator.get_added_letter(current_word, word)
        
        return {
            'success': True,
            'message': message,
            'word': word,
            'added_letter': added_letter,
            'tower_height': self.get_tower_height(),
            'current_letters': sorted(word)
        }
    
    def undo_last_word(self) -> Dict:
        """Remove the last word from tower (can't remove starting word)"""
        if len(self.tower) <= 1:
            return {
                'success': False,
                'message': "Cannot undo starting word"
            }
        
        removed_word = self.tower.pop()
        return {
            'success': True,
            'message': f"Removed '{removed_word}'",
            'tower_height': self.get_tower_height(),
            'current_word': self.get_current_word()
        }
    
    def reset_game(self):
        """Reset to starting word"""
        self.tower = [self.starting_word]
        self.start_time = datetime.now()
        self.end_time = None
        self.hints_used = 0
    
    def end_game(self) -> Dict:
        """Mark game as ended and calculate final score"""
        self.end_time = datetime.now()
        
        # Calculate time taken
        time_taken = None
        if self.start_time and self.end_time:
            time_taken = int((self.end_time - self.start_time).total_seconds())
        
        # Calculate score
        score_data = self.score_calculator.calculate_tower_score(self.tower, time_taken)
        
        return {
            'tower': self.tower.copy(),
            'height': self.get_tower_height(),
            'starting_word': self.starting_word,
            'time_seconds': time_taken,
            'hints_used': self.hints_used,
            **score_data
        }
    
    def get_hint(self, hint_type: str = 'definition') -> Dict:
        """
        Get a hint for the next possible word
        
        hint_type: 'definition', 'starts_with', 'contains', 'length'
        """
        self.hints_used += 1
        current_word = self.get_current_word()
        current_letters = sorted(current_word)
        target_length = len(current_word) + 1
        
        # Find possible next words
        possible_words = []
        for word in self.validator.get_words_of_length(target_length):
            if word not in self.tower:
                is_valid, _ = self.tower_validator.can_build_word(current_word, word)
                if is_valid:
                    possible_words.append(word)
        
        if not possible_words:
            return {
                'success': False,
                'message': "No more words possible! Great job reaching the top!"
            }
        
        # Pick a random possible word for hint
        hint_word = random.choice(possible_words)
        
        hints = {
            'starts_with': f"Try a word starting with '{hint_word[0].upper()}'",
            'contains': f"Try a word containing '{hint_word[len(hint_word)//2].upper()}'",
            'length': f"The next word should be {target_length} letters long",
            'definition': f"Try a {target_length}-letter word (like '{hint_word[:2]}...')"
        }
        
        return {
            'success': True,
            'hint': hints.get(hint_type, hints['definition']),
            'possible_words_count': len(possible_words)
        }
    
    def get_game_state(self) -> Dict:
        """Get current game state"""
        return {
            'tower': self.tower.copy(),
            'height': self.get_tower_height(),
            'current_word': self.get_current_word(),
            'starting_word': self.starting_word,
            'hints_used': self.hints_used,
            'is_active': self.end_time is None
        }
    
    def get_validation_stats(self) -> Dict:
        """Get word validation statistics (local vs API usage)"""
        return self.validator.get_validation_stats()
    
    def set_api_fallback(self, enabled: bool):
        """
        Enable or disable Datamuse API fallback for word validation
        
        Args:
            enabled: True for hybrid mode (local + API), False for local-only
        """
        self.validator.set_api_fallback(enabled)
    
    @staticmethod
    def get_random_starting_word() -> str:
        """
        Get a random 3-letter word for starting a new game
        Returns a different word each time for unlimited replayability
        """
        # Always return random 3-letter word
        validator = WordValidator()
        three_letter_words = validator.get_words_of_length(3)
        
        if not three_letter_words:
            return 'cat'
        
        # Return a truly random word (no date-based seed)
        return random.choice(three_letter_words)


# Helper function for quick game testing
def play_test_game():
    """Quick test of game engine with hybrid word validation"""
    print("🗼 WORDRISE GAME ENGINE TEST (Hybrid Mode)\n")
    
    game = WordRiseGame(starting_word='art')
    print(f"Starting word: {game.starting_word.upper()}")
    print(f"Tower: {' → '.join(word.upper() for word in game.tower)}")
    print(f"API Fallback: {'ENABLED' if game.validator.use_api_fallback else 'DISABLED'}\n")
    
    # Test adding words
    test_words = ['tart', 'start', 'stray']
    
    for word in test_words:
        print(f"Attempting to add: {word.upper()}")
        result = game.add_word(word)
        
        if result['success']:
            print(f"✓ Success! {result['message']}")
            print(f"  Tower: {' → '.join(w.upper() for w in game.tower)}")
        else:
            print(f"✗ Failed: {result['message']}")
        print()
    
    # Show validation stats
    print("📊 Validation Statistics:")
    stats = game.get_validation_stats()
    print(f"  Local cache hits: {stats['local_hits']}")
    print(f"  API lookups: {stats['api_hits']}")
    print(f"  Invalid words: {stats['api_misses']}")
    print(f"  Local hit rate: {stats['local_hit_rate']}")
    print()
    
    # Get hint
    print("Getting hint...")
    hint = game.get_hint('starts_with')
    if hint['success']:
        print(f"💡 {hint['hint']}")
        print(f"   ({hint['possible_words_count']} possible words)\n")
    
    # End game and show score
    print("Ending game...")
    final = game.end_game()
    print(f"\n🎉 FINAL RESULTS")
    print(f"Height: {final['height']} levels")
    print(f"Score: {final['total_score']} points")
    print(f"Time: {final['time_seconds']}s")
    print(f"\nTower: {' → '.join(w.upper() for w in final['tower'])}")
    
    print(f"\nScore Breakdown:")
    for item in final['breakdown']:
        print(f"  Level {item['level']}: {item['word'].upper()} = {item['base_points']} pts " +
              f"(+{item['letter_bonus']} letter bonus)")
    
    # Final stats
    print(f"\n📈 Final Validation Stats:")
    final_stats = game.get_validation_stats()
    print(f"  Total validations: {final_stats['total_validations']}")
    print(f"  Local hit rate: {final_stats['local_hit_rate']}")
    print(f"  API was used: {'Yes' if final_stats['api_hits'] > 0 else 'No'}")


if __name__ == "__main__":
    play_test_game()
