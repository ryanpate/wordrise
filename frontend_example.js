// WordRise Frontend - Random Mode
// Updated to work with random starting words

// Game state
let startingWord = '';
let tower = [];
let gameActive = false;

// Start a new random game
async function startNewGame() {
    try {
        // Show loading
        showLoading(true);
        
        // Call API to get random starting word
        const response = await fetch('/api/game/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Initialize game with random word
            startingWord = data.starting_word;
            tower = [startingWord];
            gameActive = true;
            
            // Update UI
            updateTowerDisplay();
            showMessage(`New game started with: ${startingWord.toUpperCase()}`, 'success');
            
            // Show game screen, hide menu
            document.getElementById('menuScreen').style.display = 'none';
            document.getElementById('gameScreen').style.display = 'block';
        } else {
            showMessage('Failed to start game', 'error');
        }
        
    } catch (error) {
        console.error('Error starting game:', error);
        showMessage('Network error - please try again', 'error');
    } finally {
        showLoading(false);
    }
}

// Add word to tower
async function addWord(word) {
    if (!gameActive) {
        showMessage('Please start a new game first', 'warning');
        return;
    }
    
    if (!word || word.trim() === '') {
        showMessage('Please enter a word', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch('/api/game/add-word', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                word: word.toLowerCase(),
                tower: tower
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Update tower
            tower = data.game_state.tower;
            updateTowerDisplay();
            showMessage(data.message, 'success');
            
            // Clear input
            document.getElementById('wordInput').value = '';
        } else {
            showMessage(data.message, 'error');
        }
        
    } catch (error) {
        console.error('Error adding word:', error);
        showMessage('Network error - please try again', 'error');
    } finally {
        showLoading(false);
    }
}

// End current game and start a new one
function endAndStartNew() {
    if (confirm('End current game and start a new random game?')) {
        startNewGame();
    }
}

// Update tower display
function updateTowerDisplay() {
    const towerElement = document.getElementById('tower');
    towerElement.innerHTML = '';
    
    // Display tower from bottom to top
    tower.forEach((word, index) => {
        const wordDiv = document.createElement('div');
        wordDiv.className = 'tower-word';
        wordDiv.textContent = word.toUpperCase();
        
        // Highlight current word (top of tower)
        if (index === tower.length - 1) {
            wordDiv.classList.add('current-word');
        }
        
        towerElement.appendChild(wordDiv);
    });
    
    // Update stats
    document.getElementById('towerHeight').textContent = tower.length;
    document.getElementById('currentWord').textContent = tower[tower.length - 1].toUpperCase();
}

// Show loading indicator
function showLoading(show) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = show ? 'block' : 'none';
    }
}

// Show message to user
function showMessage(message, type = 'info') {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // New game button
    const newGameBtn = document.getElementById('newGameBtn');
    if (newGameBtn) {
        newGameBtn.addEventListener('click', startNewGame);
    }
    
    // Submit word button
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            const input = document.getElementById('wordInput');
            addWord(input.value);
        });
    }
    
    // Enter key to submit
    const wordInput = document.getElementById('wordInput');
    if (wordInput) {
        wordInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                addWord(wordInput.value);
            }
        });
    }
    
    // New game from game screen
    const playAgainBtn = document.getElementById('playAgainBtn');
    if (playAgainBtn) {
        playAgainBtn.addEventListener('click', endAndStartNew);
    }
});

// Helper: Format time
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}
