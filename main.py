#!/usr/bin/env python3
"""
Hackathon Game - Main Entry Point
"""

import pygame
import sys

def main():
    """Main game function"""
    print("Welcome to our Hackathon Game!")
    print("Choose your game:")
    print("1. Snake Game")
    print("2. Space Shooter")
    print("3. Platformer")
    print("4. Breakout")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        from games.snake import SnakeGame
        game = SnakeGame()
    elif choice == "2":
        from games.space_shooter import SpaceShooter
        game = SpaceShooter()
    elif choice == "3":
        from games.platformer import PlatformerGame
        game = PlatformerGame()
    elif choice == "4":
        from games.breakout import BreakoutGame
        game = BreakoutGame()
    else:
        print("Invalid choice! Starting Snake Game...")
        from games.snake import SnakeGame
        game = SnakeGame()
    
    game.run()

if __name__ == "__main__":
    main()
