# Snake Game - Hackathon Edition 🐍

A classic Snake game built with Python and Pygame for the Victoria Hackathon!

## Features

- 🐍 Classic snake gameplay with smooth controls
- 🍎 Food collection and score tracking
- 🏆 High score system with persistent storage
- ⚡ Dynamic speed increase as score grows
- 👁️ Animated snake head with directional eyes
- ⏸️ Pause functionality
- 🔄 Game over and restart
- 🎮 Intuitive controls
- 🎨 Clean, modern graphics
- 🚀 "NEW HIGH SCORE!" indicator

## How to Play

1. **Movement**: Use arrow keys to control the snake
2. **Objective**: Eat the red food to grow and increase your score
3. **Avoid**: Don't hit the walls or yourself!
4. **Controls**:
   - Arrow keys: Move the snake
   - Space: Pause/Resume or restart after game over
   - Escape: Quit the game

## Installation & Setup

1. **Install Python** (3.7 or higher)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the game**:
   ```bash
   # Option 1: Quick launcher
   python3 run_snake.py
   
   # Option 2: Main launcher (with game selection)
   python3 main.py
   
   # Option 3: Direct game
   python3 games/snake.py
   ```

## Game Structure

```
├── main.py              # Main entry point with game selection
├── run_snake.py         # Quick launcher for Snake game
├── test_game.py         # Test script for game functionality
├── games/
│   ├── __init__.py
│   └── snake.py         # Snake game implementation
├── requirements.txt     # Python dependencies
├── high_score.txt       # High score storage (created automatically)
└── README.md           # This file
```

## Development

The game is built with:
- **Python 3.7+**
- **Pygame 2.5.2** for graphics and game loop
- **Object-oriented design** for clean code structure

## Future Enhancements

- 🏆 High score system
- 🎵 Sound effects and music
- 🎨 Different themes and colors
- 🚀 Power-ups and special food
- 📱 Mobile-friendly controls

## Hackathon Notes

This project demonstrates:
- Game development fundamentals
- Python programming skills
- Pygame library usage
- Object-oriented programming
- Event handling and game loops

Perfect for a hackathon because it's:
- ✅ Quick to build and test
- ✅ Fun and engaging
- ✅ Easy to extend with new features
- ✅ Great foundation for learning game development

---

**Happy Gaming!** 🎮