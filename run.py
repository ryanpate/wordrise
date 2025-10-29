"""
WordRise Enhanced - Main Flask Application
Features: Authentication, Tokens, Powerups, Statistics, Difficulty Levels
"""
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import os

from app.models.models import db, TokenPrice
from app.api.routes import api_bp


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__, 
                static_folder='static',
                static_url_path='/static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:///wordrise.db'
    )
    # Fix for PostgreSQL URLs from some providers
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create tables and initialize data
    with app.app_context():
        db.create_all()
        TokenPrice.initialize_prices()
    
    # Routes
    @app.route('/')
    def index():
        return send_from_directory('.', 'index.html')
    
    @app.route('/data/<path:filename>')
    def serve_data(filename):
        return send_from_directory('data', filename)
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy",
            "service": "wordrise-enhanced"
        }), 200
    
    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
