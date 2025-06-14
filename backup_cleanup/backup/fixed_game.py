#!/usr/bin/env python3
import pygame
import random
import sys
import time
import math
import json
import os
import traceback
from typing import List, Tuple, Dict, Any, Optional

# Initialize pygame
pygame.init()

# Get the screen info to make the game fit the window
info = pygame.display.Info()
SCREEN_WIDTH = 800  # Use fixed size for stability
SCREEN_HEIGHT = 600  # Use fixed size for stability

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 224)

# Menu color palette
DEEP_BLUE = (26, 35, 126)
NEON_YELLOW = (255, 255, 0)
SLEEK_SILVER = (204, 204, 204)
BRIGHT_RED = (255, 62, 65)

# Gameplay color palette
DARK_SLATE = (47, 79, 79)
TEAL = (0, 128, 128)
MATTE_BLACK = (15, 15, 15)
METALLIC_SILVER = (192, 192, 192)
ELECTRIC_PURPLE = (191, 64, 191)
NEON_GREEN = (80, 200, 120)

# Power-up colors
BOOST_COLOR = (255, 140, 0)
SHIELD_COLOR = (30, 144, 255)
MAGNET_COLOR = (255, 215, 0)
COIN_COLOR = (255, 223, 0)
SLOW_MO_COLOR = (138, 43, 226)

# Game settings
LANE_WIDTH = SCREEN_WIDTH // 6
LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
CAR_WIDTH = 60
CAR_HEIGHT = 120
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
INITIAL_SPEED = 5
SPEED_INCREMENT = 0.005

# Day-Night cycle settings
DAY_NIGHT_CYCLE_DURATION = 60
DAY_COLOR = (47, 79, 79)
DAY_COLOR_BOTTOM = (0, 128, 128)
NIGHT_COLOR = (5, 5, 25)
NIGHT_COLOR_BOTTOM = (20, 20, 40)
SUNRISE_COLOR = (255, 127, 80)
SUNRISE_COLOR_BOTTOM = (255, 99, 71)
STAR_COUNT = 100

# Power-up settings
POWERUP_WIDTH = 40
POWERUP_HEIGHT = 40
POWERUP_DURATION = 5
BOOST_MULTIPLIER = 1.5
SHIELD_DURATION = 7
MAGNET_RANGE = 150
SLOW_MO_FACTOR = 0.5
COIN_VALUE = 10

# Game modes
GAME_MODE_ENDLESS = 0
GAME_MODE_TIME_ATTACK = 1
GAME_MODE_MISSIONS = 2

# Mission types
MISSION_COLLECT_COINS = 0
MISSION_DISTANCE = 1
MISSION_AVOID_CRASHES = 2
MISSION_USE_POWERUPS = 3

