// ============================================
// WordRise - Main Application Controller
// ============================================

// ============================================
// Page Management
// ============================================

function showLanding() {
    document.getElementById('landing-page').classList.remove('hidden');
    document.getElementById('game-page').classList.add('hidden');
    closeMenu();
}

function showGamePage() {
    document.getElementById('landing-page').classList.add('hidden');
    document.getElementById('game-page').classList.remove('hidden');
}

// ============================================
// Game Initialization
// ============================================

async function startGame(mode) {
    if (mode === 'daily' || mode === 'random') {
        try {
            showLoading();
            
            // For random mode, get a random starting word
            // For daily mode, get the daily word
            const response = await api.startGame(mode);
            hideLoading();
            
            if (response.success) {
                await initializeGame(mode, response.starting_word || response.word);
            }
        } catch (error) {
            hideLoading();
            showMessage('Failed to start game', 'error');
            console.error('Start game error:', error);
        }
    }
}

function showPracticeModal() {
    const modal = document.getElementById('practice-modal');
    modal.classList.add('active');
    document.getElementById('starting-word-input').focus();
}

function closePracticeModal() {
    const modal = document.getElementById('practice-modal');
    modal.classList.remove('active');
    document.getElementById('starting-word-input').value = '';
}

function setStartWord(word) {
    document.getElementById('starting-word-input').value = word;
}

async function startPracticeGame() {
    const input = document.getElementById('starting-word-input');
    const word = input.value.toLowerCase().trim();

    if (!word || word.length !== 3) {
        showMessage('Please enter a 3-letter word', 'error');
        return;
    }

    closePracticeModal();
    await initializeGame('practice', word);
}

async function initializeGame(mode, startingWord) {
    const success = await game.init(mode, startingWord);

    if (success) {
        showGamePage();
        updateUI();
        updateModeBadge();
        document.getElementById('word-input').focus();
    }
}

// ============================================
// UI Updates
// ============================================

function updateUI() {
    updateTower();
    updateCurrentLetters();
    updateStats(game.height, game.calculateCurrentScore(), game.hintsUsed);
}

function updateTower() {
    const towerElement = document.getElementById('word-tower');
    towerElement.innerHTML = '';

    game.tower.forEach((word, index) => {
        const level = index + 1;
        const wordElement = document.createElement('div');
        wordElement.className = 'tower-word';
        
        const levelBadge = document.createElement('span');
        levelBadge.className = 'tower-word-level';
        levelBadge.textContent = level;
        
        const wordText = document.createElement('span');
        wordText.textContent = word.toUpperCase();
        
        wordElement.appendChild(levelBadge);
        wordElement.appendChild(wordText);
        
        // Show added letter for non-starting words
        if (index > 0) {
            const prevWord = game.tower[index - 1];
            const addedLetter = findAddedLetter(prevWord, word);
            if (addedLetter) {
                const letterBadge = document.createElement('span');
                letterBadge.className = 'tower-word-added';
                letterBadge.textContent = `+${addedLetter.toUpperCase()}`;
                wordElement.appendChild(letterBadge);
            }
        }
        
        towerElement.appendChild(wordElement);
    });
}

function updateCurrentLetters() {
    const lettersElement = document.getElementById('current-letters');
    lettersElement.innerHTML = '';

    const letters = game.getCurrentLetters();
    letters.forEach(letter => {
        const letterTile = document.createElement('div');
        letterTile.className = 'letter-tile';
        letterTile.textContent = letter.toUpperCase();
        lettersElement.appendChild(letterTile);
    });
}

function updateStats(height, score, hints) {
    document.getElementById('tower-height').textContent = height;
    document.getElementById('current-score').textContent = score;
    document.getElementById('hints-used').textContent = hints;
}

function updateModeBadge() {
    document.getElementById('mode-badge').textContent = game.getModeDisplay();
}

// ============================================
// Game Actions
// ============================================

async function submitWord() {
    const input = document.getElementById('word-input');
    const word = input.value.trim();

    if (!word) return;

    const success = await game.addWord(word);

    if (success) {
        input.value = '';
        updateUI();
    }

    input.focus();
}

async function getHint() {
    await game.getHint();
}

async function undoLastWord() {
    const success = await game.undo();
    if (success) {
        updateUI();
    }
}

async function resetGame() {
    if (confirm('Reset your tower to the starting word? This cannot be undone.')) {
        const success = await game.reset();
        if (success) {
            updateUI();
        }
    }
}

function confirmNewGame() {
    if (game.isActive) {
        if (confirm('Start a new game? Your current progress will be lost.')) {
            closeMenu();
            showLanding();
        }
    } else {
        closeMenu();
        showLanding();
    }
}

