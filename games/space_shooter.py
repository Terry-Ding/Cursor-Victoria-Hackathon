#!/usr/bin/env python3
"""
Space Shooter Game - A classic arcade shooter built with Pygame
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
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.speed = 5
        self.health = 100
        self.max_health = 100
        
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Keep player on screen
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
        self.y = max(0, min(WINDOW_HEIGHT - self.height, self.y))
    
    def draw(self, screen):
        # Draw player ship (triangle)
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, GREEN, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
        
        # Draw health bar
        bar_width = 100
        bar_height = 10
        bar_x = self.x + (self.width - bar_width) // 2
        bar_y = self.y - 20
        
        # Background
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # Health
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))

class Bullet:
    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.speed = 8 * direction
        self.direction = direction
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen):
        color = YELLOW if self.direction > 0 else RED
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
    def is_off_screen(self):
        return self.y < 0 or self.y > WINDOW_HEIGHT

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 25
        self.speed = random.uniform(1, 3)
        self.health = 1
        self.shoot_timer = 0
        self.shoot_delay = random.randint(60, 180)  # Frames between shots
        
    def update(self):
        self.y += self.speed
        self.shoot_timer += 1
        
    def draw(self, screen):
        # Draw enemy ship (inverted triangle)
        points = [
            (self.x + self.width // 2, self.y + self.height),
            (self.x, self.y),
            (self.x + self.width, self.y)
        ]
        pygame.draw.polygon(screen, RED, points)
        pygame.draw.polygon(screen, WHITE, points, 2)
        
    def can_shoot(self):
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            return True
        return False
        
    def shoot(self):
        return Bullet(self.x + self.width // 2 - 2, self.y + self.height, -1)
        
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 30
        self.growth_rate = 2
        self.alpha = 255
        
    def update(self):
        self.radius += self.growth_rate
        self.alpha -= 10
        
    def draw(self, screen):
        if self.alpha > 0:
            color = (255, 255, 0, self.alpha)
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), int(self.radius))
            
    def is_finished(self):
        return self.alpha <= 0 or self.radius >= self.max_radius

class SpaceShooter:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space Shooter - Hackathon Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Game objects
        self.player = Player(WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT - 50)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        
        # Game state
        self.score = 0
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60  # Frames between enemy spawns
        self.game_over = False
        self.paused = False
        
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
            
        # Handle player movement
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            
        self.player.move(dx, dy)
        
        # Player shooting
        if keys[pygame.K_SPACE]:
            if len(self.bullets) < 5:  # Limit bullets
                bullet = Bullet(self.player.x + self.player.width // 2 - 2, self.player.y)
                self.bullets.append(bullet)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            enemy = Enemy(random.randint(0, WINDOW_WIDTH - 30), -30)
            self.enemies.append(enemy)
            self.enemy_spawn_timer = 0
            
            # Increase spawn rate over time
            if self.enemy_spawn_delay > 20:
                self.enemy_spawn_delay -= 1
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Enemy shooting
            if enemy.can_shoot():
                bullet = enemy.shoot()
                self.enemy_bullets.append(bullet)
            
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)
        
        # Collision detection
        self.check_collisions()
    
    def check_collisions(self):
        # Player bullets vs enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet.x < enemy.x + enemy.width and
                    bullet.x + bullet.width > enemy.x and
                    bullet.y < enemy.y + enemy.height and
                    bullet.y + bullet.height > enemy.y):
                    
                    # Hit!
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    
                    # Create explosion
                    explosion = Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                    self.explosions.append(explosion)
                    break
        
        # Enemy bullets vs player
        for bullet in self.enemy_bullets[:]:
            if (bullet.x < self.player.x + self.player.width and
                bullet.x + bullet.width > self.player.x and
                bullet.y < self.player.y + self.player.height and
                bullet.y + bullet.height > self.player.y):
                
                # Hit player!
                self.enemy_bullets.remove(bullet)
                self.player.health -= 20
                
                if self.player.health <= 0:
                    self.game_over = True
        
        # Enemies vs player
        for enemy in self.enemies[:]:
            if (enemy.x < self.player.x + self.player.width and
                enemy.x + enemy.width > self.player.x and
                enemy.y < self.player.y + self.player.height and
                enemy.y + enemy.height > self.player.y):
                
                # Collision!
                self.enemies.remove(enemy)
                self.player.health -= 30
                
                if self.player.health <= 0:
                    self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw stars background
        for i in range(50):
            x = (i * 37) % WINDOW_WIDTH
            y = (i * 23) % WINDOW_HEIGHT
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
        
        # Draw game objects
        self.player.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
            
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.big_font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, text_rect)
            
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
        controls_text = self.font.render("WASD/Arrows: Move, SPACE: Shoot/Pause", True, GRAY)
        self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
    
    def reset_game(self):
        self.player = Player(WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT - 50)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        self.score = 0
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60
        self.game_over = False
        self.paused = False
    
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
    game = SpaceShooter()
    game.run()
