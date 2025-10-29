// ============================================
// WordRise - API Configuration
// ============================================

const CONFIG = {
    // API Base URL - change this for production
    API_BASE_URL: window.location.origin + '/api',
    
    // Development mode
    DEV_MODE: window.location.hostname === 'localhost' || 
              window.location.hostname === '127.0.0.1',
    
    // Request timeout in milliseconds
    REQUEST_TIMEOUT: 10000,
    
    // Game settings
    GAME: {
        MIN_WORD_LENGTH: 3,
        MAX_WORD_LENGTH: 15,
        ANIMATION_DURATION: 300,
        MESSAGE_DURATION: 3000
    },
    
    // Hint types
    HINT_TYPES: {
        STARTS_WITH: 'starts_with',
        CONTAINS: 'contains',
        LENGTH: 'length',
        DEFINITION: 'definition'
    }
};

// Log configuration in development mode
if (CONFIG.DEV_MODE) {
    console.log('WordRise Configuration:', CONFIG);
}
