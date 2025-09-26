#!/usr/bin/env python3
"""
Graphical Game Launcher - A Pygame-based menu system for the Hackathon Game Collection
"""

import pygame
import sys
import os

# Add the games directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'games'))

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (100, 150, 255)
DARK_BLUE = (50, 100, 200)

class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_BLUE, hover_color=DARK_BLUE, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        # Draw button background
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

class GameLauncher:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hackathon Game Collection - Launcher")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Create buttons
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = 200
        
        self.snake_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
            "🐍 Snake Game"
        )
        
        self.space_shooter_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + button_spacing,
            button_width,
            button_height,
            "🚀 Space Shooter"
        )
        
        self.breakout_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + button_spacing * 2,
            button_width,
            button_height,
            "🧱 Breakout"
        )
        
        self.quit_button = Button(
            WINDOW_WIDTH // 2 - button_width // 2,
            start_y + button_spacing * 3,
            button_width,
            button_height,
            "❌ Quit",
            color=RED,
            hover_color=(200, 0, 0)
        )
        
        self.buttons = [
            self.snake_button,
            self.space_shooter_button,
            self.breakout_button,
            self.quit_button
        ]
        
        # Animation variables
        self.star_positions = []
        self.generate_stars()
        
    def generate_stars(self):
        """Generate random star positions for background animation"""
        for _ in range(100):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.star_positions.append((x, y))
    
    def draw_background(self):
        """Draw animated starfield background"""
        self.screen.fill(BLACK)
        
        # Draw stars
        for i, (x, y) in enumerate(self.star_positions):
            # Animate stars moving down
            new_y = (y + 1) % WINDOW_HEIGHT
            self.star_positions[i] = (x, new_y)
            
            # Draw star
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(self.screen, color, (x, new_y), 1)
    
    def draw_title(self):
        """Draw the main title"""
        title_text = self.font.render("🎮 Hackathon Game Collection", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.small_font.render("Choose a game to play!", True, GRAY)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_instructions(self):
        """Draw instructions at the bottom"""
        instructions = [
            "Use mouse to select a game",
            "Press ESC to quit at any time"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, GRAY)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60 + i * 25))
            self.screen.blit(text, text_rect)
    
    def launch_game(self, game_name):
        """Launch the selected game"""
        try:
            if game_name == "snake":
                from games.snake import SnakeGame
                game = SnakeGame()
            elif game_name == "space_shooter":
                from games.space_shooter import SpaceShooter
                game = SpaceShooter()
            elif game_name == "breakout":
                from games.breakout import BreakoutGame
                game = BreakoutGame()
            else:
                return False
            
            # Hide the launcher window
            pygame.display.iconify()
            
            # Run the game
            game.run()
            
            # Show the launcher window again
            pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Hackathon Game Collection - Launcher")
            
            return True
            
        except ImportError as e:
            print(f"❌ Error importing {game_name}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error running {game_name}: {e}")
            return False
    
    def handle_events(self):
        """Handle all events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_1:
                    self.launch_game("snake")
                elif event.key == pygame.K_2:
                    self.launch_game("space_shooter")
                elif event.key == pygame.K_3:
                    self.launch_game("breakout")
            
            # Handle button events
            for button in self.buttons:
                if button.handle_event(event):
                    if button == self.snake_button:
                        self.launch_game("snake")
                    elif button == self.space_shooter_button:
                        self.launch_game("space_shooter")
                    elif button == self.breakout_button:
                        self.launch_game("breakout")
                    elif button == self.quit_button:
                        return False
        
        return True
    
    def draw(self):
        """Draw everything"""
        self.draw_background()
        self.draw_title()
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        self.draw_instructions()
        
        # Draw keyboard shortcuts
        shortcuts_text = self.small_font.render("Keyboard shortcuts: 1, 2, 3, ESC", True, GRAY)
        shortcuts_rect = shortcuts_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        self.screen.blit(shortcuts_text, shortcuts_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main launcher loop"""
        print("🎮 Starting Game Launcher...")
        print("=" * 50)
        print("Available games:")
        print("1. Snake Game 🐍")
        print("2. Space Shooter 🚀")
        print("3. Breakout 🧱")
        print("=" * 50)
        print("Use mouse or keyboard shortcuts (1, 2, 3) to select games")
        print()
        
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    import random
    launcher = GameLauncher()
    launcher.run()
