"""
WordRise API Routes - Random Mode
Updated to give a random 3-letter word every time instead of daily challenge
"""
from flask import Blueprint, request, jsonify
from game_engine import WordRiseGame

api_bp = Blueprint('api', __name__)


@api_bp.route('/game/start', methods=['POST'])
def start_game():
    """
    Start a new game with a random 3-letter word
    Every time this is called, you get a different starting word
    """
    try:
        # Get a random starting word (different each time!)
        starting_word = WordRiseGame.get_random_starting_word()
        
        # Create new game
        game = WordRiseGame(starting_word=starting_word)
        
        return jsonify({
            'success': True,
            'starting_word': starting_word,
            'game_state': game.get_game_state()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/add-word', methods=['POST'])
def add_word():
    """Add a word to the tower"""
    data = request.json
    word = data.get('word', '').strip()
    tower = data.get('tower', [])
    
    if not word:
        return jsonify({
            'success': False,
            'message': 'Word is required'
        }), 400
    
    if not tower or len(tower) == 0:
        return jsonify({
            'success': False,
            'message': 'Tower state is required'
        }), 400
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=tower[0])
        for w in tower[1:]:
            game.add_word(w)
        
        # Try to add new word
        result = game.add_word(word)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'game_state': game.get_game_state(),
                'added_letter': result.get('added_letter')
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/hint', methods=['POST'])
def get_hint():
    """Get a hint for the next word"""
    data = request.json
    tower = data.get('tower', [])
    hint_type = data.get('hint_type', 'definition')
    
    if not tower or len(tower) == 0:
        return jsonify({
            'success': False,
            'message': 'Tower state is required'
        }), 400
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=tower[0])
        for word in tower[1:]:
            game.add_word(word)
        
        # Get hint
        hint_result = game.get_hint(hint_type)
        
        return jsonify(hint_result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/end', methods=['POST'])
def end_game():
    """End game and get final score"""
    data = request.json
    tower = data.get('tower', [])
    
    if not tower or len(tower) == 0:
        return jsonify({
            'success': False,
            'message': 'Tower state is required'
        }), 400
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=tower[0])
        for word in tower[1:]:
            game.add_word(word)
        
        # End game
        final_result = game.end_game()
        
        return jsonify({
            'success': True,
            **final_result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'wordrise-api',
        'mode': 'random'  # Indicates random word mode instead of daily challenge
    })
