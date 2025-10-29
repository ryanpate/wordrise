"""
WordRise Enhanced API Routes
Authentication, game management, tokens, powerups, and statistics
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.models import db, User, GameSession, UserStats, TokenTransaction, TokenPrice
from app.auth.auth_utils import (
    login_required, optional_auth, generate_token,
    validate_registration_data, validate_login_data
)
from app.game_engine import WordRiseGame

api_bp = Blueprint('api', __name__)


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    # Validate data
    errors = validate_registration_data(username, email, password)
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    try:
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        user.last_login = datetime.utcnow()
        
        db.session.add(user)
        db.session.flush()  # Get user.id
        
        # Create user stats
        stats = UserStats(user_id=user.id)
        db.session.add(stats)
        
        db.session.commit()
        
        # Generate token
        token = generate_token(user.id)
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'token': token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Registration failed'
        }), 500


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Validate
    error = validate_login_data(username, password)
    if error:
        return jsonify({
            'success': False,
            'message': error
        }), 400
    
    # Find user (check both username and email)
    user = User.query.filter(
        (User.username == username) | (User.email == username.lower())
    ).first()
    
    if not user or not user.check_password(password):
        return jsonify({
            'success': False,
            'message': 'Invalid username or password'
        }), 401
    
    if not user.is_active:
        return jsonify({
            'success': False,
            'message': 'Account is inactive'
        }), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    })


@api_bp.route('/auth/me', methods=['GET'])
@login_required
def get_current_user_info(user):
    """Get current user information"""
    return jsonify({
        'success': True,
        'user': user.to_dict()
    })


# ============================================================================
# GAME ROUTES
# ============================================================================

@api_bp.route('/game/start', methods=['POST'])
@login_required
def start_game(user):
    """Start a new game with difficulty selection"""
    data = request.json or {}
    difficulty = data.get('difficulty', 'hard')  # easy, medium, hard
    
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({
            'success': False,
            'message': 'Invalid difficulty. Choose: easy, medium, or hard'
        }), 400
    
    try:
        # Create game engine
        game = WordRiseGame(difficulty=difficulty)
        
        # Create session record
        session = GameSession(
            user_id=user.id,
            starting_word=game.starting_word,
            difficulty=difficulty
        )
        session.set_tower(game.tower)
        session.set_powerups(game.powerups_used)
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'session_id': session.id,
            'starting_word': game.starting_word,
            'difficulty': difficulty,
            'game_state': game.get_game_state(),
            'user_tokens': user.tokens
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/<int:session_id>/add-word', methods=['POST'])
@login_required
def add_word(user, session_id):
    """Add a word to the tower"""
    session = GameSession.query.filter_by(id=session_id, user_id=user.id).first()
    
    if not session:
        return jsonify({
            'success': False,
            'message': 'Game session not found'
        }), 404
    
    if session.is_completed:
        return jsonify({
            'success': False,
            'message': 'Game already completed'
        }), 400
    
    data = request.json
    word = data.get('word', '').strip()
    
    if not word:
        return jsonify({
            'success': False,
            'message': 'Word is required'
        }), 400
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=session.starting_word, difficulty=session.difficulty)
        game.tower = session.get_tower()
        game.hints_used = session.hints_used
        game.powerups_used = session.get_powerups()
        
        # Try to add word
        result = game.add_word(word)
        
        if result['success']:
            # Update session
            session.set_tower(game.tower)
            session.tower_height = game.get_tower_height()
            db.session.commit()
            
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


@api_bp.route('/game/<int:session_id>/hint', methods=['POST'])
@login_required
def get_hint(user, session_id):
    """Get a hint (costs tokens)"""
    session = GameSession.query.filter_by(id=session_id, user_id=user.id).first()
    
    if not session:
        return jsonify({
            'success': False,
            'message': 'Game session not found'
        }), 404
    
    # Check token cost
    hint_cost = TokenPrice.get_price('hint')
    if user.tokens < hint_cost:
        return jsonify({
            'success': False,
            'message': f'Insufficient tokens. Need {hint_cost} tokens.',
            'tokens_needed': hint_cost,
            'tokens_available': user.tokens
        }), 402
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=session.starting_word, difficulty=session.difficulty)
        game.tower = session.get_tower()
        game.hints_used = session.hints_used
        
        # Get hint
        data = request.json or {}
        hint_type = data.get('hint_type', 'definition')
        hint_result = game.get_hint(hint_type)
        
        if hint_result['success']:
            # Spend tokens
            user.spend_tokens(hint_cost, f'Hint for game {session_id}')
            
            # Update session
            session.hints_used = game.hints_used
            db.session.commit()
            
            hint_result['tokens_spent'] = hint_cost
            hint_result['tokens_remaining'] = user.tokens
            
            return jsonify(hint_result)
        else:
            return jsonify(hint_result)
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/<int:session_id>/remove-letter', methods=['POST'])
@login_required
def remove_letter_powerup(user, session_id):
    """Use remove letter powerup (costs tokens)"""
    session = GameSession.query.filter_by(id=session_id, user_id=user.id).first()
    
    if not session:
        return jsonify({
            'success': False,
            'message': 'Game session not found'
        }), 404
    
    # Check token cost
    cost = TokenPrice.get_price('remove_letter')
    if user.tokens < cost:
        return jsonify({
            'success': False,
            'message': f'Insufficient tokens. Need {cost} tokens.',
            'tokens_needed': cost,
            'tokens_available': user.tokens
        }), 402
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=session.starting_word, difficulty=session.difficulty)
        game.tower = session.get_tower()
        game.powerups_used = session.get_powerups()
        
        # Use powerup
        result = game.remove_letter()
        
        if result['success']:
            # Spend tokens
            user.spend_tokens(cost, f'Remove letter powerup in game {session_id}')
            
            # Update session
            session.set_tower(game.tower)
            session.tower_height = game.get_tower_height()
            session.set_powerups(game.powerups_used)
            db.session.commit()
            
            result['tokens_spent'] = cost
            result['tokens_remaining'] = user.tokens
            result['game_state'] = game.get_game_state()
            
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/<int:session_id>/skip-word', methods=['POST'])
@login_required
def skip_word_powerup(user, session_id):
    """Use skip word powerup (costs tokens)"""
    session = GameSession.query.filter_by(id=session_id, user_id=user.id).first()
    
    if not session:
        return jsonify({
            'success': False,
            'message': 'Game session not found'
        }), 404
    
    # Check token cost
    cost = TokenPrice.get_price('skip_word')
    if user.tokens < cost:
        return jsonify({
            'success': False,
            'message': f'Insufficient tokens. Need {cost} tokens.',
            'tokens_needed': cost,
            'tokens_available': user.tokens
        }), 402
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=session.starting_word, difficulty=session.difficulty)
        game.tower = session.get_tower()
        game.powerups_used = session.get_powerups()
        
        # Use powerup
        result = game.skip_word()
        
        if result['success']:
            # Spend tokens
            user.spend_tokens(cost, f'Skip word powerup in game {session_id}')
            
            # Update session
            session.set_tower(game.tower)
            session.set_powerups(game.powerups_used)
            db.session.commit()
            
            result['tokens_spent'] = cost
            result['tokens_remaining'] = user.tokens
            result['game_state'] = game.get_game_state()
            
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/<int:session_id>/end', methods=['POST'])
@login_required
def end_game(user, session_id):
    """End game and calculate final score"""
    session = GameSession.query.filter_by(id=session_id, user_id=user.id).first()
    
    if not session:
        return jsonify({
            'success': False,
            'message': 'Game session not found'
        }), 404
    
    if session.is_completed:
        return jsonify({
            'success': False,
            'message': 'Game already completed'
        }), 400
    
    try:
        # Recreate game state
        game = WordRiseGame(starting_word=session.starting_word, difficulty=session.difficulty)
        game.tower = session.get_tower()
        game.hints_used = session.hints_used
        game.powerups_used = session.get_powerups()
        game.start_time = session.started_at
        
        # End game
        final_result = game.end_game()
        
        # Update session
        session.is_completed = True
        session.ended_at = datetime.utcnow()
        session.final_score = final_result['total_score']
        session.play_time_seconds = final_result['time_seconds']
        session.set_powerups(game.powerups_used)
        
        # Update user stats
        stats = user.stats
        if not stats:
            stats = UserStats(user_id=user.id)
            db.session.add(stats)
        
        stats.update_stats(session)
        
        # Award completion tokens (base: 10 tokens + bonus for height)
        tokens_earned = 10 + (session.tower_height * 2)
        user.add_tokens(tokens_earned, f'Completed game {session_id}')
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'final_result': final_result,
            'tokens_earned': tokens_earned,
            'tokens_total': user.tokens,
            'session_id': session.id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# USER STATS ROUTES
# ============================================================================

@api_bp.route('/stats/me', methods=['GET'])
@login_required
def get_my_stats(user):
    """Get current user's statistics"""
    stats = user.stats
    
    if not stats:
        return jsonify({
            'success': True,
            'stats': {
                'total_games_played': 0,
                'message': 'No games played yet'
            }
        })
    
    return jsonify({
        'success': True,
        'stats': stats.to_dict()
    })


