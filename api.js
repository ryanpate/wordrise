// ============================================
// WordRise - API Client
// ============================================

class WordRiseAPI {
    constructor(baseURL = CONFIG.API_BASE_URL) {
        this.baseURL = baseURL;
    }

    /**
     * Make a fetch request with error handling
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || data.message || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * GET request
     */
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    /**
     * POST request
     */
    async post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(body)
        });
    }

    // ============================================
    // Health & Info
    // ============================================

    /**
     * Get API health status
     */
    async getHealth() {
        return this.get('/health');
    }

    /**
     * Get API statistics
     */
    async getStats() {
        return this.get('/stats');
    }

    // ============================================
    // Game Endpoints
    // ============================================

    /**
     * Start a new game
     * @param {string} mode - 'daily', 'random', or 'practice'
     * @param {string} startingWord - Optional, for practice mode only
     */
    async startGame(mode, startingWord = null) {
        if (mode === 'random') {
            // For random mode, call the new random endpoint
            return this.post('/game/start', {});
        } else if (mode === 'practice' && startingWord) {
            // For practice mode with custom word
            const body = { 
                mode: 'practice',
                starting_word: startingWord.toLowerCase() 
            };
            return this.post('/game/start', body);
        } else {
            // For daily mode or other modes
            const body = { mode };
            if (mode === 'practice' && startingWord) {
                body.starting_word = startingWord.toLowerCase();
            }
            return this.post('/game/start', body);
        }
    }

    /**
     * Get current game state
     * @param {string} sessionId
     */
    async getGameState(sessionId) {
        return this.get(`/game/${sessionId}/state`);
    }

    /**
     * Add a word to the tower
     * @param {string} sessionId
     * @param {string} word
     */
    async addWord(sessionId, word) {
        return this.post(`/game/${sessionId}/add-word`, {
            word: word.toLowerCase()
        });
    }

    /**
     * Get a hint for the next word
     * @param {string} sessionId
     * @param {string} hintType - Optional hint type
     */
    async getHint(sessionId, hintType = CONFIG.HINT_TYPES.STARTS_WITH) {
        return this.get(`/game/${sessionId}/hint?hint_type=${hintType}`);
    }

    /**
     * Undo the last word
     * @param {string} sessionId
     */
    async undoWord(sessionId) {
        return this.post(`/game/${sessionId}/undo`, {});
    }

    /**
     * Reset the game
     * @param {string} sessionId
     */
    async resetGame(sessionId) {
        return this.post(`/game/${sessionId}/reset`, {});
    }

    /**
     * End the game and get results
     * @param {string} sessionId
     */
    async endGame(sessionId) {
        return this.post(`/game/${sessionId}/end`, {});
    }

    // ============================================
    // Daily Challenge
    // ============================================

    /**
     * Get the daily challenge word
     * @param {string} date - Optional date in YYYY-MM-DD format
     */
    async getDailyWord(date = null) {
        const endpoint = date ? `/daily/word?date=${date}` : '/daily/word';
        return this.get(endpoint);
    }

    // ============================================
    // Utility
    // ============================================

    /**
     * Validate a word
     * @param {string} word
     */
    async validateWord(word) {
        return this.post('/validate-word', {
            word: word.toLowerCase()
        });
    }
}

// Create a global API instance
const api = new WordRiseAPI();

// Log API initialization in development
if (CONFIG.DEV_MODE) {
    console.log('WordRise API initialized');
}
