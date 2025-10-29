// ============================================
// WordRise - Game Logic
// ============================================

class WordRiseGame {
    constructor() {
        this.sessionId = null;
        this.mode = null;
        this.tower = [];
        this.currentWord = '';
        this.startingWord = '';
        this.height = 0;
        this.hintsUsed = 0;
        this.isActive = false;
        this.startTime = null;
    }

    /**
     * Initialize a new game
     */
    async init(mode, startingWord = null) {
        try {
            showLoading();
            
            const response = await api.startGame(mode, startingWord);
            
            if (response.success) {
                this.sessionId = response.session_id;
                this.mode = response.mode;
                this.tower = response.tower;
                this.currentWord = response.current_word;
                this.startingWord = response.starting_word;
                this.height = response.height;
                this.hintsUsed = 0;
                this.isActive = true;
                this.startTime = Date.now();
                
                return true;
            }
            
            return false;
        } catch (error) {
            console.error('Failed to initialize game:', error);
            showMessage('Failed to start game. Please try again.', 'error');
            return false;
        } finally {
            hideLoading();
        }
    }

    /**
     * Add a word to the tower
     */
    async addWord(word) {
        if (!this.isActive || !this.sessionId) {
            showMessage('No active game session', 'error');
            return false;
        }

        if (!word || word.trim().length === 0) {
            showMessage('Please enter a word', 'error');
            return false;
        }

        const cleanWord = word.toLowerCase().trim();

        try {
            const response = await api.addWord(this.sessionId, cleanWord);

            if (response.success) {
                // Update local state
                this.tower.push(cleanWord);
                this.currentWord = cleanWord;
                this.height = response.tower_height;

                showMessage(response.message, 'success');
                return true;
            } else {
                showMessage(response.message, 'error');
                return false;
            }
        } catch (error) {
            console.error('Failed to add word:', error);
            showMessage(error.message || 'Failed to add word', 'error');
            return false;
        }
    }

    /**
     * Get a hint
     */
    async getHint(hintType = CONFIG.HINT_TYPES.STARTS_WITH) {
        if (!this.isActive || !this.sessionId) {
            showMessage('No active game session', 'error');
            return;
        }

        try {
            const response = await api.getHint(this.sessionId, hintType);

            if (response.success) {
                this.hintsUsed = response.hints_used;
                showMessage(`💡 ${response.hint}`, 'info');
                updateStats(this.height, this.calculateCurrentScore(), this.hintsUsed);
            }
        } catch (error) {
            console.error('Failed to get hint:', error);
            showMessage('Failed to get hint', 'error');
        }
    }

    /**
     * Undo the last word
     */
    async undo() {
        if (!this.isActive || !this.sessionId) {
            showMessage('No active game session', 'error');
            return false;
        }

        if (this.tower.length <= 1) {
            showMessage('Cannot undo the starting word', 'error');
            return false;
        }

        try {
            const response = await api.undoWord(this.sessionId);

            if (response.success) {
                // Update local state
                this.tower.pop();
                this.currentWord = response.current_word;
                this.height = response.tower_height;

                showMessage(response.message, 'success');
                return true;
            }

            return false;
        } catch (error) {
            console.error('Failed to undo:', error);
            showMessage('Failed to undo', 'error');
            return false;
        }
    }

    /**
     * Reset the game to starting word
     */
    async reset() {
        if (!this.isActive || !this.sessionId) {
            showMessage('No active game session', 'error');
            return false;
        }

        try {
            const response = await api.resetGame(this.sessionId);

            if (response.success) {
                // Update local state
                this.tower = response.tower;
                this.currentWord = response.starting_word;
                this.height = response.height;

                showMessage(response.message, 'success');
                return true;
            }

            return false;
        } catch (error) {
            console.error('Failed to reset:', error);
            showMessage('Failed to reset game', 'error');
            return false;
        }
    }

    /**
     * End the game and get results
     */
    async end() {
        if (!this.sessionId) {
            showMessage('No active game session', 'error');
            return null;
        }

        try {
            showLoading();
            const response = await api.endGame(this.sessionId);

            if (response.success) {
                this.isActive = false;
                return response.results;
            }

            return null;
        } catch (error) {
            console.error('Failed to end game:', error);
            showMessage('Failed to end game', 'error');
            return null;
        } finally {
            hideLoading();
        }
    }

    /**
     * Get current game state from server
     */
    async refreshState() {
        if (!this.sessionId) {
            return false;
        }

        try {
            const response = await api.getGameState(this.sessionId);

            if (response.success) {
                this.tower = response.tower;
                this.currentWord = response.current_word;
                this.height = response.height;
                this.hintsUsed = response.hints_used;
                this.isActive = response.is_active;

                return true;
            }

            return false;
        } catch (error) {
            console.error('Failed to refresh state:', error);
            return false;
        }
    }

    /**
     * Calculate current score (approximate)
     */
    calculateCurrentScore() {
        let score = 0;
        this.tower.forEach((word, index) => {
            const level = index + 1;
            const wordLength = word.length;
            score += wordLength * level;
        });
        return score;
    }

    /**
     * Get current letters
     */
    getCurrentLetters() {
        if (!this.currentWord) return [];
        return this.currentWord.split('').sort();
    }

    /**
     * Get elapsed time in seconds
     */
    getElapsedTime() {
        if (!this.startTime) return 0;
        return Math.floor((Date.now() - this.startTime) / 1000);
    }

    /**
     * Get game mode display name
     */
    getModeDisplay() {
        return this.mode === 'daily' ? '📅 Daily Challenge' : '🎮 Practice Mode';
    }
}

// Create a global game instance
const game = new WordRiseGame();

// Log game initialization in development
if (CONFIG.DEV_MODE) {
    console.log('WordRise Game initialized');
}