@api_bp.route('/stats/history', methods=['GET'])
@login_required
def get_game_history(user):
    """Get user's game history"""
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    sessions = GameSession.query.filter_by(
        user_id=user.id,
        is_completed=True
    ).order_by(
        GameSession.ended_at.desc()
    ).limit(limit).offset(offset).all()
    
    return jsonify({
        'success': True,
        'games': [session.to_dict() for session in sessions],
        'total': GameSession.query.filter_by(user_id=user.id, is_completed=True).count()
    })


@api_bp.route('/stats/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get global leaderboard"""
    limit = request.args.get('limit', 10, type=int)
    
    # Get top scores
    top_stats = UserStats.query.order_by(
        UserStats.highest_score.desc()
    ).limit(limit).all()
    
    leaderboard = []
    for i, stats in enumerate(top_stats, 1):
        user = User.query.get(stats.user_id)
        leaderboard.append({
            'rank': i,
            'username': user.username,
            'highest_score': stats.highest_score,
            'highest_tower': stats.highest_tower,
            'total_games': stats.total_games_played
        })
    
    return jsonify({
        'success': True,
        'leaderboard': leaderboard
    })


# ============================================================================
# TOKEN ROUTES
# ============================================================================

@api_bp.route('/tokens/balance', methods=['GET'])
@login_required
def get_token_balance(user):
    """Get user's token balance"""
    return jsonify({
        'success': True,
        'tokens': user.tokens,
        'total_earned': user.total_tokens_earned,
        'total_spent': user.total_tokens_spent
    })


@api_bp.route('/tokens/history', methods=['GET'])
@login_required
def get_token_history(user):
    """Get user's token transaction history"""
    limit = request.args.get('limit', 20, type=int)
    
    transactions = TokenTransaction.query.filter_by(
        user_id=user.id
    ).order_by(
        TokenTransaction.created_at.desc()
    ).limit(limit).all()
    
    return jsonify({
        'success': True,
        'transactions': [t.to_dict() for t in transactions]
    })


@api_bp.route('/tokens/prices', methods=['GET'])
def get_token_prices():
    """Get powerup prices"""
    prices = TokenPrice.query.all()
    
    return jsonify({
        'success': True,
        'prices': {p.item_type: {'cost': p.cost, 'description': p.description} for p in prices}
    })


# ============================================================================
# UTILITY ROUTES
# ============================================================================

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'wordrise-enhanced',
        'features': ['authentication', 'tokens', 'powerups', 'statistics']
    })
