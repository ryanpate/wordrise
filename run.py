"""
WordRise Flask Application Runner
"""
import os
from app import create_app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Get port from environment or default to 8080
    port = int(os.environ.get('PORT', 8080))

    # Get debug mode from environment
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
    🏗️  WordRise API Server
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Environment: {os.environ.get('FLASK_ENV', 'development')}
    Port: {port}
    Debug: {debug}
    
    API Endpoints:
    - GET  /                          Root info
    - GET  /api/health                Health check
    
    Game Endpoints:
    - POST /api/game/start            Start new game
    - GET  /api/game/<id>/state       Get game state
    - POST /api/game/<id>/add-word    Add word to tower
    - GET  /api/game/<id>/hint        Get hint
    - POST /api/game/<id>/undo        Undo last word
    - POST /api/game/<id>/reset       Reset game
    - POST /api/game/<id>/end         End game
    
    Daily Challenge:
    - GET  /api/daily/word            Get daily word
    
    Utilities:
    - POST /api/validate-word         Validate a word
    - GET  /api/stats                 Server stats
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🚀 Server starting on http://localhost:{port}
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
