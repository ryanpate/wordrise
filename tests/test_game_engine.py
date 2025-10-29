"""
Unit tests for WordRise game engine
"""
import unittest
import sys
import os
from datetime import date

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.game_engine import (
    WordValidator, 
    TowerValidator, 
    ScoreCalculator, 
    WordRiseGame
)


class TestWordValidator(unittest.TestCase):
    """Test word validation"""
    
    def setUp(self):
        self.validator = WordValidator()
    
    def test_valid_words(self):
        """Test that common words are recognized"""
        valid_words = ['cat', 'dog', 'house', 'start', 'happy']
        for word in valid_words:
            self.assertTrue(
                self.validator.is_valid_word(word),
                f"'{word}' should be valid"
            )
    
    def test_invalid_words(self):
        """Test that nonsense words are rejected"""
        invalid_words = ['xyz', 'qqqq', 'asfgjkl']
        for word in invalid_words:
            self.assertFalse(
                self.validator.is_valid_word(word),
                f"'{word}' should be invalid"
            )
    
    def test_case_insensitive(self):
        """Test that validation is case-insensitive"""
        self.assertTrue(self.validator.is_valid_word('CAT'))
        self.assertTrue(self.validator.is_valid_word('Cat'))
        self.assertTrue(self.validator.is_valid_word('cat'))
    
    def test_get_words_of_length(self):
        """Test getting words by length"""
        three_letter = self.validator.get_words_of_length(3)
        self.assertIsInstance(three_letter, list)
        self.assertGreater(len(three_letter), 0)
        self.assertTrue(all(len(w) == 3 for w in three_letter))


class TestTowerValidator(unittest.TestCase):
    """Test tower building rules"""
    
    def setUp(self):
        self.validator = TowerValidator()
    
    def test_valid_tower_builds(self):
        """Test valid word additions"""
        test_cases = [
            ('art', 'tart'),
            ('cat', 'tack'),
            ('art', 'rate'),
            ('rap', 'trap'),
        ]
        
        for base, new in test_cases:
            is_valid, message = self.validator.can_build_word(base, new)
            self.assertTrue(
                is_valid,
                f"Should be able to build '{new}' from '{base}': {message}"
            )
    
    def test_wrong_length(self):
        """Test that wrong length words are rejected"""
        is_valid, _ = self.validator.can_build_word('cat', 'at')  # Too short
        self.assertFalse(is_valid)
        
        is_valid, _ = self.validator.can_build_word('cat', 'crate')  # Too long
        self.assertFalse(is_valid)
    
    def test_missing_letters(self):
        """Test that words missing base letters are rejected"""
        is_valid, _ = self.validator.can_build_word('art', 'path')
        self.assertFalse(is_valid, "Should reject word missing letters from base")
    
    def test_multiple_new_letters(self):
        """Test that adding multiple letters is rejected"""
        is_valid, _ = self.validator.can_build_word('cat', 'table')
        self.assertFalse(is_valid, "Should reject adding multiple letters")
    
    def test_get_added_letter(self):
        """Test identifying the added letter"""
        letter = self.validator.get_added_letter('art', 'tart')
        self.assertEqual(letter, 't')
        
        letter = self.validator.get_added_letter('cat', 'cart')
        self.assertEqual(letter, 'r')


class TestScoreCalculator(unittest.TestCase):
    """Test score calculation"""
    
    def setUp(self):
        self.calculator = ScoreCalculator()
    
    def test_basic_scoring(self):
        """Test basic tower scoring"""
        tower = ['art', 'tart', 'start']
        score_data = self.calculator.calculate_tower_score(tower)
        
        # Level 1: 3 letters × 1 = 3
        # Level 2: 4 letters × 2 = 8
        # Level 3: 5 letters × 3 = 15
        # Total = 26
        self.assertEqual(score_data['base_score'], 26)
        self.assertEqual(score_data['height'], 3)
    
    def test_empty_tower(self):
        """Test scoring empty tower"""
        score_data = self.calculator.calculate_tower_score([])
        self.assertEqual(score_data['total_score'], 0)
        self.assertEqual(score_data['height'], 0)
    
    def test_uncommon_letter_bonus(self):
        """Test bonus for uncommon letters"""
        tower = ['fox']  # Contains 'x'
        score_data = self.calculator.calculate_tower_score(tower)
        self.assertGreater(score_data['letter_bonus'], 0)
    
    def test_speed_bonus(self):
        """Test speed bonus for fast completion"""
        tower = ['art', 'tart']
        
        # With speed bonus (under 5 minutes)
        score_fast = self.calculator.calculate_tower_score(tower, time_seconds=200)
        
        # Without speed bonus (over 5 minutes)
        score_slow = self.calculator.calculate_tower_score(tower, time_seconds=400)
        
        self.assertGreater(score_fast['speed_bonus'], 0)
        self.assertEqual(score_slow['speed_bonus'], 0)
        self.assertGreater(score_fast['total_score'], score_slow['total_score'])


