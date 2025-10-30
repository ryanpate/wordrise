/**
 * WordRise Enhanced - Frontend JavaScript
 * Handles authentication, game logic, tokens, and powerups
 * Updated with enhanced hint system support
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
            
            // Update display
            document.getElementById('game-difficulty').textContent = 
                selectedDifficulty.charAt(0).toUpperCase() + selectedDifficulty.slice(1);
            
            updateGameDisplay(data.game_state);
            showGamePage();
        } else {
            alert(data.message || 'Failed to start game');
        }
    } catch (error) {
        console.error('Failed to start game:', error);
        alert('Failed to start game. Please try again.');
    }
}

function updateTowerDisplay(tower) {
    const towerEl = document.getElementById('word-tower');
    towerEl.innerHTML = '';
    
    tower.forEach((word, index) => {
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

function showMessage(message, isError = false, duration = 3000) {
    const messageEl = document.getElementById('message');
    
    // Clear any existing timeout
    if (messageEl._timeout) {
        clearTimeout(messageEl._timeout);
    }
    
    // Set message content and style
    messageEl.textContent = message || '';
    messageEl.className = isError ? 'message error' : 'message success';
    messageEl.style.display = message ? 'block' : 'none';
    
    // Auto-hide after duration
    if (message && duration > 0) {
        messageEl._timeout = setTimeout(() => {
            messageEl.textContent = '';
            messageEl.className = 'message';
            messageEl.style.display = 'none';
        }, duration);
    }
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
        console.error('Failed to add word:', error);
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
// POWERUPS - ENHANCED HINT HANDLING
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
            },
            body: JSON.stringify({
                hint_type: 'smart' // Use smart hints by default
            })
        });
        
        const data = await response.json();
        
        console.log('Powerup response:', data); // Debug logging
        
        // Handle hint responses
        if (type === 'hint') {
            if (data.success) {
                // Show hint with additional context
                let hintMessage = data.hint || 'Try thinking creatively!';
                
                // Add context if available
                if (data.possible_words_count) {
                    hintMessage += ` (${data.possible_words_count} possible words)`;
                }
                
                showMessage(hintMessage, false, 5000); // Show for 5 seconds
                
                // Update tokens
                if (data.tokens_remaining !== undefined) {
                    currentUser.tokens = data.tokens_remaining;
                    updateTokenDisplay();
                }
            } else if (data.no_words_available) {
                // Special case: No more words available (tower complete!)
                showTowerCompleteDialog(data);
            } else {
                // Regular error
                showMessage(data.message || 'Hint unavailable', true);
            }
        } else {
            // Handle other powerups
            if (data.success) {
                showMessage(data.message);
                
                // Update tokens
                if (data.tokens_remaining !== undefined) {
                    currentUser.tokens = data.tokens_remaining;
                    updateTokenDisplay();
                }
                
                // Update game state if provided
                if (data.game_state) {
                    updateGameDisplay(data.game_state);
                }
            } else {
                showMessage(data.message || 'Powerup failed', true);
            }
        }
    } catch (error) {
        console.error('Powerup error:', error);
        showMessage(`${type} failed. Please try again.`, true);
    }
}

function showTowerCompleteDialog(data) {
    const message = data.message || "🎉 Amazing! You've reached the maximum tower height!";
    const height = data.tower_height || 'final';
    const finalWord = data.final_word || '';
    
    // Create a custom modal for tower completion
    const dialog = document.createElement('div');
    dialog.className = 'modal';
    dialog.innerHTML = `
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h3>
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
                        <path d="M7 4V8C7 10.7614 9.23858 13 12 13C14.7614 13 17 10.7614 17 8V4" stroke="#5a7a99" stroke-width="2" stroke-linecap="round"/>
                        <rect x="6" y="2" width="12" height="4" rx="1" fill="#5a7a99"/>
                        <path d="M12 13V17M12 17H8M12 17H16" stroke="#5a7a99" stroke-width="2" stroke-linecap="round"/>
                        <path d="M8 17V20H16V17" stroke="#5a7a99" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Tower Complete!
                </h3>
            </div>
            <div class="modal-body">
                <div style="text-align: center; padding: 20px; background: var(--paper-cream); border-radius: 8px; margin-bottom: 20px;">
                    <p style="font-size: 18px; margin: 0; color: var(--text-primary);">${message}</p>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid var(--border-light); margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span style="color: var(--text-secondary);">Final Height:</span>
                        <span style="font-weight: 700; color: var(--accent-blue);">${height} words</span>
                    </div>
                    ${finalWord ? `
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: var(--text-secondary);">Final Word:</span>
                        <span style="font-weight: 700; color: var(--accent-blue);">${finalWord}</span>
                    </div>
                    ` : ''}
                </div>
                <p style="text-align: center; color: var(--text-secondary); font-size: 14px;">
                    You've built the tallest tower possible with these letters. Ready to see your final score?
                </p>
            </div>
            <div class="modal-footer">
                <button class="btn btn-primary" onclick="closeTowerCompleteDialog(); endGame();">View Final Score</button>
                <button class="btn btn-secondary" onclick="closeTowerCompleteDialog();">Keep Playing</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(dialog);
    window._towerCompleteDialog = dialog;
}

function closeTowerCompleteDialog() {
    if (window._towerCompleteDialog) {
        window._towerCompleteDialog.remove();
        window._towerCompleteDialog = null;
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
        console.error('Failed to end game:', error);
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
    towerDisplay.innerHTML = '<h4 style="color: var(--text-primary); margin-bottom: 15px;">Your Tower:</h4>' + 
        result.tower.map(word => `<div style="margin: 5px 0; font-weight: 600; color: var(--accent-blue);">${word.toUpperCase()}</div>`).join('');
    
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
        console.error('Failed to load statistics:', error);
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