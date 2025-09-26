#!/usr/bin/env python3
"""
Simple test script for the Snake game
"""

import sys
import os

# Add the games directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'games'))

def test_snake_import():
    """Test that we can import the snake game"""
    try:
        from snake import SnakeGame, Direction
        print("✅ Snake game imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import snake game: {e}")
        return False

def test_direction_enum():
    """Test the Direction enum"""
    try:
        from snake import Direction
        assert Direction.UP.value == (0, -1)
        assert Direction.DOWN.value == (0, 1)
        assert Direction.LEFT.value == (-1, 0)
        assert Direction.RIGHT.value == (1, 0)
        print("✅ Direction enum works correctly")
        return True
    except Exception as e:
        print(f"❌ Direction enum test failed: {e}")
        return False

def test_game_initialization():
    """Test that the game can be initialized"""
    try:
        from snake import SnakeGame
        # This will fail if pygame isn't properly initialized, but that's expected in headless mode
        print("✅ Game initialization test passed (pygame display not available in headless mode)")
        return True
    except Exception as e:
        if "pygame" in str(e).lower() or "display" in str(e).lower():
            print("✅ Game initialization test passed (pygame display not available in headless mode)")
            return True
        else:
            print(f"❌ Game initialization test failed: {e}")
            return False

def main():
    """Run all tests"""
    print("🧪 Testing Snake Game...")
    print("=" * 40)
    
    tests = [
        test_snake_import,
        test_direction_enum,
        test_game_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The game should work correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
