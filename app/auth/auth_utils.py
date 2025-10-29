"""
Authentication utilities for WordRise
JWT token generation and verification, login decorators
"""
from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta
from app.models.models import User, db


def generate_token(user_id):
    """Generate JWT token for user"""
    try:
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        return token
    except Exception as e:
        return None


def decode_token(token):
    """Decode JWT token and return user_id"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def get_current_user():
    """Get current user from JWT token in request"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    try:
        # Expected format: "Bearer <token>"
        token = auth_header.split(' ')[1]
        user_id = decode_token(token)
        
        if user_id:
            return User.query.get(user_id)
        
        return None
    except:
        return None


def login_required(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is inactive'
            }), 403
        
        # Pass user to the route function
        return f(user, *args, **kwargs)
    
    return decorated_function


def optional_auth(f):
    """Decorator for routes that work with or without authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        # Pass user (or None) to the route function
        return f(user, *args, **kwargs)
    
    return decorated_function


def validate_registration_data(username, email, password):
    """Validate registration data"""
    errors = []
    
    # Username validation
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters")
    elif len(username) > 80:
        errors.append("Username must be less than 80 characters")
    elif not username.replace('_', '').replace('-', '').isalnum():
        errors.append("Username can only contain letters, numbers, hyphens, and underscores")
    
    # Check if username exists
    if User.query.filter_by(username=username).first():
        errors.append("Username already exists")
    
    # Email validation
    if not email or '@' not in email:
        errors.append("Valid email is required")
    elif len(email) > 120:
        errors.append("Email must be less than 120 characters")
    
    # Check if email exists
    if User.query.filter_by(email=email).first():
        errors.append("Email already registered")
    
    # Password validation
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters")
    elif len(password) > 100:
        errors.append("Password must be less than 100 characters")
    
    return errors


def validate_login_data(username, password):
    """Validate login data"""
    if not username or not password:
        return "Username and password are required"
    
    return None
