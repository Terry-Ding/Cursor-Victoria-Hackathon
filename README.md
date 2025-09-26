# Hackathon Game Collection 🎮

A collection of classic arcade games built with Python and Pygame for the Victoria Hackathon!

## Games Included

### 🐍 Snake Game
- Classic snake gameplay with smooth controls
- Food collection and score tracking
- High score system with persistent storage
- Dynamic speed increase as score grows
- Animated snake head with directional eyes
- WASD and arrow key controls

### 🚀 Space Shooter
- Player ship with health system
- Enemy ships with AI shooting
- Explosion effects
- Increasing difficulty over time
- Starfield background
- Power-ups and special effects

### 🧱 Breakout
- Classic brick-breaking gameplay
- Realistic ball physics
- Multiple levels with increasing difficulty
- Power-ups (big paddle, small paddle, extra life)
- Lives system and score tracking
- Colorful brick patterns

## How to Play

### 🐍 Snake Game
- **Movement**: Use WASD or arrow keys to control the snake
- **Objective**: Eat the red food to grow and increase your score
- **Avoid**: Don't hit the walls or yourself!

### 🚀 Space Shooter
- **Movement**: Use WASD or arrow keys to move your ship
- **Shooting**: Hold Space to shoot at enemy ships
- **Objective**: Destroy enemies and survive as long as possible
- **Avoid**: Enemy bullets and ship collisions

### 🧱 Breakout
- **Movement**: Use A/D or left/right arrows to move the paddle
- **Objective**: Break all bricks by bouncing the ball
- **Strategy**: Use paddle angle to control ball direction
- **Power-ups**: Collect falling power-ups for special abilities

### 🎮 Common Controls
- **Space**: Shoot (Space Shooter), Pause/Resume (all games), Restart (after game over)
- **Escape**: Quit any game

## Installation & Setup

1. **Install Python** (3.7 or higher)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the games**:
   ```bash
   # Option 1: Main launcher (choose from all games)
   python3 main.py
   
   # Option 2: Quick launchers
   python3 run_snake.py        # Snake Game
   python3 run_space_shooter.py # Space Shooter
   python3 run_breakout.py     # Breakout
   
   # Option 3: Direct game files
   python3 games/snake.py
   python3 games/space_shooter.py
   python3 games/breakout.py
   ```

## Game Structure

```
├── main.py                    # Main entry point with game selection
├── run_snake.py              # Quick launcher for Snake game
├── run_space_shooter.py      # Quick launcher for Space Shooter
├── run_breakout.py           # Quick launcher for Breakout
├── test_game.py              # Test script for game functionality
├── games/
│   ├── __init__.py
│   ├── snake.py              # Snake game implementation
│   ├── space_shooter.py      # Space Shooter game implementation
│   └── breakout.py           # Breakout game implementation
├── requirements.txt          # Python dependencies
├── high_score.txt            # High score storage (created automatically)
└── README.md                # This file
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