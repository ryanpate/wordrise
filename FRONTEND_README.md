# 🏗️ WordRise - Frontend Documentation

## Overview

WordRise is a modern, responsive web-based word game where players build towers by adding one letter at a time. The frontend is built with vanilla JavaScript and modern CSS, providing a smooth and engaging user experience.

## Features

### 🎮 Game Modes
- **Daily Challenge**: Everyone gets the same starting word each day
- **Practice Mode**: Choose your own 3-letter starting word

### 🎨 User Interface
- Modern, gradient-based design
- Smooth animations and transitions
- Fully responsive (desktop, tablet, mobile)
- Dark theme optimized for extended play
- Intuitive touch-friendly controls

### 🏆 Game Features
- Visual word tower with level indicators
- Real-time score tracking
- Hint system (4 types of hints)
- Undo functionality
- Game statistics (height, score, hints used)
- Beautiful results screen with sharing capability

## Project Structure

```
wordrise_project/
├── static/
│   ├── index.html          # Main HTML file
│   ├── css/
│   │   └── style.css       # All styles and animations
│   └── js/
│       ├── config.js       # Configuration constants
│       ├── api.js          # API client wrapper
│       ├── game.js         # Game logic and state
│       └── app.js          # UI controllers and events
├── app/                    # Flask backend
├── data/                   # Word database
└── run.py                  # Application entry point
```

## Quick Start

### 1. Install Dependencies

```bash
cd wordrise_project
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python run.py
```

The application will be available at `http://localhost:5000`

### 3. Play the Game!

Open your browser and navigate to `http://localhost:5000`

## Frontend Architecture

### JavaScript Modules

#### 1. **config.js** - Configuration
- API base URL configuration
- Game settings (min/max word length, animation timings)
- Hint types enumeration
- Development mode detection

#### 2. **api.js** - API Client
- RESTful API wrapper
- Error handling
- Async request methods
- All game endpoints:
  - `startGame(mode, startingWord)`
  - `addWord(sessionId, word)`
  - `getHint(sessionId, hintType)`
  - `undoWord(sessionId)`
  - `resetGame(sessionId)`
  - `endGame(sessionId)`
  - `getDailyWord(date)`
  - `validateWord(word)`

#### 3. **game.js** - Game Logic
- Game state management
- Session handling
- Tower building logic
- Score calculation
- Time tracking
- Local state synchronization with API

#### 4. **app.js** - UI Controller
- Page transitions
- Event handlers
- UI updates (tower, stats, letters)
- Modal management
- Message system
- Loading states

### CSS Architecture

The stylesheet uses:
- **CSS Variables** for theming
- **Flexbox & Grid** for layouts
- **CSS Animations** for smooth transitions
- **Media Queries** for responsiveness
- **Utility Classes** for common patterns

Key Design Elements:
- Purple gradient background (`#667eea` to `#764ba2`)
- Card-based UI with glassmorphism effects
- Smooth hover states and animations
- Accessible focus styles
- Dark theme optimized for readability

## Game Flow

### Landing Page
1. Welcome screen with animated example tower
2. Choose between Daily Challenge or Practice Mode
3. View game rules and features

### Starting a Game
```javascript
// Daily Challenge
startGame('daily')

// Practice Mode (user chooses starting word)
showPracticeModal() → startPracticeGame()
```

### Playing
1. View current tower and available letters
2. Type a word that:
   - Uses ALL letters from previous word
   - Adds exactly ONE new letter
   - Is a valid English word
3. Submit to add to tower
4. Use hints if stuck
5. Build as high as possible

### Ending
1. Click "Finish" button
2. View final score and statistics
3. Share results
4. Play again or return home

## API Integration

### Game Initialization
```javascript
const game = new WordRiseGame();
await game.init('practice', 'cat');
```

### Adding Words
```javascript
const success = await game.addWord('tack');
if (success) {
    updateUI();
}
```

### Getting Hints
```javascript
await game.getHint('starts_with');
```

### Ending Game
```javascript
const results = await game.end();
showResults(results);
```

## Customization

### Changing Colors

Edit `css/style.css` CSS variables:

```css
:root {
    --primary: #6366f1;        /* Main accent color */
    --secondary: #10b981;       /* Success color */
    --bg-primary: #0f172a;      /* Background */
    --text-primary: #f1f5f9;    /* Text color */
}
```

