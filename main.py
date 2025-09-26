#!/usr/bin/env python3
"""
Hackathon Game - Main Entry Point
"""

import pygame
import sys

def main():
    """Main game function"""
    print("🎮 Welcome to our Hackathon Game Collection!")
    print("=" * 50)
    print("Available games:")
    print("1. Snake Game 🐍")
    print("2. Space Shooter 🚀")
    print("3. Breakout 🧱")
    print("=" * 50)
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        print("🐍 Starting Snake Game...")
        from games.snake import SnakeGame
        game = SnakeGame()
    elif choice == "2":
        print("🚀 Starting Space Shooter...")
        from games.space_shooter import SpaceShooter
        game = SpaceShooter()
    elif choice == "3":
        print("🧱 Starting Breakout...")
        from games.breakout import BreakoutGame
        game = BreakoutGame()
    else:
        print("Invalid choice! Starting Snake Game...")
        from games.snake import SnakeGame
        game = SnakeGame()
    
    game.run()

if __name__ == "__main__":
    main()
