"""
Database Models for WordRise Enhanced
Includes User authentication, game sessions, statistics, and token system
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model):
    """User account model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Token system
    tokens = db.Column(db.Integer, default=100)  # Starting tokens
    total_tokens_earned = db.Column(db.Integer, default=100)
    total_tokens_spent = db.Column(db.Integer, default=0)
    
    # Account info
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    game_sessions = db.relationship('GameSession', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    token_transactions = db.relationship('TokenTransaction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    stats = db.relationship('UserStats', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def add_tokens(self, amount, reason=''):
        """Add tokens to user account"""
        self.tokens += amount
        self.total_tokens_earned += amount
        
        transaction = TokenTransaction(
            user_id=self.id,
            amount=amount,
            transaction_type='earn',
            reason=reason
        )
        db.session.add(transaction)
    
    def spend_tokens(self, amount, reason=''):
        """Spend tokens (returns False if insufficient)"""
        if self.tokens < amount:
            return False
        
        self.tokens -= amount
        self.total_tokens_spent += amount
        
        transaction = TokenTransaction(
            user_id=self.id,
            amount=-amount,
            transaction_type='spend',
            reason=reason
        )
        db.session.add(transaction)
        return True
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'tokens': self.tokens,
            'total_tokens_earned': self.total_tokens_earned,
            'total_tokens_spent': self.total_tokens_spent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class GameSession(db.Model):
    """Individual game session"""
    __tablename__ = 'game_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Game details
    starting_word = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(10), default='medium')  # easy=1 letter, medium=2, hard=3
    tower = db.Column(db.Text)  # JSON array of words
    
    # Scores and stats
    final_score = db.Column(db.Integer, default=0)
    tower_height = db.Column(db.Integer, default=1)
    hints_used = db.Column(db.Integer, default=0)
    powerups_used = db.Column(db.Text)  # JSON object tracking powerup usage
    
    # Timing
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    play_time_seconds = db.Column(db.Integer)
    
    # Status
    is_completed = db.Column(db.Boolean, default=False)
    
    def set_tower(self, tower_list):
        """Store tower as JSON"""
        self.tower = json.dumps(tower_list)
    
    def get_tower(self):
        """Retrieve tower as list"""
        return json.loads(self.tower) if self.tower else []
    
    def set_powerups(self, powerups_dict):
        """Store powerups usage as JSON"""
        self.powerups_used = json.dumps(powerups_dict)
    
    def get_powerups(self):
        """Retrieve powerups as dict"""
        return json.loads(self.powerups_used) if self.powerups_used else {}
    
    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'starting_word': self.starting_word,
            'difficulty': self.difficulty,
            'tower': self.get_tower(),
            'final_score': self.final_score,
            'tower_height': self.tower_height,
            'hints_used': self.hints_used,
            'powerups_used': self.get_powerups(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'play_time_seconds': self.play_time_seconds,
            'is_completed': self.is_completed
        }


class UserStats(db.Model):
    """User statistics and achievements"""
    __tablename__ = 'user_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Game stats
    total_games_played = db.Column(db.Integer, default=0)
    total_games_completed = db.Column(db.Integer, default=0)
    total_play_time_seconds = db.Column(db.Integer, default=0)
    
    # Scores
    highest_score = db.Column(db.Integer, default=0)
    highest_tower = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)
    
    # Word/Letter usage (JSON)
    most_used_letters = db.Column(db.Text)  # JSON: {"a": 150, "b": 80, ...}
    most_used_words = db.Column(db.Text)    # JSON: {"art": 50, "tart": 45, ...}
    
    # Achievements
    longest_word_used = db.Column(db.String(50))
    fastest_game_seconds = db.Column(db.Integer)
    
    # Last updated
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def update_stats(self, game_session):
        """Update statistics after a game"""
        self.total_games_played += 1
        
        if game_session.is_completed:
            self.total_games_completed += 1
            self.total_score += game_session.final_score
            self.average_score = self.total_score / self.total_games_completed
            
            if game_session.final_score > self.highest_score:
                self.highest_score = game_session.final_score
            
            if game_session.tower_height > self.highest_tower:
                self.highest_tower = game_session.tower_height
            
            if game_session.play_time_seconds:
                self.total_play_time_seconds += game_session.play_time_seconds
                
                if not self.fastest_game_seconds or game_session.play_time_seconds < self.fastest_game_seconds:
                    self.fastest_game_seconds = game_session.play_time_seconds
        
        # Update letter/word usage
        self._update_letter_usage(game_session.get_tower())
        self._update_word_usage(game_session.get_tower())
        
        self.updated_at = datetime.utcnow()
    
    def _update_letter_usage(self, tower):
        """Track letter frequency"""
        letter_counts = json.loads(self.most_used_letters) if self.most_used_letters else {}
        
        for word in tower:
            for letter in word.lower():
                if letter.isalpha():
                    letter_counts[letter] = letter_counts.get(letter, 0) + 1
        
        self.most_used_letters = json.dumps(letter_counts)
    
    def _update_word_usage(self, tower):
        """Track word frequency"""
        word_counts = json.loads(self.most_used_words) if self.most_used_words else {}
        
        for word in tower:
            word_lower = word.lower()
            word_counts[word_lower] = word_counts.get(word_lower, 0) + 1
            
            # Track longest word
            if not self.longest_word_used or len(word) > len(self.longest_word_used):
                self.longest_word_used = word_lower
        
        self.most_used_words = json.dumps(word_counts)
    
    def get_most_used_letters(self, limit=10):
        """Get top N most used letters"""
        if not self.most_used_letters:
            return []
        
        letter_counts = json.loads(self.most_used_letters)
        sorted_letters = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_letters[:limit]
    
    def get_most_used_words(self, limit=10):
        """Get top N most used words"""
        if not self.most_used_words:
            return []
        
        word_counts = json.loads(self.most_used_words)
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:limit]
    
    def to_dict(self):
        """Convert stats to dictionary"""
        return {
            'user_id': self.user_id,
            'total_games_played': self.total_games_played,
            'total_games_completed': self.total_games_completed,
            'total_play_time_seconds': self.total_play_time_seconds,
            'highest_score': self.highest_score,
            'highest_tower': self.highest_tower,
            'total_score': self.total_score,
            'average_score': round(self.average_score, 2),
            'most_used_letters': self.get_most_used_letters(),
            'most_used_words': self.get_most_used_words(),
            'longest_word_used': self.longest_word_used,
            'fastest_game_seconds': self.fastest_game_seconds,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class TokenTransaction(db.Model):
    """Track token earnings and spending"""
    __tablename__ = 'token_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    amount = db.Column(db.Integer, nullable=False)  # Positive for earning, negative for spending
    transaction_type = db.Column(db.String(20), nullable=False)  # 'earn' or 'spend'
    reason = db.Column(db.String(200))  # What was the token for
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TokenPrice(db.Model):
    """Token pricing for powerups and purchases"""
    __tablename__ = 'token_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50), unique=True, nullable=False)  # 'hint', 'remove_letter', 'skip_word', 'token_pack'
    cost = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    
    @staticmethod
    def get_price(item_type):
        """Get price for an item"""
        item = TokenPrice.query.filter_by(item_type=item_type).first()
        return item.cost if item else 0
    
    @staticmethod
    def initialize_prices():
        """Initialize default prices"""
        default_prices = [
            {'item_type': 'hint', 'cost': 10, 'description': 'Get a hint for the next word'},
            {'item_type': 'remove_letter', 'cost': 25, 'description': 'Remove one letter from the current word'},
            {'item_type': 'skip_word', 'cost': 50, 'description': 'Choose a new word to build from'},
            {'item_type': 'token_pack_small', 'cost': 100, 'description': '100 tokens'},
            {'item_type': 'token_pack_medium', 'cost': 500, 'description': '500 tokens'},
            {'item_type': 'token_pack_large', 'cost': 1000, 'description': '1000 tokens'},
        ]
        
        for price_data in default_prices:
            existing = TokenPrice.query.filter_by(item_type=price_data['item_type']).first()
            if not existing:
                price = TokenPrice(**price_data)
                db.session.add(price)
        
        db.session.commit()
