"""
WordRise API Routes

REST API endpoints for the WordRise game
"""
from flask import Blueprint, request, jsonify
from datetime import date
from app.game_engine import WordRiseGame
from app.session_manager import session_manager


api_bp = Blueprint('api', __name__)


# ============================================================================
# GAME ENDPOINTS
# ============================================================================

@api_bp.route('/game/start', methods=['POST'])
def start_game():
    """
    Start a new game
    
    Request Body:
        {
            "mode": "daily" | "practice",
            "starting_word": "optional" (only for practice mode)
        }
    
    Response:
        {
            "session_id": "uuid",
            "starting_word": "art",
            "tower": ["art"],
            "height": 1,
            "current_word": "art"
        }
    """
    try:
        data = request.get_json() or {}
        mode = data.get('mode', 'practice')
        starting_word = data.get('starting_word')
        
        # Determine starting word
        if mode == 'daily':
            starting_word = WordRiseGame.get_daily_word()
        elif not starting_word:
            # Random 3-letter word for practice
            temp_game = WordRiseGame()
            starting_word = temp_game.validator.get_random_word(3)
        
        # Create session
        session = session_manager.create_session(starting_word)
        game_state = session.game.get_game_state()
        
        return jsonify({
            'success': True,
            'session_id': session.session_id,
            'mode': mode,
            'starting_word': starting_word,
            'tower': game_state['tower'],
            'height': game_state['height'],
            'current_word': game_state['current_word']
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/game/<session_id>/state', methods=['GET'])
def get_game_state(session_id):
    """
    Get current game state
    
    Response:
        {
            "session_id": "uuid",
            "tower": ["art", "tart"],
            "height": 2,
            "current_word": "tart",
            "starting_word": "art",
            "hints_used": 0,
            "is_active": true
        }
    """
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        game_state = session.game.get_game_state()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            **game_state
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/game/<session_id>/add-word', methods=['POST'])
def add_word(session_id):
    """
    Add a word to the tower
    
    Request Body:
        {
            "word": "tart"
        }
    
    Response:
        {
            "success": true,
            "message": "Added letter: T",
            "word": "tart",
            "added_letter": "t",
            "tower": ["art", "tart"],
            "height": 2,
            "current_word": "tart"
        }
    """
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        if session.is_ended:
            return jsonify({
                'success': False,
                'error': 'Game has ended'
            }), 400
        
        data = request.get_json()
        if not data or 'word' not in data:
            return jsonify({
                'success': False,
                'error': 'Word is required'
            }), 400
        
        word = data['word']
        result = session.game.add_word(word)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/game/<session_id>/hint', methods=['GET'])
def get_hint(session_id):
    """
    Get a hint for the next word
    
    Query Parameters:
        hint_type: "starts_with" | "contains" | "length" | "definition" (default: "starts_with")
    
    Response:
        {
            "success": true,
            "hint": "Try a word starting with 'T'",
            "possible_words_count": 15,
            "hints_used": 1
        }
    """
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        if session.is_ended:
            return jsonify({
                'success': False,
                'error': 'Game has ended'
            }), 400
        
        hint_type = request.args.get('hint_type', 'starts_with')
        result = session.game.get_hint(hint_type)
        
        if result['success']:
            result['hints_used'] = session.game.hints_used
            return jsonify(result), 200
        else:
            return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/game/<session_id>/undo', methods=['POST'])
def undo_word(session_id):
    """
    Undo the last word
    
    Response:
        {
            "success": true,
            "message": "Removed 'tart'",
            "tower_height": 1,
            "current_word": "art"
        }
    """
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        if session.is_ended:
            return jsonify({
                'success': False,
                'error': 'Game has ended'
            }), 400
        
        result = session.game.undo_last_word()
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/game/<session_id>/reset', methods=['POST'])
def reset_game(session_id):
    """
    Reset the game to starting word
    
    Response:
        {
            "success": true,
            "message": "Game reset",
            "starting_word": "art",
            "tower": ["art"],
            "height": 1
        }
    """
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session.game.reset_game()
        session.is_ended = False
        
        game_state = session.game.get_game_state()
        
        return jsonify({
            'success': True,
            'message': 'Game reset',
            'starting_word': game_state['starting_word'],
            'tower': game_state['tower'],
            'height': game_state['height']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/game/<session_id>/end', methods=['POST'])
def end_game(session_id):
    """
    End the game and get final results
    
    Response:
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
                "breakdown": [...]
            }
        }
    """
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        results = session.game.end_game()
        session.is_ended = True
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# ============================================================================
# DAILY CHALLENGE ENDPOINTS
# ============================================================================

@api_bp.route('/daily/word', methods=['GET'])
def get_daily_word():
    """
    Get today's daily challenge word
    
    Query Parameters:
        date: "YYYY-MM-DD" (optional, defaults to today)
    
    Response:
        {
            "success": true,
            "date": "2025-10-29",
            "word": "art",
            "challenge_number": 127
        }
    """
    try:
        date_str = request.args.get('date')
        
        if date_str:
            # Parse date string
            challenge_date = date.fromisoformat(date_str)
        else:
            challenge_date = date.today()
        
        daily_word = WordRiseGame.get_daily_word(challenge_date)
        
        # Calculate challenge number (days since launch)
        launch_date = date(2025, 1, 1)
        challenge_number = (challenge_date - launch_date).days + 1
        
        return jsonify({
            'success': True,
            'date': challenge_date.isoformat(),
            'word': daily_word,
            'challenge_number': challenge_number
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@api_bp.route('/validate-word', methods=['POST'])
def validate_word():
    """
    Check if a word is valid
    
    Request Body:
        {
            "word": "tart"
        }
    
    Response:
        {
            "success": true,
            "word": "tart",
            "is_valid": true
        }
    """
    try:
        data = request.get_json()
        if not data or 'word' not in data:
            return jsonify({
                'success': False,
                'error': 'Word is required'
            }), 400
        
        word = data['word']
        
        # Create a temporary game to use the validator
        temp_game = WordRiseGame()
        is_valid = temp_game.validator.is_valid_word(word)
        
        return jsonify({
            'success': True,
            'word': word,
            'is_valid': is_valid
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get server statistics
    
    Response:
        {
            "success": true,
            "active_sessions": 42,
            "total_words": 3154
        }
    """
    try:
        # Create a temporary game to get word count
        temp_game = WordRiseGame()
        word_count = len(temp_game.validator.words_set)
        
        return jsonify({
            'success': True,
            'active_sessions': session_manager.get_session_count(),
            'total_words': word_count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@api_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
