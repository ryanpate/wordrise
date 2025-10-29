"""
Session Manager for WordRise Game Sessions

Handles in-memory game sessions. In production, this can be replaced with Redis.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
import uuid
from app.game_engine import WordRiseGame


class GameSession:
    """Represents a single game session"""
    
    def __init__(self, game: WordRiseGame, session_id: str):
        self.session_id = session_id
        self.game = game
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.is_ended = False
    
    def touch(self):
        """Update last accessed time"""
        self.last_accessed = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        state = self.game.get_game_state()
        return {
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'is_ended': self.is_ended,
            'game_state': state
        }


class SessionManager:
    """
    Manages game sessions in memory
    
    In production, replace with Redis or database-backed sessions
    """
    
    def __init__(self, timeout_minutes: int = 30):
        self.sessions: Dict[str, GameSession] = {}
        self.timeout_minutes = timeout_minutes
    
    def create_session(self, starting_word: Optional[str] = None) -> GameSession:
        """
        Create a new game session
        
        Args:
            starting_word: Starting word for the game
        
        Returns:
            GameSession object
        """
        session_id = str(uuid.uuid4())
        game = WordRiseGame(starting_word=starting_word)
        session = GameSession(game, session_id)
        
        self.sessions[session_id] = session
        self._cleanup_old_sessions()
        
        return session
    
    def get_session(self, session_id: str) -> Optional[GameSession]:
        """
        Get a game session by ID
        
        Args:
            session_id: Session ID
        
        Returns:
            GameSession or None if not found
        """
        session = self.sessions.get(session_id)
        if session:
            session.touch()
        return session
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a game session
        
        Args:
            session_id: Session ID
        
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def _cleanup_old_sessions(self):
        """Remove sessions older than timeout"""
        cutoff_time = datetime.now() - timedelta(minutes=self.timeout_minutes)
        
        sessions_to_delete = [
            session_id
            for session_id, session in self.sessions.items()
            if session.last_accessed < cutoff_time
        ]
        
        for session_id in sessions_to_delete:
            del self.sessions[session_id]
    
    def get_session_count(self) -> int:
        """Get number of active sessions"""
        return len(self.sessions)


# Global session manager instance
session_manager = SessionManager()
