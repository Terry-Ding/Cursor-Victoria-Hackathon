#!/usr/bin/env python3
"""
Breakout Game - A classic brick-breaking game built with Pygame
"""

import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 15
        self.speed = 8
        
    def move(self, dx):
        self.x += dx * self.speed
        # Keep paddle on screen
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height), 2)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4
        self.max_speed = 8
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off walls
        if self.x <= self.radius or self.x >= WINDOW_WIDTH - self.radius:
            self.speed_x = -self.speed_x
            self.x = max(self.radius, min(WINDOW_WIDTH - self.radius, self.x))
            
        if self.y <= self.radius:
            self.speed_y = -self.speed_y
            self.y = self.radius
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT
    
    def bounce_off_paddle(self, paddle):
        # Calculate hit position on paddle (0 = left edge, 1 = right edge)
        hit_pos = (self.x - paddle.x) / paddle.width
        
        # Adjust angle based on hit position
        angle = (hit_pos - 0.5) * 2  # -1 to 1
        
        # Calculate new speed
        speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
        self.speed_x = angle * speed
        self.speed_y = -abs(self.speed_y)  # Always bounce up
        
        # Limit speed
        if abs(self.speed_x) > self.max_speed:
            self.speed_x = self.max_speed if self.speed_x > 0 else -self.max_speed
        if abs(self.speed_y) > self.max_speed:
            self.speed_y = self.max_speed if self.speed_y > 0 else -self.max_speed

class Brick:
    def __init__(self, x, y, color, points):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 25
        self.color = color
        self.points = points
        self.destroyed = False
        
    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
    
    def check_collision(self, ball):
        if self.destroyed:
            return False
            
        # Check if ball is colliding with brick
        if (ball.x + ball.radius > self.x and
            ball.x - ball.radius < self.x + self.width and
            ball.y + ball.radius > self.y and
            ball.y - ball.radius < self.y + self.height):
            
            self.destroyed = True
            
            # Determine which side was hit and bounce accordingly
            ball_center_x = ball.x
            ball_center_y = ball.y
            brick_center_x = self.x + self.width // 2
            brick_center_y = self.y + self.height // 2
            
            # Calculate collision side
            dx = ball_center_x - brick_center_x
            dy = ball_center_y - brick_center_y
            
            if abs(dx) > abs(dy):
                # Hit left or right side
                ball.speed_x = -ball.speed_x
            else:
                # Hit top or bottom side
                ball.speed_y = -ball.speed_y
            
            return True
        return False

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 2
        self.power_type = power_type  # 'big_paddle', 'small_paddle', 'extra_ball'
        self.collected = False
        
    def update(self):
        self.y += self.speed
        
    def draw(self, screen):
        if not self.collected:
            if self.power_type == 'big_paddle':
                color = GREEN
            elif self.power_type == 'small_paddle':
                color = RED
            else:  # extra_ball
                color = BLUE
                
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT
    
    def check_collision(self, paddle):
        if self.collected:
            return False
            
        if (self.x < paddle.x + paddle.width and
            self.x + self.width > paddle.x and
            self.y < paddle.y + paddle.height and
            self.y + self.height > paddle.y):
            
            self.collected = True
            return True
        return False

class BreakoutGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Breakout - Hackathon Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Game objects
        self.paddle = Paddle(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 30)
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
        self.bricks = []
        self.power_ups = []
        
        # Game state
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.level = 1
        
        # Create initial level
        self.create_level()
    
    def create_level(self):
        self.bricks = []
        brick_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        
        for row in range(6):
            for col in range(10):
                x = 50 + col * 80
                y = 50 + row * 30
                color = brick_colors[row]
                points = (6 - row) * 10  # More points for higher rows
                brick = Brick(x, y, color, points)
                self.bricks.append(brick)
    
    def handle_events(self):
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
        return True
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.move(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.move(1)
        
        # Update ball
        self.ball.update()
        
        # Check ball-paddle collision
        if (self.ball.x + self.ball.radius > self.paddle.x and
            self.ball.x - self.ball.radius < self.paddle.x + self.paddle.width and
            self.ball.y + self.ball.radius > self.paddle.y and
            self.ball.y - self.ball.radius < self.paddle.y + self.paddle.height and
            self.ball.speed_y > 0):  # Only bounce if ball is moving down
            
            self.ball.bounce_off_paddle(self.paddle)
        
        # Check ball-brick collisions
        for brick in self.bricks:
            if brick.check_collision(self.ball):
                self.score += brick.points
                
                # Chance to drop power-up
                if random.random() < 0.1:  # 10% chance
                    power_type = random.choice(['big_paddle', 'small_paddle', 'extra_ball'])
                    power_up = PowerUp(brick.x + brick.width // 2 - 10, brick.y + brick.height, power_type)
                    self.power_ups.append(power_up)
                break
        
        # Update power-ups
        for power_up in self.power_ups[:]:
            power_up.update()
            
            if power_up.check_collision(self.paddle):
                self.apply_power_up(power_up)
                self.power_ups.remove(power_up)
            elif power_up.is_off_screen():
                self.power_ups.remove(power_up)
        
        # Check if ball is off screen
        if self.ball.is_off_screen():
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Reset ball
                self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
        
        # Check if level is complete
        if all(brick.destroyed for brick in self.bricks):
            self.level += 1
            self.create_level()
            self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
            # Increase ball speed slightly
            self.ball.speed_x *= 1.1
            self.ball.speed_y *= 1.1
    
    def apply_power_up(self, power_up):
        if power_up.power_type == 'big_paddle':
            self.paddle.width = min(150, self.paddle.width + 20)
        elif power_up.power_type == 'small_paddle':
            self.paddle.width = max(60, self.paddle.width - 20)
        elif power_up.power_type == 'extra_ball':
            self.lives += 1
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        for brick in self.bricks:
            brick.draw(self.screen)
            
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))
        
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (WINDOW_WIDTH - 150, 10))
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.big_font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(final_score_text, score_rect)
            
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
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
        controls_text = self.font.render("A/D or Left/Right: Move paddle, SPACE: Pause", True, GRAY)
        self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
    
    def reset_game(self):
        self.paddle = Paddle(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 30)
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
        self.power_ups = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.level = 1
        self.create_level()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BreakoutGame()
    game.run()
