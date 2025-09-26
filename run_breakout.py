#!/usr/bin/env python3
"""
Quick launcher for the Breakout Game
"""

import sys
import os

# Add the games directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'games'))

def main():
    print("🧱 Starting Breakout...")
    print("=" * 40)
    print("Controls:")
    print("  A/D or Left/Right: Move paddle")
    print("  Space: Pause/Resume")
    print("  Escape: Quit the game")
    print("=" * 40)
    print()
    
    try:
        from games.breakout import BreakoutGame
        game = BreakoutGame()
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