function confirmEndGame() {
    if (confirm('End the game and see your results?')) {
        endGame();
    }
}

async function endGame() {
    const results = await game.end();

    if (results) {
        showResults(results);
    }
}

// ============================================
// Results Display
// ============================================

function showResults(results) {
    const modal = document.getElementById('results-modal');
    
    // Update final score
    document.getElementById('final-score').textContent = results.total_score;
    document.getElementById('final-height').textContent = results.height;
    document.getElementById('base-score').textContent = results.base_score;
    document.getElementById('bonus-score').textContent = 
        results.letter_bonus + results.speed_bonus;
    document.getElementById('time-taken').textContent = 
        formatTime(results.time_seconds);

    // Display final tower
    const towerDisplay = document.getElementById('final-tower-display');
    towerDisplay.innerHTML = '';
    
    results.tower.forEach(word => {
        const wordElement = document.createElement('div');
        wordElement.className = 'final-tower-word';
        wordElement.textContent = word.toUpperCase();
        towerDisplay.appendChild(wordElement);
    });

    modal.classList.add('active');
}

function closeResults() {
    const modal = document.getElementById('results-modal');
    modal.classList.remove('active');
}

function shareResults() {
    const score = document.getElementById('final-score').textContent;
    const height = document.getElementById('final-height').textContent;
    const mode = game.mode === 'daily' ? 'Daily Challenge' : 'Practice Mode';
    
    const shareText = `🏗️ WordRise ${mode}\nTower Height: ${height}\nScore: ${score} points\n\nPlay at ${window.location.origin}`;

    if (navigator.share) {
        navigator.share({
            title: 'WordRise',
            text: shareText
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(shareText).then(() => {
            showMessage('Results copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    }
}

// ============================================
// Menu & Modals
// ============================================

function toggleMenu() {
    const menu = document.getElementById('side-menu');
    menu.classList.toggle('active');
}

function closeMenu() {
    const menu = document.getElementById('side-menu');
    menu.classList.remove('active');
}

function toggleRules() {
    const modal = document.getElementById('rules-modal');
    modal.classList.toggle('active');
}

// ============================================
// Messages & Loading
// ============================================

let messageTimeout;

function showMessage(text, type = 'info') {
    const messageElement = document.getElementById('message');
    messageElement.textContent = text;
    messageElement.className = `message ${type}`;

    // Clear previous timeout
    if (messageTimeout) {
        clearTimeout(messageTimeout);
    }

    // Auto-hide after duration
    messageTimeout = setTimeout(() => {
        messageElement.textContent = '';
        messageElement.className = 'message';
    }, CONFIG.GAME.MESSAGE_DURATION);
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

// ============================================
// Helper Functions
// ============================================

function findAddedLetter(oldWord, newWord) {
    const oldLetters = oldWord.split('').sort();
    const newLetters = newWord.split('').sort();
    
    for (let i = 0; i < newLetters.length; i++) {
        if (newLetters[i] !== oldLetters[i]) {
            return newLetters[i];
        }
    }
    
    return newLetters[newLetters.length - 1];
}

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
}

// ============================================
// Event Listeners
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Word input - submit on Enter
    const wordInput = document.getElementById('word-input');
    if (wordInput) {
        wordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                submitWord();
            }
        });
    }

    // Practice modal - submit on Enter
    const startingWordInput = document.getElementById('starting-word-input');
    if (startingWordInput) {
        startingWordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                startPracticeGame();
            }
        });
    }

    // Close modals on background click
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });

    // Close menu on background click
    const sideMenu = document.getElementById('side-menu');
    if (sideMenu) {
        sideMenu.addEventListener('click', (e) => {
            if (e.target === sideMenu) {
                closeMenu();
            }
        });
    }

    // Check API health on load
    if (CONFIG.DEV_MODE) {
        api.getHealth().then(health => {
            console.log('API Health:', health);
        }).catch(err => {
            console.error('API health check failed:', err);
        });
    }

    console.log('WordRise loaded successfully!');
});

// ============================================
// Global Error Handler
// ============================================

window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    if (CONFIG.DEV_MODE) {
        showMessage('An error occurred. Check console for details.', 'error');
    }
});

// ============================================
// Service Worker (future enhancement)
// ============================================

// Register service worker for PWA support
if ('serviceWorker' in navigator && !CONFIG.DEV_MODE) {
    navigator.serviceWorker.register('/sw.js').then(() => {
        console.log('Service Worker registered');
    }).catch(err => {
        console.log('Service Worker registration failed:', err);
    });
}
