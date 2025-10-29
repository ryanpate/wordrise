/**
 * WordRise Enhanced - Frontend JavaScript
 * Handles authentication, game logic, tokens, and powerups
 */

// Global state
const API_URL = window.location.origin + '/api';
let authToken = localStorage.getItem('authToken');
let currentUser = null;
let currentSession = null;
let selectedDifficulty = 'hard';

// ============================================================================
// AUTHENTICATION
// ============================================================================

function showLoginForm() {
    document.getElementById('login-form').classList.remove('hidden');
    document.getElementById('register-form').classList.add('hidden');
}

function showRegisterForm() {
    document.getElementById('register-form').classList.remove('hidden');
    document.getElementById('login-form').classList.add('hidden');
}

function showAuthMessage(message, isError = false) {
    const messageEl = document.getElementById('auth-message');
    messageEl.textContent = message;
    messageEl.style.display = 'block';
    messageEl.style.backgroundColor = isError ? '#ffebee' : '#e8f5e9';
    messageEl.style.color = isError ? '#c62828' : '#2e7d32';
}

async function handleLogin() {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    
    if (!username || !password) {
        showAuthMessage('Please fill in all fields', true);
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            authToken = data.token;
            localStorage.setItem('authToken', authToken);
            currentUser = data.user;
            showLandingPage();
        } else {
            showAuthMessage(data.message, true);
        }
    } catch (error) {
        showAuthMessage('Login failed. Please try again.', true);
    }
}

async function handleRegister() {
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value;
    
    if (!username || !email || !password) {
        showAuthMessage('Please fill in all fields', true);
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            authToken = data.token;
            localStorage.setItem('authToken', authToken);
            currentUser = data.user;
            showLandingPage();
        } else {
            showAuthMessage(data.errors ? data.errors.join(', ') : data.error, true);
        }
    } catch (error) {
        showAuthMessage('Registration failed. Please try again.', true);
    }
}

function handleLogout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showAuthPage();
}

async function verifyAuth() {
    if (!authToken) {
        showAuthPage();
        return false;
    }
    
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            return true;
        } else {
            handleLogout();
            return false;
        }
    } catch (error) {
        handleLogout();
        return false;
    }
}

// ============================================================================
// PAGE NAVIGATION
// ============================================================================

function showAuthPage() {
    document.getElementById('auth-page').classList.remove('hidden');
    document.getElementById('landing-page').classList.add('hidden');
    document.getElementById('game-page').classList.add('hidden');
}

function showLandingPage() {
    document.getElementById('auth-page').classList.add('hidden');
    document.getElementById('landing-page').classList.remove('hidden');
    document.getElementById('game-page').classList.add('hidden');
    
    if (currentUser) {
        updateTokenDisplay();
    }
}

function showGamePage() {
    document.getElementById('auth-page').classList.add('hidden');
    document.getElementById('landing-page').classList.add('hidden');
    document.getElementById('game-page').classList.remove('hidden');
}

function returnToLanding() {
    showLandingPage();
}

// ============================================================================
// DIFFICULTY SELECTION
// ============================================================================

function selectDifficulty(difficulty) {
    selectedDifficulty = difficulty;
    document.querySelectorAll('.difficulty-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    event.target.closest('.difficulty-btn').classList.add('selected');
}

// ============================================================================
// TOKEN MANAGEMENT
// ============================================================================

function updateTokenDisplay() {
    if (currentUser && currentUser.tokens !== undefined) {
        document.getElementById('header-tokens').textContent = currentUser.tokens;
        document.getElementById('game-tokens').textContent = currentUser.tokens;
        
        // Update powerup availability
        updatePowerupAvailability();
    }
}

async function refreshUserData() {
    if (!authToken) return;
    
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        if (data.success) {
            currentUser = data.user;
            updateTokenDisplay();
        }
    } catch (error) {
        console.error('Failed to refresh user data:', error);
    }
}

function updatePowerupAvailability() {
    const tokens = currentUser?.tokens || 0;
    const prices = { hint: 10, remove: 25, skip: 50 };
    
    document.querySelectorAll('.powerup-card').forEach((card, index) => {
        const powerupTypes = ['hint', 'remove', 'skip'];
        const type = powerupTypes[index];
        const cost = prices[type];
        
        if (tokens < cost) {
            card.classList.add('disabled');
        } else {
            card.classList.remove('disabled');
        }
    });
}

// ============================================================================
// GAME MANAGEMENT
// ============================================================================

