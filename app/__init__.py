"""
WordRise Flask Application
"""
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
from config import config
import os


def create_app(config_name=None):
    """
    Flask application factory
    
    Args:
        config_name: Configuration to use (development, production, testing)
    
    Returns:
        Flask app instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Define static folder path
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    
    app = Flask(__name__, static_folder=static_folder, static_url_path='')
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Root route - serve frontend
    @app.route('/')
    def index():
        return send_file(os.path.join(static_folder, 'index.html'))
    
    # Serve static files
    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)
        # If file doesn't exist, serve index.html (for SPA routing)
        return send_file(os.path.join(static_folder, 'index.html'))
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return {
            'name': 'WordRise API',
            'version': '1.0.0',
            'description': 'REST API for WordRise word tower game',
            'endpoints': {
                'game': '/api/game',
                'daily': '/api/daily',
                'health': '/api/health',
                'stats': '/api/stats'
            },
            'docs': 'https://wordrise.app/api/docs'
        }
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'service': 'wordrise-api'}
    
    return app
