#!/usr/bin/env python3
"""
Snake Game - A classic arcade game built with Pygame
"""

import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 150, 0)
GRAY = (128, 128, 128)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Hackathon Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # High score system
        self.high_score = self.load_high_score()
        
        # Game state
        self.reset_game()
        
    def reset_game(self):
        """Reset the game to initial state"""
        # Snake starts in the middle, moving right
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
        # Food
        self.food = self.generate_food()
        
        # Score
        self.score = 0
        self.game_over = False
        self.paused = False
        self.new_high_score = False
        
    def generate_food(self):
        """Generate food at a random position not occupied by snake"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def handle_events(self):
        """Handle keyboard and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.paused = not self.paused
                elif not self.game_over and not self.paused:
                    # Direction controls
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT
        return True
    
    def update(self):
        """Update game logic"""
        if self.game_over or self.paused:
            return
            
        # Update direction
        self.direction = self.next_direction
        
        # Move snake
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
            
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            # Check for new high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.new_high_score = True
                self.save_high_score()
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def get_game_speed(self):
        """Calculate game speed based on score"""
        base_speed = 10
        speed_increase = min(self.score // 50, 5)  # Increase speed every 50 points, max 5 levels
        return base_speed + speed_increase
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(BLACK)
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE
            
            if i == 0:  # Snake head
                # Draw head with eyes
                pygame.draw.rect(self.screen, GREEN, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 2)
                
                # Draw eyes based on direction
                eye_size = 3
                if self.direction == Direction.RIGHT:
                    pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE - 6, y + 5), eye_size)
                    pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE - 6, y + GRID_SIZE - 5), eye_size)
                elif self.direction == Direction.LEFT:
                    pygame.draw.circle(self.screen, BLACK, (x + 6, y + 5), eye_size)
                    pygame.draw.circle(self.screen, BLACK, (x + 6, y + GRID_SIZE - 5), eye_size)
                elif self.direction == Direction.UP:
                    pygame.draw.circle(self.screen, BLACK, (x + 5, y + 6), eye_size)
                    pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE - 5, y + 6), eye_size)
                elif self.direction == Direction.DOWN:
                    pygame.draw.circle(self.screen, BLACK, (x + 5, y + GRID_SIZE - 6), eye_size)
                    pygame.draw.circle(self.screen, BLACK, (x + GRID_SIZE - 5, y + GRID_SIZE - 6), eye_size)
            else:  # Snake body
                pygame.draw.rect(self.screen, DARK_GREEN, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 1)
        
        # Draw food
        food_x = self.food[0] * GRID_SIZE
        food_y = self.food[1] * GRID_SIZE
        pygame.draw.rect(self.screen, RED, (food_x, food_y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, WHITE, (food_x, food_y, GRID_SIZE, GRID_SIZE), 1)
        
        # Draw score and high score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (10, 50))
        
        # Show new high score indicator
        if self.new_high_score:
            new_high_text = self.font.render("NEW HIGH SCORE!", True, RED)
            self.screen.blit(new_high_text, (WINDOW_WIDTH - 200, 10))
        
        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = self.big_font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            # Instructions
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            self.screen.blit(restart_text, restart_rect)
        
        # Draw pause screen
        elif self.paused:
            pause_text = self.big_font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
            
            resume_text = self.font.render("Press SPACE to resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            self.screen.blit(resume_text, resume_rect)
        
        # Draw controls
        controls_text = self.font.render("Use arrow keys to move, SPACE to pause/restart", True, GRAY)
        self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            pass  # Silently fail if we can't save
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.get_game_speed())  # Dynamic speed based on score
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