async function startGame() {
    if (!authToken) {
        showAuthPage();
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/game/start`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                difficulty: selectedDifficulty
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentSession = data.session_id;
            currentUser.tokens = data.user_tokens;
            
            // Initialize game display
            initializeGameDisplay(data.game_state);
            showGamePage();
            updateTokenDisplay();
        } else {
            alert(data.message || 'Failed to start game');
        }
    } catch (error) {
        alert('Failed to start game. Please try again.');
    }
}

function initializeGameDisplay(gameState) {
    document.getElementById('tower-height').textContent = gameState.height;
    document.getElementById('game-difficulty').textContent = 
        selectedDifficulty.charAt(0).toUpperCase() + selectedDifficulty.slice(1);
    document.getElementById('hints-used').textContent = gameState.hints_used;
    
    updateTowerDisplay(gameState.tower);
    updateCurrentLetters(gameState.current_word);
    document.getElementById('word-input').value = '';
    document.getElementById('message').textContent = '';
}

function updateTowerDisplay(tower) {
    const towerEl = document.getElementById('word-tower');
    towerEl.innerHTML = '';
    
    tower.slice().reverse().forEach((word, index) => {
        const wordEl = document.createElement('div');
        wordEl.className = 'tower-word';
        wordEl.textContent = word.toUpperCase();
        wordEl.style.animationDelay = `${index * 0.1}s`;
        towerEl.appendChild(wordEl);
    });
}

function updateCurrentLetters(word) {
    const lettersEl = document.getElementById('current-letters');
    lettersEl.innerHTML = '';
    
    const letters = word.split('').sort();
    letters.forEach(letter => {
        const letterEl = document.createElement('span');
        letterEl.className = 'letter-tile';
        letterEl.textContent = letter.toUpperCase();
        lettersEl.appendChild(letterEl);
    });
}

function showMessage(message, isError = false) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = isError ? 'message error' : 'message success';
    
    setTimeout(() => {
        messageEl.textContent = '';
        messageEl.className = 'message';
    }, 3000);
}

async function submitWord() {
    const wordInput = document.getElementById('word-input');
    const word = wordInput.value.trim().toLowerCase();
    
    if (!word) return;
    
    try {
        const response = await fetch(`${API_URL}/game/${currentSession}/add-word`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ word })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(data.message);
            updateGameDisplay(data.game_state);
            wordInput.value = '';
        } else {
            showMessage(data.message, true);
        }
    } catch (error) {
        showMessage('Failed to add word', true);
    }
}

function updateGameDisplay(gameState) {
    document.getElementById('tower-height').textContent = gameState.height;
    document.getElementById('hints-used').textContent = gameState.hints_used;
    updateTowerDisplay(gameState.tower);
    updateCurrentLetters(gameState.current_word);
}

// ============================================================================
// POWERUPS
// ============================================================================

async function usePowerup(type) {
    if (!currentUser || currentUser.tokens < getPowerupCost(type)) {
        showMessage('Insufficient tokens!', true);
        return;
    }
    
    const endpoints = {
        hint: 'hint',
        remove: 'remove-letter',
        skip: 'skip-word'
    };
    
    try {
        const response = await fetch(`${API_URL}/game/${currentSession}/${endpoints[type]}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(type === 'hint' ? data.hint : data.message);
            
            // Update tokens
            currentUser.tokens = data.tokens_remaining;
            updateTokenDisplay();
            
            // Update game state if provided
            if (data.game_state) {
                updateGameDisplay(data.game_state);
            }
        } else {
            showMessage(data.message, true);
        }
    } catch (error) {
        showMessage('Powerup failed', true);
    }
}

function getPowerupCost(type) {
    const costs = { hint: 10, remove: 25, skip: 50 };
    return costs[type];
}

// ============================================================================
// GAME END
// ============================================================================

function confirmEndGame() {
    if (confirm('Are you sure you want to end the game?')) {
        endGame();
    }
}

async function endGame() {
    try {
        const response = await fetch(`${API_URL}/game/${currentSession}/end`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            alert(data.message || 'Failed to end game');
        }
    } catch (error) {
        alert('Failed to end game');
    }
}

function displayResults(data) {
    const result = data.final_result;
    
    document.getElementById('final-score').textContent = result.total_score;
    document.getElementById('tokens-earned').textContent = data.tokens_earned;
    document.getElementById('final-height').textContent = result.height;
    document.getElementById('time-taken').textContent = result.time_seconds + 's';
    
    // Update user tokens
    currentUser.tokens = data.tokens_total;
    updateTokenDisplay();
    
    // Show tower
    const towerDisplay = document.getElementById('final-tower-display');
    towerDisplay.innerHTML = '<h4>Your Tower:</h4>' + 
        result.tower.map(word => `<div>${word.toUpperCase()}</div>`).join('');
    
    document.getElementById('results-modal').classList.remove('hidden');
}

function closeResults() {
    document.getElementById('results-modal').classList.add('hidden');
}

// ============================================================================
// STATISTICS
// ============================================================================

async function showStats() {
    try {
        const response = await fetch(`${API_URL}/stats/me`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.success && data.stats) {
            displayStats(data.stats);
            document.getElementById('stats-modal').classList.remove('hidden');
        }
    } catch (error) {
        alert('Failed to load statistics');
    }
}

function displayStats(stats) {
    document.getElementById('stat-total-games').textContent = stats.total_games_played;
    document.getElementById('stat-highest-score').textContent = stats.highest_score;
    document.getElementById('stat-highest-tower').textContent = stats.highest_tower;
    document.getElementById('stat-play-time').textContent = 
        Math.round(stats.total_play_time_seconds / 60) + ' min';
    document.getElementById('stat-avg-score').textContent = stats.average_score;
    
    // Top letters
    const topLetters = document.getElementById('top-letters');
    if (stats.most_used_letters && stats.most_used_letters.length > 0) {
        topLetters.innerHTML = stats.most_used_letters
            .map(([letter, count]) => `<span style="margin: 5px; padding: 8px 12px; background: #e0e0e0; border-radius: 8px;">${letter.toUpperCase()}: ${count}</span>`)
            .join('');
    } else {
        topLetters.innerHTML = '<p>No data yet</p>';
    }
    
    // Top words
    const topWords = document.getElementById('top-words');
    if (stats.most_used_words && stats.most_used_words.length > 0) {
        topWords.innerHTML = stats.most_used_words
            .map(([word, count]) => `<div style="margin: 5px 0;">${word}: ${count} times</div>`)
            .join('');
    } else {
        topWords.innerHTML = '<p>No data yet</p>';
    }
}

function closeStats() {
    document.getElementById('stats-modal').classList.add('hidden');
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    // Setup enter key handlers
    document.getElementById('login-password').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleLogin();
    });
    
    document.getElementById('register-password').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleRegister();
    });
    
    document.getElementById('word-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') submitWord();
    });
    
    // Check authentication
    const isAuthenticated = await verifyAuth();
    if (isAuthenticated) {
        showLandingPage();
    } else {
        showAuthPage();
    }
});
