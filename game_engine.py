"""
WordRise Game Engine
Core game logic for word tower building

Enhanced with Hybrid Word Validation:
- Primary: Local JSON cache (3,154 curated words) - instant validation
- Fallback: Datamuse API (100,000+ words) - for extended vocabulary

Enhanced Hint System:
- Better hint quality with more information
- Word definition support via Datamuse API
- Multiple hint strategies
- Clear messaging when no words are available
"""
import json
import os
from collections import Counter
from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
import random
from functools import lru_cache
import requests


class DatamuseAPIValidator:
    """
    Datamuse API word validator with caching and definition support
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
    
    @staticmethod
    @lru_cache(maxsize=500)
    def get_word_definition(word: str) -> Optional[str]:
        """
        Get a definition for a word using Datamuse API
        
        Args:
            word: Word to get definition for
            
        Returns:
            Definition string or None if not available
        """
        try:
            response = requests.get(
                DatamuseAPIValidator.BASE_URL,
                params={"sp": word, "md": "d", "max": 1},
                timeout=2
            )
            
            if response.status_code == 200:
                results = response.json()
                if results and len(results) > 0:
                    # Get definitions from the result
                    defs = results[0].get('defs', [])
                    if defs:
                        # Return first definition, cleaned up
                        definition = defs[0]
                        # Remove part of speech tags like "n\t" or "v\t"
                        if '\t' in definition:
                            definition = definition.split('\t', 1)[1]
                        return definition
            
            return None
            
        except:
            return None
    
    @staticmethod
    @lru_cache(maxsize=500)
    def get_related_words(word: str, rel_type: str = "syn") -> List[str]:
        """
        Get related words (synonyms, rhymes, etc.)
        
        Args:
            word: Base word
            rel_type: Relationship type (syn=synonyms, rhy=rhymes, etc.)
            
        Returns:
            List of related words
        """
        try:
            response = requests.get(
                DatamuseAPIValidator.BASE_URL,
                params={"rel_" + rel_type: word, "max": 5},
                timeout=2
            )
            
            if response.status_code == 200:
                results = response.json()
                return [r['word'] for r in results[:3]]
            
            return []
            
        except:
            return []


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
        
        # Count how many NEW letters were added
        added_letters = []
        for letter, count in new_counter.items():
            base_count = base_counter.get(letter, 0)
            if count > base_count:
                added_letters.extend([letter] * (count - base_count))
        
        if len(added_letters) != 1:
            return False, "Must add exactly one new letter"
        
        return True, f"Added '{added_letters[0].upper()}' to build '{new_word.upper()}'!"
    
    @staticmethod
    def get_added_letter(base_word: str, new_word: str) -> str:
        """Get the letter that was added to build new word"""
        base_counter = Counter(base_word.lower())
        new_counter = Counter(new_word.lower())
        
        for letter, count in new_counter.items():
            base_count = base_counter.get(letter, 0)
            if count > base_count:
                return letter.upper()
        
        return ""


class ScoreCalculator:
    """Calculates scores for towers and individual words"""
    
    @staticmethod
    def calculate_word_score(word: str, position: int) -> Dict:
        """
        Calculate score for a single word
        
        Position multiplier increases as tower grows
        Rare letters give bonus points
        """
        base_points = len(word) * 10
        position_multiplier = 1 + (position * 0.1)
        
        # Bonus for rare letters
        rare_letters = {'q': 10, 'z': 10, 'x': 8, 'j': 8, 'k': 5}
        letter_bonus = sum(rare_letters.get(letter.lower(), 0) for letter in word)
        
        total = int((base_points + letter_bonus) * position_multiplier)
        
        return {
            'base_points': base_points,
            'position_multiplier': position_multiplier,
            'letter_bonus': letter_bonus,
            'total': total
        }
    
    @staticmethod
    def calculate_tower_score(tower: List[str], time_seconds: Optional[int] = None) -> Dict:
        """Calculate total score for entire tower"""
        breakdown = []
        total_score = 0
        
        for i, word in enumerate(tower):
            score_data = ScoreCalculator.calculate_word_score(word, i)
            breakdown.append({
                'level': i + 1,
                'word': word,
                **score_data
            })
            total_score += score_data['total']
        
        # Time bonus (faster completion = bonus points)
        time_bonus = 0
        if time_seconds is not None and time_seconds > 0:
            # Bonus diminishes over time
            if time_seconds < 60:
                time_bonus = 100
            elif time_seconds < 120:
                time_bonus = 50
            elif time_seconds < 180:
                time_bonus = 25
        
        return {
            'breakdown': breakdown,
            'subtotal': total_score,
            'time_bonus': time_bonus,
            'total_score': total_score + time_bonus
        }


class WordRiseGame:
    """Main game engine for WordRise"""
    
    def __init__(self, starting_word: Optional[str] = None, data_dir: str = None):
        """
        Initialize a new game
        
        Args:
            starting_word: Word to start tower with (random if None)
            data_dir: Path to word data directory
        """
        self.validator = WordValidator(data_dir)
        self.tower_validator = TowerValidator()
        self.score_calculator = ScoreCalculator()
        
        # Initialize tower with starting word
        if starting_word is None:
            starting_word = self.validator.get_random_word(3)
        
        self.starting_word = starting_word.lower()
        self.tower = [self.starting_word]
        
        # Game state
        self.start_time = datetime.now()
        self.end_time = None
        self.hints_used = 0
    
    def get_current_word(self) -> str:
        """Get the top word of the tower"""
        return self.tower[-1]
    
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
    
    def get_hint(self, hint_type: str = 'smart') -> Dict:
        """
        Get an enhanced hint for the next possible word
        
        hint_type options:
        - 'smart': Intelligent hint based on difficulty (default)
        - 'pattern': Show letter pattern (e.g., "S__R_")
        - 'starts_with': First letter only
        - 'contains': A letter that's in the word
        - 'definition': Word definition (requires API)
        - 'length': Just the length
        """
        self.hints_used += 1
        current_word = self.get_current_word()
        target_length = len(current_word) + 1
        
        # Find possible next words
        possible_words = []
        for word in self.validator.get_words_of_length(target_length):
            if word not in self.tower:
                is_valid, _ = self.tower_validator.can_build_word(current_word, word)
                if is_valid:
                    possible_words.append(word)
        
        # No words available - give helpful message
        if not possible_words:
            height = self.get_tower_height()
            messages = [
                f"🎉 Incredible! You've reached the maximum height of {height} words!",
                f"🏆 Amazing job! No more words can be built from '{current_word.upper()}'.",
                f"👏 You've mastered this tower! There are no available {target_length}-letter words using these letters.",
                f"⭐ Outstanding! Your tower of {height} words is complete - no further words possible!"
            ]
            
            return {
                'success': False,
                'message': random.choice(messages),
                'no_words_available': True,
                'tower_height': height,
                'final_word': current_word.upper()
            }
        
        # Sort by frequency if we have API access (show common words first)
        if self.validator.use_api_fallback and len(possible_words) > 1:
            try:
                word_scores = [(w, DatamuseAPIValidator.get_word_frequency(w)) for w in possible_words[:20]]
                word_scores.sort(key=lambda x: x[1], reverse=True)
                # Use top 5 most common words for hints
                possible_words = [w for w, _ in word_scores[:5]]
            except:
                pass
        
        # Pick a word for the hint (prefer common words)
        hint_word = random.choice(possible_words[:5] if len(possible_words) > 5 else possible_words)
        
        # Generate hint based on type
        if hint_type == 'pattern':
            # Show some letters, hide others (S_A_T for START)
            pattern = ''
            reveal_positions = sorted(random.sample(range(len(hint_word)), min(2, len(hint_word))))
            for i, letter in enumerate(hint_word):
                if i in reveal_positions:
                    pattern += letter.upper()
                else:
                    pattern += '_'
            hint_text = f"Try a {target_length}-letter word with pattern: {pattern}"
        
        elif hint_type == 'starts_with':
            hint_text = f"Try a {target_length}-letter word starting with '{hint_word[0].upper()}'"
        
        elif hint_type == 'contains':
            # Pick a letter that's less common
            letter = hint_word[len(hint_word)//2]
            hint_text = f"Try a {target_length}-letter word containing the letter '{letter.upper()}'"
        
        elif hint_type == 'definition':
            # Try to get actual definition from API
            definition = None
            if self.validator.use_api_fallback:
                definition = DatamuseAPIValidator.get_word_definition(hint_word)
            
            if definition:
                hint_text = f"Definition: {definition}"
            else:
                # Fallback to pattern hint
                first_half = len(hint_word) // 2
                hint_text = f"Try a {target_length}-letter word (like '{hint_word[:first_half].upper()}...')"
        
        elif hint_type == 'length':
            hint_text = f"The next word should be {target_length} letters long"
        
        else:  # 'smart' - adaptive hint based on tower height
            height = self.get_tower_height()
            
            if height <= 3:
                # Early game - easier hints (show more letters)
                first_letters = hint_word[:2]
                hint_text = f"Try a {target_length}-letter word starting with '{first_letters.upper()}...'"
            
            elif height <= 6:
                # Mid game - medium difficulty (pattern)
                reveal_count = max(1, target_length // 3)
                reveal_positions = sorted(random.sample(range(len(hint_word)), reveal_count))
                pattern = ''.join(hint_word[i].upper() if i in reveal_positions else '_' 
                                for i in range(len(hint_word)))
                hint_text = f"Try matching this pattern: {pattern}"
            
            else:
                # Late game - harder hints (just first letter or definition)
                if self.validator.use_api_fallback and random.random() < 0.5:
                    definition = DatamuseAPIValidator.get_word_definition(hint_word)
                    if definition:
                        hint_text = f"Hint: {definition}"
                    else:
                        hint_text = f"Try a {target_length}-letter word starting with '{hint_word[0].upper()}'"
                else:
                    hint_text = f"Try a {target_length}-letter word starting with '{hint_word[0].upper()}'"
        
        return {
            'success': True,
            'hint': hint_text,
            'possible_words_count': len(possible_words),
            'current_height': self.get_tower_height(),
            'target_length': target_length
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
    """Quick test of game engine with enhanced hints"""
    print("🗼 WORDRISE GAME ENGINE TEST (Enhanced Hints)\n")
    
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
    
    # Test different hint types
    print("📝 Testing Enhanced Hints:")
    hint_types = ['smart', 'pattern', 'starts_with', 'definition']
    
    for hint_type in hint_types:
        hint = game.get_hint(hint_type)
        if hint['success']:
            print(f"\n💡 {hint_type.upper()} hint:")
            print(f"   {hint['hint']}")
            print(f"   ({hint['possible_words_count']} possible words)")
        else:
            print(f"\n⚠️  {hint['message']}")
    
    # Show validation stats
    print("\n📊 Validation Statistics:")
    stats = game.get_validation_stats()
    print(f"  Local cache hits: {stats['local_hits']}")
    print(f"  API lookups: {stats['api_hits']}")
    print(f"  Invalid words: {stats['api_misses']}")
    print(f"  Local hit rate: {stats['local_hit_rate']}")
    
    # End game and show score
    print("\nEnding game...")
    final = game.end_game()
    print(f"\n🎉 FINAL RESULTS")
    print(f"Height: {final['height']} levels")
    print(f"Score: {final['total_score']} points")
    print(f"Time: {final['time_seconds']}s")
    print(f"\nTower: {' → '.join(w.upper() for w in final['tower'])}")


if __name__ == "__main__":
    play_test_game()