### Changing API Endpoint

Edit `js/config.js`:

```javascript
const CONFIG = {
    API_BASE_URL: 'https://your-api.com/api',
    // ...
};
```

### Animation Speeds

Edit `js/config.js`:

```javascript
GAME: {
    ANIMATION_DURATION: 300,    // Milliseconds
    MESSAGE_DURATION: 3000,     // Milliseconds
}
```

## Responsive Design

### Breakpoints
- **Desktop**: > 768px
- **Tablet**: 481px - 768px
- **Mobile**: ≤ 480px

### Mobile Optimizations
- Larger touch targets (48px minimum)
- Simplified layouts
- Optimized font sizes
- Vertical stacking of elements
- Full-width buttons
- Reduced animations on low-power devices

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile Safari (iOS 14+)
- ✅ Chrome Mobile

### Required Features
- Fetch API
- ES6+ JavaScript
- CSS Grid & Flexbox
- CSS Custom Properties
- Async/Await

## Performance

### Optimizations
- Minimal dependencies (no frameworks)
- Lazy loading for images
- CSS animations (GPU-accelerated)
- Debounced input handlers
- Efficient DOM updates
- Request caching where appropriate

### Bundle Size
- HTML: ~15 KB
- CSS: ~25 KB
- JavaScript: ~20 KB
- **Total: ~60 KB** (uncompressed)

## Accessibility

### Features
- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Focus indicators
- Sufficient color contrast
- Reduced motion support
- Screen reader friendly

### Keyboard Shortcuts
- `Enter` - Submit word
- `Esc` - Close modals
- `Tab` - Navigate elements

## Future Enhancements

### Planned Features
- [ ] User accounts and authentication
- [ ] Persistent game history
- [ ] Global leaderboards
- [ ] Social sharing with images
- [ ] Sound effects
- [ ] Achievements system
- [ ] Multiplayer mode
- [ ] Progressive Web App (PWA)
- [ ] Offline mode
- [ ] Multiple languages

### Technical Improvements
- [ ] Service Worker for offline support
- [ ] IndexedDB for local storage
- [ ] WebSocket for real-time features
- [ ] Code splitting and lazy loading
- [ ] Build process (webpack/vite)
- [ ] TypeScript migration
- [ ] Unit tests (Jest)
- [ ] E2E tests (Playwright)

## Development

### Running in Development Mode

```bash
# Start Flask server with auto-reload
export FLASK_ENV=development
python run.py
```

### Making Changes

1. **Frontend changes**: Edit files in `static/`
2. **Backend changes**: Edit files in `app/`
3. **Refresh browser** to see changes
4. Check browser console for errors

### Debugging

Enable development mode in `config.js`:

```javascript
DEV_MODE: true
```

This enables:
- Console logging
- API health checks on load
- Detailed error messages

## Deployment

### Static Hosting (Frontend Only)

For API-less demo:

```bash
cd static
python -m http.server 8000
```

### Full Application

See main README for deployment options:
- Heroku
- Railway
- AWS
- Digital Ocean
- Vercel (API + Frontend)

### Build for Production

1. Minify CSS and JavaScript
2. Set production API URL in `config.js`
3. Enable CORS for production domain
4. Set up CDN for static assets
5. Configure caching headers

## Troubleshooting

### Common Issues

**Problem**: API requests fail
- Check API server is running
- Verify API_BASE_URL in config.js
- Check browser console for CORS errors

**Problem**: Words not appearing in tower
- Check game.tower array in console
- Verify updateUI() is being called
- Check for JavaScript errors

**Problem**: Styles not loading
- Clear browser cache
- Check CSS file path
- Verify Flask static folder configuration

**Problem**: Modal won't close
- Check for JavaScript errors
- Verify modal event listeners
- Try refreshing page

## Contributing

When contributing to the frontend:

1. Follow existing code style
2. Test on multiple browsers
3. Ensure mobile responsiveness
4. Update documentation
5. Add comments for complex logic
6. Test with API backend

## License

MIT License - See LICENSE file for details

## Support

- **Documentation**: README files
- **Issues**: GitHub Issues
- **Email**: support@wordrise.app
- **Discord**: [Join our community]

---

Built with ❤️ for word game enthusiasts

**WordRise** - Build your vocabulary, one letter at a time!
