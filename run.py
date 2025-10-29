"""
WordRise Flask Application
Serves static files and API endpoints for Railway deployment
"""
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from app.api.routes import api_bp
import os

app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static')

# Enable CORS for all routes
CORS(app)

# Register API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Serve index.html at root
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve data files
@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory('data', filename)

# Health check for Railway
@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "wordrise"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
