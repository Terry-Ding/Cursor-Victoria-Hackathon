#!/usr/bin/env python3
"""
Quick launcher for the Snake Game
"""

import sys
import os

# Add the games directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'games'))

def main():
    print("🐍 Starting Snake Game...")
    print("=" * 40)
    print("Controls:")
    print("  Arrow Keys: Move the snake")
    print("  Space: Pause/Resume or restart after game over")
    print("  Escape: Quit the game")
    print("=" * 40)
    print()
    
    try:
        from snake import SnakeGame
        game = SnakeGame()
        game.run()
    except ImportError as e:
        print(f"❌ Error importing game: {e}")
        print("Make sure pygame is installed: pip install pygame")
        return 1
    except Exception as e:
        print(f"❌ Error running game: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