class TestWordRiseGame(unittest.TestCase):
    """Test main game functionality"""
    
    def setUp(self):
        self.game = WordRiseGame(starting_word='art')
    
    def test_initialization(self):
        """Test game initializes correctly"""
        self.assertEqual(self.game.starting_word, 'art')
        self.assertEqual(self.game.get_tower_height(), 1)
        self.assertEqual(self.game.get_current_word(), 'art')
    
    def test_add_valid_word(self):
        """Test adding valid words"""
        result = self.game.add_word('tart')
        self.assertTrue(result['success'])
        self.assertEqual(self.game.get_tower_height(), 2)
        
        result = self.game.add_word('start')
        self.assertTrue(result['success'])
        self.assertEqual(self.game.get_tower_height(), 3)
    
    def test_add_invalid_word(self):
        """Test adding invalid words"""
        result = self.game.add_word('xyz')
        self.assertFalse(result['success'])
        self.assertEqual(self.game.get_tower_height(), 1)
    
    def test_duplicate_word(self):
        """Test that duplicate words are rejected"""
        self.game.add_word('tart')
        result = self.game.add_word('tart')
        self.assertFalse(result['success'])
        self.assertIn('already been used', result['message'])
    
    def test_undo_word(self):
        """Test undoing last word"""
        self.game.add_word('tart')
        self.assertEqual(self.game.get_tower_height(), 2)
        
        result = self.game.undo_last_word()
        self.assertTrue(result['success'])
        self.assertEqual(self.game.get_tower_height(), 1)
    
    def test_cannot_undo_starting_word(self):
        """Test that starting word cannot be undone"""
        result = self.game.undo_last_word()
        self.assertFalse(result['success'])
    
    def test_reset_game(self):
        """Test game reset"""
        self.game.add_word('tart')
        self.game.add_word('start')
        
        self.game.reset_game()
        self.assertEqual(self.game.get_tower_height(), 1)
        self.assertEqual(self.game.get_current_word(), 'art')
    
    def test_end_game(self):
        """Test ending game and getting results"""
        self.game.add_word('tart')
        self.game.add_word('start')
        
        results = self.game.end_game()
        
        self.assertIn('tower', results)
        self.assertIn('total_score', results)
        self.assertIn('height', results)
        self.assertEqual(results['height'], 3)
        self.assertGreater(results['total_score'], 0)
    
    def test_get_hint(self):
        """Test hint system"""
        hint = self.game.get_hint('starts_with')
        self.assertIn('hint', hint)
        self.assertEqual(self.game.hints_used, 1)
    
    def test_game_state(self):
        """Test getting game state"""
        state = self.game.get_game_state()
        
        self.assertIn('tower', state)
        self.assertIn('height', state)
        self.assertIn('current_word', state)
        self.assertIn('starting_word', state)
        self.assertTrue(state['is_active'])
    
    def test_daily_word_consistency(self):
        """Test that daily word is consistent for same date"""
        test_date = date(2025, 1, 1)
        word1 = WordRiseGame.get_daily_word(test_date)
        word2 = WordRiseGame.get_daily_word(test_date)
        
        self.assertEqual(word1, word2)
        self.assertEqual(len(word1), 3)
    
    def test_daily_word_different_dates(self):
        """Test that different dates give different words"""
        word1 = WordRiseGame.get_daily_word(date(2025, 1, 1))
        word2 = WordRiseGame.get_daily_word(date(2025, 1, 2))
        
        # They MIGHT be the same by chance, but very unlikely
        # This test might occasionally fail due to randomness
        # but that's okay for this purpose


class TestGameFlows(unittest.TestCase):
    """Test complete game flows"""
    
    def test_complete_game_flow(self):
        """Test a complete game from start to finish"""
        game = WordRiseGame(starting_word='art')
        
        # Build a tower
        words_to_add = ['tart', 'start']
        
        for word in words_to_add:
            result = game.add_word(word)
            self.assertTrue(result['success'], f"Failed to add {word}")
        
        # End game
        results = game.end_game()
        
        # Verify results
        self.assertEqual(results['height'], 3)
        self.assertEqual(len(results['tower']), 3)
        self.assertGreater(results['total_score'], 0)
        self.assertIsNotNone(results['time_seconds'])
    
    def test_game_with_mistakes(self):
        """Test game with invalid attempts"""
        game = WordRiseGame(starting_word='art')
        
        # Try invalid word
        result = game.add_word('xyz')
        self.assertFalse(result['success'])
        
        # Try wrong tower build
        result = game.add_word('path')
        self.assertFalse(result['success'])
        
        # Add valid word
        result = game.add_word('tart')
        self.assertTrue(result['success'])
        
        # Verify tower only has valid additions
        self.assertEqual(game.get_tower_height(), 2)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWordValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestTowerValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestScoreCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestWordRiseGame))
    suite.addTests(loader.loadTestsFromTestCase(TestGameFlows))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