class Car:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lane = 1
        
        # Power-up states
        self.has_shield = False
        self.shield_timer = 0
        self.has_boost = False
        self.boost_timer = 0
        self.has_magnet = False
        self.magnet_timer = 0
        self.has_slow_mo = False
        self.slow_mo_timer = 0
        
        # Boost energy
        self.boost_energy = 0
        self.max_boost_energy = 100
        
        # Animation variables
        self.swerve_offset = 0
        self.swerve_direction = 0
        self.is_boosting = False
        self.boost_particles = []
        
        # Particle effects
        self.tire_smoke_cooldown = 0

    def draw(self, screen):
        # Calculate actual x position with swerve offset
        actual_x = self.x + self.swerve_offset
        
        # Car body
        pygame.draw.rect(screen, self.color, [actual_x - self.width // 2, self.y - self.height // 2, 
                                             self.width, self.height], 0, 10)
        
        # Add metallic effect with gradient
        highlight_color = (min(self.color[0] + 40, 255), min(self.color[1] + 40, 255), min(self.color[2] + 40, 255))
        pygame.draw.rect(screen, highlight_color, 
                       [actual_x - self.width // 2, self.y - self.height // 2, self.width // 2, self.height], 0, 10)
        
        # Draw shield if active
        if self.has_shield:
            shield_radius = max(self.width, self.height) * 0.7
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            
            # Pulsating effect based on remaining time
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 10
            shield_alpha = int(100 + pulse)
            
            # Draw shield with transparency
            pygame.draw.circle(shield_surface, (*SHIELD_COLOR, shield_alpha), 
                             (shield_radius, shield_radius), shield_radius)
            pygame.draw.circle(shield_surface, (*SHIELD_COLOR, shield_alpha // 2), 
                             (shield_radius, shield_radius), shield_radius - 5, 3)
            
            screen.blit(shield_surface, 
                      (actual_x - shield_radius, self.y - shield_radius))

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANE_POSITIONS[self.lane]
            # Add swerve effect
            self.swerve_offset = self.width // 2
            self.swerve_direction = -1
            # Add tire smoke effect
            self.tire_smoke_cooldown = 0.2

    def move_right(self):
        if self.lane < 5:
            self.lane += 1
            self.x = LANE_POSITIONS[self.lane]
            # Add swerve effect
            self.swerve_offset = -self.width // 2
            self.swerve_direction = 1
            # Add tire smoke effect
            self.tire_smoke_cooldown = 0.2
    
    def update(self, dt):
        # Update swerve animation
        if self.swerve_offset != 0:
            if self.swerve_direction < 0:
                self.swerve_offset = max(0, self.swerve_offset - 5)
            else:
                self.swerve_offset = min(0, self.swerve_offset + 5)
        
        # Update power-up timers
        if self.has_shield:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.has_shield = False
        
        if self.has_boost:
            self.boost_timer -= dt
            if self.boost_timer <= 0:
                self.has_boost = False
                self.is_boosting = False
        
        if self.has_magnet:
            self.magnet_timer -= dt
            if self.magnet_timer <= 0:
                self.has_magnet = False
        
        if self.has_slow_mo:
            self.slow_mo_timer -= dt
            if self.slow_mo_timer <= 0:
                self.has_slow_mo = False
                
        # Update tire smoke cooldown
        if self.tire_smoke_cooldown > 0:
            self.tire_smoke_cooldown -= dt
    
    def activate_shield(self):
        self.has_shield = True
        self.shield_timer = SHIELD_DURATION
    
    def activate_boost(self):
        self.has_boost = True
        self.boost_timer = POWERUP_DURATION
        self.is_boosting = True
    
    def activate_magnet(self):
        self.has_magnet = True
        self.magnet_timer = POWERUP_DURATION
    
    def activate_slow_mo(self):
        self.has_slow_mo = True
        self.slow_mo_timer = POWERUP_DURATION
    
    def add_boost_energy(self, amount):
        self.boost_energy = min(self.max_boost_energy, self.boost_energy + amount)
    
    def use_boost_energy(self):
        if self.boost_energy >= 30:
            self.boost_energy -= 30
            self.activate_boost()
            return True
        return False

class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.x = LANE_POSITIONS[lane]
        self.y = -OBSTACLE_HEIGHT // 2
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.color = BRIGHT_RED
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x - self.width // 2, self.y - self.height // 2, 
                                            self.width, self.height], 0, 5)
        
    def move(self, speed):
        self.y += speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2
        
    def collides_with(self, car):
        return (abs(self.x - car.x) < (self.width + car.width) // 2 and 
                abs(self.y - car.y) < (self.height + car.height) // 2)

class Game:
    def __init__(self):
        try:
            # Create a fixed size window for stability
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Car Racing Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont(None, 36)
            
            # Day-night cycle variables
            self.cycle_time = 0
            self.day_phase = 0
            self.stars = []
            self.generate_stars()
            
            self.reset_game()
        except Exception as e:
            print(f"Error initializing game: {e}")
            traceback.print_exc()
            pygame.quit()
            sys.exit(1)
        
    def generate_stars(self):
        """Generate random stars for the night sky"""
        self.stars = []
        for _ in range(STAR_COUNT):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            size = random.uniform(0.5, 2)
            brightness = random.uniform(0.5, 1.0)
            twinkle_speed = random.uniform(1.0, 3.0)
            self.stars.append({
                'x': x,
                'y': y,
                'size': size,
                'brightness': brightness,
                'twinkle_speed': twinkle_speed,
                'twinkle_offset': random.uniform(0, 2 * math.pi)
            })
    
    def interpolate_color(self, color1, color2, ratio):
        """Interpolate between two colors"""
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return (r, g, b)
        
    def reset_game(self):
        self.player_car = Car(LANE_POSITIONS[1], SCREEN_HEIGHT - 150, CAR_WIDTH, CAR_HEIGHT, RED)
        self.obstacles = []
        self.speed = INITIAL_SPEED
        self.score = 0
        self.game_over = False
        self.last_obstacle_time = time.time()
        self.last_update_time = time.time()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player_car.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player_car.move_right()
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def draw_road(self):
        # Fill background with a solid color for simplicity
        self.screen.fill(DARK_SLATE)
        
        # Draw lane markings
        for i in range(7):
            x = i * LANE_WIDTH
            pygame.draw.line(self.screen, METALLIC_SILVER, (x, 0), (x, SCREEN_HEIGHT), 3)
            
        # Draw dashed lines in the middle of lanes
        for i in range(1, 6):
            x = i * LANE_WIDTH
            for y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(self.screen, WHITE, (x, y), (x, y + 20), 2)
    
    def draw(self):
        try:
            self.draw_road()
            
            # Draw player car
            self.player_car.draw(self.screen)
            
            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
                
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            
            pygame.display.flip()
        except Exception as e:
            print(f"Error in draw method: {e}")
            traceback.print_exc()
            return False
        return True
            
    def update(self):
        if self.game_over:
            return
            
        # Calculate delta time
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Update player car
        self.player_car.update(dt)
        
        # Increase speed over time
        self.speed += SPEED_INCREMENT
        
        # Generate new obstacles
        if current_time - self.last_obstacle_time > random.uniform(1.0, 3.0):
            lane = random.randint(0, 5)
            self.obstacles.append(Obstacle(lane))
            self.last_obstacle_time = current_time
        
        # Move obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move(self.speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 1
            elif obstacle.collides_with(self.player_car):
                if self.player_car.has_shield:
                    # Shield protects from collision
                    self.obstacles.remove(obstacle)
                    self.score += 2
                else:
                    self.game_over = True
    
    def show_menu(self):
        self.screen.fill(DEEP_BLUE)
        
        title_font = pygame.font.SysFont("arial", 72, bold=True)
        menu_font = pygame.font.SysFont("arial", 48)
        
        title_text = title_font.render("CAR RACING", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        self.screen.blit(title_text, title_rect)
        
        if self.game_over:
            game_over_text = title_font.render("GAME OVER", True, BRIGHT_RED)
            score_text = menu_font.render(f"FINAL SCORE: {self.score}", True, NEON_YELLOW)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
        
        new_game_text = menu_font.render("NEW GAME", True, NEON_YELLOW)
        exit_text = menu_font.render("EXIT", True, BRIGHT_RED)
        
        new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        
        self.screen.blit(new_game_text, new_game_rect)
        self.screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if new_game_rect.collidepoint(mouse_pos):
                        self.reset_game()
                        return True
                    elif exit_rect.collidepoint(mouse_pos):
                        return False
            
            self.clock.tick(30)
        
        return False
        
    def run(self):
        try:
            running = True
            in_menu = True
            
            while running:
                if in_menu:
                    running = self.show_menu()
                    in_menu = False
                else:
                    running = self.handle_events()
                    if not self.game_over and running:
                        self.update()
                        if not self.draw():
                            running = False
                    else:
                        in_menu = True
                        
                self.clock.tick(60)
        except Exception as e:
            print(f"Error in game loop: {e}")
            traceback.print_exc()
        finally:
            pygame.quit()

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()
