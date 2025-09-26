#!/usr/bin/env python3
"""
Quick launcher for the Space Shooter Game
"""

import sys
import os

# Add the games directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'games'))

def main():
    print("🚀 Starting Space Shooter...")
    print("=" * 40)
    print("Controls:")
    print("  WASD or Arrow Keys: Move ship")
    print("  Space: Shoot/Pause/Resume")
    print("  Escape: Quit the game")
    print("=" * 40)
    print()
    
    try:
        from games.space_shooter import SpaceShooter
        game = SpaceShooter()
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
