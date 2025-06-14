import pygame
import random
import sys
import time
import math
import json
import os
from typing import List, Tuple, Dict, Any, Optional

# Initialize pygame
pygame.init()

# Get the screen info to make the game fit the window
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w - 100  # Leave some margin
SCREEN_HEIGHT = info.current_h - 100  # Leave some margin

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
DEEP_BLUE = (26, 35, 126)  # #1A237E - Primary background
NEON_YELLOW = (255, 255, 0)  # #FFFF00 - Buttons and highlights
SLEEK_SILVER = (204, 204, 204)  # #CCCCCC - UI elements and borders
BRIGHT_RED = (255, 62, 65)  # #FF3E41 - Call-to-action buttons

# Gameplay color palette
DARK_SLATE = (47, 79, 79)  # #2F4F4F - Top of gradient
TEAL = (0, 128, 128)  # #008080 - Bottom of gradient
MATTE_BLACK = (15, 15, 15)  # #0F0F0F - Car bodies
METALLIC_SILVER = (192, 192, 192)  # #C0C0C0 - UI overlays
ELECTRIC_PURPLE = (191, 64, 191)  # #BF40BF - Speed indicators
NEON_GREEN = (80, 200, 120)  # #50C878 - Boost effects

# Power-up colors
BOOST_COLOR = (255, 140, 0)  # Orange for speed boost
SHIELD_COLOR = (30, 144, 255)  # Dodger blue for shield
MAGNET_COLOR = (255, 215, 0)  # Gold for coin magnet
COIN_COLOR = (255, 223, 0)  # Gold for coins
SLOW_MO_COLOR = (138, 43, 226)  # Purple for slow motion

# Game settings
LANE_WIDTH = SCREEN_WIDTH // 6  # Changed from 4 to 6 lanes
LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]  # Now 6 lane positions
CAR_WIDTH = 60
CAR_HEIGHT = 120
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
INITIAL_SPEED = 5
SPEED_INCREMENT = 0.005

# Power-up settings
POWERUP_WIDTH = 40
POWERUP_HEIGHT = 40
POWERUP_DURATION = 5  # seconds
BOOST_MULTIPLIER = 1.5
SHIELD_DURATION = 7  # seconds
MAGNET_RANGE = 150  # pixels
SLOW_MO_FACTOR = 0.5  # 50% slower
COIN_VALUE = 10  # points

# Game modes
GAME_MODE_ENDLESS = 0
GAME_MODE_TIME_ATTACK = 1
GAME_MODE_MISSIONS = 2

# Mission types
MISSION_COLLECT_COINS = 0
MISSION_DISTANCE = 1
MISSION_AVOID_CRASHES = 2
MISSION_USE_POWERUPS = 3

class HighScoreManager:
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.highscores = {
            "endless": [],
            "time_attack": [],
            "missions": []
        }
        self.load_highscores()
    
    def load_highscores(self):
        """Load high scores from file if it exists"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.highscores = json.load(f)
        except Exception as e:
            print(f"Error loading high scores: {e}")
            # If there's an error, we'll use the default empty high scores
    
    def save_highscores(self):
        """Save high scores to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.highscores, f)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def add_score(self, game_mode, player_name, score, distance=0, coins=0):
        """Add a new score to the appropriate game mode list"""
        mode_key = self._get_mode_key(game_mode)
        
        # Create score entry with timestamp
        score_entry = {
            "name": player_name,
            "score": score,
            "distance": distance,
            "coins": coins,
            "date": time.strftime("%Y-%m-%d %H:%M")
        }
        
        # Add to appropriate list
        self.highscores[mode_key].append(score_entry)
        
        # Sort by score (descending)
        self.highscores[mode_key].sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10 scores
        self.highscores[mode_key] = self.highscores[mode_key][:10]
        
        # Save to file
        self.save_highscores()
    
    def get_highscores(self, game_mode):
        """Get high scores for the specified game mode"""
        mode_key = self._get_mode_key(game_mode)
        return self.highscores[mode_key]
    
    def is_high_score(self, game_mode, score):
        """Check if the score qualifies as a high score"""
        mode_key = self._get_mode_key(game_mode)
        scores = self.highscores[mode_key]
        
        # If we have fewer than 10 scores, it's automatically a high score
        if len(scores) < 10:
            return True
        
        # Otherwise, check if it's higher than the lowest score
        return score > scores[-1]["score"] if scores else True
    
    def _get_mode_key(self, game_mode):
        """Convert game mode constant to string key"""
        if game_mode == GAME_MODE_ENDLESS:
            return "endless"
        elif game_mode == GAME_MODE_TIME_ATTACK:
            return "time_attack"
        elif game_mode == GAME_MODE_MISSIONS:
            return "missions"
        else:
            return "endless"  # Default

class Particle:
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 size: float, velocity: Tuple[float, float], lifetime: float, 
                 alpha: int = 255, shrink: bool = True, gravity: float = 0):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.initial_size = size
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alpha = alpha
        self.shrink = shrink
        self.gravity = gravity
    
    def update(self, dt: float) -> None:
        # Update position
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        
        # Apply gravity
        if self.gravity > 0:
            self.velocity = (self.velocity[0], self.velocity[1] + self.gravity * dt)
        
        # Update lifetime
        self.lifetime -= dt
        
        # Update size if shrinking
        if self.shrink:
            self.size = self.initial_size * (self.lifetime / self.max_lifetime)
        
        # Update alpha (fade out)
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
    
    def draw(self, screen: pygame.Surface) -> None:
        if self.lifetime <= 0:
            return
        
        # Create a surface with per-pixel alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # Draw the particle with alpha
        pygame.draw.circle(particle_surface, (*self.color, self.alpha), 
                         (self.size, self.size), self.size)
        
        # Blit the particle surface onto the screen
        screen.blit(particle_surface, (self.x - self.size, self.y - self.size))
    
    def is_alive(self) -> bool:
        return self.lifetime > 0

class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
    
    def add_particle(self, particle: Particle) -> None:
        self.particles.append(particle)
    
    def update(self, dt: float) -> None:
        # Update all particles
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface) -> None:
        for particle in self.particles:
            particle.draw(screen)
    
    def create_spark(self, x: float, y: float, count: int = 10) -> None:
        """Create spark particles at the given position"""
        for _ in range(count):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            
            # Random color variations of yellow/orange
            color_choice = random.choice([
                (255, 255, 0),  # Yellow
                (255, 200, 0),  # Gold
                (255, 165, 0),  # Orange
                (255, 140, 0),  # Dark Orange
                (255, 255, 224)  # Light Yellow
            ])
            
            # Create the particle
            particle = Particle(
                x=x,
                y=y,
                color=color_choice,
                size=random.uniform(1, 3),
                velocity=velocity,
                lifetime=random.uniform(0.2, 0.5),
                shrink=True,
                gravity=0
            )
            self.add_particle(particle)
    
    def create_smoke(self, x: float, y: float, count: int = 5) -> None:
        """Create smoke particles at the given position"""
        for _ in range(count):
            # Upward and slightly random velocity
            velocity = (random.uniform(-10, 10), random.uniform(-30, -10))
            
            # Gray color with random variation
            gray_value = random.randint(150, 200)
            color = (gray_value, gray_value, gray_value)
            
            # Create the particle
            particle = Particle(
                x=x,
                y=y,
                color=color,
                size=random.uniform(5, 15),
                velocity=velocity,
                lifetime=random.uniform(0.5, 1.5),
                shrink=False,
                gravity=-5  # Negative gravity makes smoke rise
            )
            self.add_particle(particle)
    
    def create_crash(self, x: float, y: float) -> None:
        """Create a crash effect with multiple particle types"""
        # Create a burst of sparks
        self.create_spark(x, y, count=30)
        
        # Create smoke
        self.create_smoke(x, y, count=20)
        
        # Create debris particles
        for _ in range(15):
            # Random velocity in all directions, but stronger than sparks
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            
            # Random colors for debris
            color_choice = random.choice([
                (100, 100, 100),  # Gray
                (80, 80, 80),     # Dark Gray
                (120, 120, 120),  # Light Gray
                (50, 50, 50),     # Very Dark Gray
                (150, 150, 150)   # Very Light Gray
            ])
            
            # Create the particle with gravity
            particle = Particle(
                x=x,
                y=y,
                color=color_choice,
                size=random.uniform(3, 8),
                velocity=velocity,
                lifetime=random.uniform(0.5, 1.5),
                shrink=True,
                gravity=200  # Debris falls down
            )
            self.add_particle(particle)
    
    def create_boost_trail(self, x: float, y: float) -> None:
        """Create boost trail particles behind a car"""
        # Create several particles at slightly different positions
        for _ in range(3):
            # Random position variation
            pos_x = x + random.uniform(-10, 10)
            pos_y = y + random.uniform(-5, 5)
            
            # Downward velocity (car is moving up the screen)
            velocity = (random.uniform(-5, 5), random.uniform(10, 30))
            
            # Random color from boost colors
            color_choice = random.choice([
                BOOST_COLOR,
                (255, 69, 0),  # Red-Orange
                (255, 215, 0)  # Gold
            ])
            
            # Create the particle
            particle = Particle(
                x=pos_x,
                y=pos_y,
                color=color_choice,
                size=random.uniform(5, 10),
                velocity=velocity,
                lifetime=random.uniform(0.3, 0.8),
                shrink=True,
                gravity=0
            )
            self.add_particle(particle)
class PowerUp:
    def __init__(self, lane, type):
        self.lane = lane
        self.x = LANE_POSITIONS[lane]
        self.y = -POWERUP_HEIGHT // 2
        self.width = POWERUP_WIDTH
        self.height = POWERUP_HEIGHT
        self.type = type  # 'boost', 'shield', 'magnet', 'coin', 'slow_mo'
        
        # Set color based on type
        if self.type == 'boost':
            self.color = BOOST_COLOR
            self.symbol = "⚡"
        elif self.type == 'shield':
            self.color = SHIELD_COLOR
            self.symbol = "🛡️"
        elif self.type == 'magnet':
            self.color = MAGNET_COLOR
            self.symbol = "🧲"
        elif self.type == 'coin':
            self.color = COIN_COLOR
            self.symbol = "💰"
        elif self.type == 'slow_mo':
            self.color = SLOW_MO_COLOR
            self.symbol = "⏱️"
        
        self.pulse_effect = 0
        self.collected = False
        
    def draw(self, screen):
        # Skip drawing if collected
        if self.collected:
            return
            
        # Pulsating effect
        self.pulse_effect = (self.pulse_effect + 0.1) % (2 * math.pi)
        pulse_size = math.sin(self.pulse_effect) * 5
        
        # Draw power-up with glow effect
        for offset in range(3, 0, -1):
            glow_color = (*self.color, 100 - offset * 30)
            glow_surface = pygame.Surface((self.width + offset * 4 + pulse_size, 
                                         self.height + offset * 4 + pulse_size), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, 
                             (glow_surface.get_width() // 2, glow_surface.get_height() // 2), 
                             (self.width + offset * 4 + pulse_size) // 2)
            screen.blit(glow_surface, 
                      (self.x - glow_surface.get_width() // 2, 
                       self.y - glow_surface.get_height() // 2))
        
        # Draw main power-up
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.width // 2)
        
        # Draw symbol
        font = pygame.font.SysFont("arial", 20, bold=True)
        symbol_text = font.render(self.symbol, True, WHITE)
        symbol_rect = symbol_text.get_rect(center=(self.x, self.y))
        screen.blit(symbol_text, symbol_rect)
        
    def move(self, speed):
        self.y += speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2
        
    def collides_with(self, car):
        if self.collected:
            return False
        return (abs(self.x - car.x) < (self.width + car.width) // 2 and 
                abs(self.y - car.y) < (self.height + car.height) // 2)
                
    def collect(self):
        self.collected = True

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = COIN_COLOR
        self.collected = False
        self.pulse_effect = random.random() * 2 * math.pi
        
    def draw(self, screen):
        if self.collected:
            return
            
        # Pulsating effect
        self.pulse_effect = (self.pulse_effect + 0.1) % (2 * math.pi)
        pulse_size = math.sin(self.pulse_effect) * 2
        
        # Draw coin with glow
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.width // 2 + pulse_size)
        pygame.draw.circle(screen, (255, 255, 200), (self.x, self.y), self.width // 3)
        
    def move(self, speed):
        self.y += speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2
        
    def collides_with(self, car):
        if self.collected:
            return False
        return (abs(self.x - car.x) < (self.width + car.width) // 2 and 
                abs(self.y - car.y) < (self.height + car.height) // 2)
                
    def collect(self):
        self.collected = True

class Car:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lane = 1  # Starting lane (0-3)
        
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
        
        # Windshield
        windshield_width = int(self.width * 0.8)
        windshield_height = int(self.height * 0.3)
        windshield_x = actual_x - windshield_width // 2
        windshield_y = self.y - self.height // 2 + int(self.height * 0.15)
        pygame.draw.rect(screen, (100, 200, 255), [windshield_x, windshield_y, 
                                                 windshield_width, windshield_height], 0, 5)
        
        # Roof
        roof_width = int(self.width * 0.8)
        roof_height = int(self.height * 0.2)
        roof_x = actual_x - roof_width // 2
        roof_y = self.y - self.height // 2 + int(self.height * 0.15) + windshield_height
        pygame.draw.rect(screen, self.color, [roof_x, roof_y, 
                                            roof_width, roof_height], 0, 5)
        
        # Rear window
        rear_window_width = int(self.width * 0.7)
        rear_window_height = int(self.height * 0.2)
        rear_window_x = actual_x - rear_window_width // 2
        rear_window_y = roof_y + roof_height
        pygame.draw.rect(screen, (100, 200, 255), [rear_window_x, rear_window_y, 
                                                 rear_window_width, rear_window_height], 0, 5)
        
        # Wheels
        wheel_width = int(self.width * 0.25)
        wheel_height = int(self.height * 0.15)
        
        # Front left wheel
        pygame.draw.rect(screen, MATTE_BLACK, [actual_x - self.width // 2 - 3, 
                                       self.y - self.height // 4, 
                                       wheel_width, wheel_height], 0, 3)
        
        # Front right wheel
        pygame.draw.rect(screen, MATTE_BLACK, [actual_x + self.width // 2 - wheel_width + 3, 
                                       self.y - self.height // 4, 
                                       wheel_width, wheel_height], 0, 3)
        
        # Rear left wheel
        pygame.draw.rect(screen, MATTE_BLACK, [actual_x - self.width // 2 - 3, 
                                       self.y + self.height // 4 - wheel_height, 
                                       wheel_width, wheel_height], 0, 3)
        
        # Rear right wheel
        pygame.draw.rect(screen, MATTE_BLACK, [actual_x + self.width // 2 - wheel_width + 3, 
                                       self.y + self.height // 4 - wheel_height, 
                                       wheel_width, wheel_height], 0, 3)
        
        # Headlights with glow effect
        headlight_width = int(self.width * 0.15)
        headlight_height = int(self.height * 0.08)
        
        # Left headlight glow
        for offset in range(3, 0, -1):
            glow_color = (255, 255, 100, 100 - offset * 30)
            glow_surface = pygame.Surface((headlight_width + offset * 4, headlight_height + offset * 4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, 
                           [0, 0, headlight_width + offset * 4, headlight_height + offset * 4], 0, 5)
            screen.blit(glow_surface, 
                      (actual_x - self.width // 2 + 5 - offset * 2, self.y - self.height // 2 + 5 - offset * 2))
        
        # Left headlight
        pygame.draw.rect(screen, NEON_YELLOW, [actual_x - self.width // 2 + 5, 
                                        self.y - self.height // 2 + 5, 
                                        headlight_width, headlight_height], 0, 3)
        
        # Right headlight glow
        for offset in range(3, 0, -1):
            glow_color = (255, 255, 100, 100 - offset * 30)
            glow_surface = pygame.Surface((headlight_width + offset * 4, headlight_height + offset * 4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, 
                           [0, 0, headlight_width + offset * 4, headlight_height + offset * 4], 0, 5)
            screen.blit(glow_surface, 
                      (actual_x + self.width // 2 - headlight_width - 5 - offset * 2, self.y - self.height // 2 + 5 - offset * 2))
        
        # Right headlight
        pygame.draw.rect(screen, NEON_YELLOW, [actual_x + self.width // 2 - headlight_width - 5, 
                                        self.y - self.height // 2 + 5, 
                                        headlight_width, headlight_height], 0, 3)
        
        # Taillights
        taillight_width = int(self.width * 0.15)
        taillight_height = int(self.height * 0.08)
        
        # Left taillight
        pygame.draw.rect(screen, BRIGHT_RED, [actual_x - self.width // 2 + 5, 
                                     self.y + self.height // 2 - taillight_height - 5, 
                                     taillight_width, taillight_height], 0, 3)
        
        # Right taillight
        pygame.draw.rect(screen, BRIGHT_RED, [actual_x + self.width // 2 - taillight_width - 5, 
                                     self.y + self.height // 2 - taillight_height - 5, 
                                     taillight_width, taillight_height], 0, 3)
        
        # Draw boost particles if boosting
        if self.is_boosting:
            for i in range(5):
                particle_x = random.randint(int(actual_x - self.width // 3), int(actual_x + self.width // 3))
                particle_y = self.y + self.height // 2 + random.randint(5, 15)
                particle_size = random.randint(3, 8)
                particle_color = random.choice([BOOST_COLOR, (255, 69, 0), (255, 215, 0)])
                pygame.draw.circle(screen, particle_color, (particle_x, particle_y), particle_size)
        
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
        
        # Draw magnet effect if active
        if self.has_magnet:
            magnet_radius = MAGNET_RANGE
            magnet_surface = pygame.Surface((magnet_radius * 2, magnet_radius * 2), pygame.SRCALPHA)
            
            # Pulsating effect
            pulse = math.sin(pygame.time.get_ticks() * 0.005) * 5
            magnet_alpha = int(30 + pulse)
            
            # Draw magnet field with transparency
            pygame.draw.circle(magnet_surface, (*MAGNET_COLOR, magnet_alpha), 
                             (magnet_radius, magnet_radius), magnet_radius)
            pygame.draw.circle(magnet_surface, (*MAGNET_COLOR, magnet_alpha // 2), 
                             (magnet_radius, magnet_radius), magnet_radius - 10, 5)
            
            screen.blit(magnet_surface, 
                      (actual_x - magnet_radius, self.y - magnet_radius))
            
        # Draw boost energy meter
        self.draw_boost_meter(screen)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANE_POSITIONS[self.lane]
            # Add swerve effect
            self.swerve_offset = self.width // 2
            self.swerve_direction = -1
            # Add tire smoke effect
            self.tire_smoke_cooldown = 0.2  # Will create smoke for 0.2 seconds

    def move_right(self):
        if self.lane < 5:  # Changed from 3 to 5 for 6 lanes
            self.lane += 1
            self.x = LANE_POSITIONS[self.lane]
            # Add swerve effect
            self.swerve_offset = -self.width // 2
            self.swerve_direction = 1
            # Add tire smoke effect
            self.tire_smoke_cooldown = 0.2  # Will create smoke for 0.2 seconds
    
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
        
    def draw_boost_meter(self, screen):
        # Draw boost energy meter
        meter_width = 150
        meter_height = 15
        meter_x = 10
        meter_y = SCREEN_HEIGHT - 30
        
        # Background
        pygame.draw.rect(screen, MATTE_BLACK, (meter_x, meter_y, meter_width, meter_height), 0, 5)
        
        # Fill based on energy
        energy_width = int(meter_width * (self.boost_energy / self.max_boost_energy))
        pygame.draw.rect(screen, BOOST_COLOR, (meter_x, meter_y, energy_width, meter_height), 0, 5)
        
        # Border
        pygame.draw.rect(screen, WHITE, (meter_x, meter_y, meter_width, meter_height), 1, 5)
        
        # Label
        font = pygame.font.SysFont("arial", 16, bold=True)
        text = font.render("BOOST", True, WHITE)
        screen.blit(text, (meter_x + meter_width + 10, meter_y))
class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.x = LANE_POSITIONS[lane]
        self.y = -OBSTACLE_HEIGHT // 2
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.color = BRIGHT_RED
        self.type = random.choice(['cone', 'barrier', 'pothole'])
        
    def draw(self, screen):
        if self.type == 'cone':
            # Traffic cone with glow effect
            for offset in range(3, 0, -1):
                glow_color = (255, 100, 0, 100 - offset * 30)
                glow_surface = pygame.Surface((self.width + offset * 4, self.height + offset * 4), pygame.SRCALPHA)
                pygame.draw.polygon(glow_surface, glow_color, [
                    (self.width // 2, 0),
                    (0, self.height + offset * 4),
                    (self.width + offset * 4, self.height + offset * 4)
                ])
                screen.blit(glow_surface, 
                          (self.x - self.width // 2 - offset * 2, self.y - self.height // 2 - offset * 2))
            
            # Traffic cone
            pygame.draw.polygon(screen, (255, 140, 0), [
                (self.x, self.y - self.height // 2),
                (self.x - self.width // 2, self.y + self.height // 2),
                (self.x + self.width // 2, self.y + self.height // 2)
            ])
            pygame.draw.rect(screen, WHITE, [self.x - self.width // 4, self.y - self.height // 4, 
                                           self.width // 2, self.height // 4])
        elif self.type == 'barrier':
            # Road barrier with glow effect
            for offset in range(3, 0, -1):
                glow_color = (255, 50, 50, 100 - offset * 30)
                glow_surface = pygame.Surface((self.width + offset * 4, self.height + offset * 4), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, glow_color, 
                               [0, 0, self.width + offset * 4, self.height + offset * 4], 0, 5)
                screen.blit(glow_surface, 
                          (self.x - self.width // 2 - offset * 2, self.y - self.height // 2 - offset * 2))
            
            # Road barrier
            pygame.draw.rect(screen, BRIGHT_RED, [self.x - self.width // 2, self.y - self.height // 2, 
                                         self.width, self.height], 0, 5)
            for i in range(3):
                y_pos = self.y - self.height // 2 + (i * self.height // 3)
                pygame.draw.rect(screen, SLEEK_SILVER, [self.x - self.width // 2, y_pos, 
                                               self.width, self.height // 6])
        else:  # pothole
            # Pothole with glow effect
            for offset in range(3, 0, -1):
                glow_color = (0, 0, 50, 100 - offset * 30)
                glow_surface = pygame.Surface((self.width + offset * 4, self.height + offset * 4), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surface, glow_color, 
                                  [0, 0, self.width + offset * 4, self.height + offset * 4])
                screen.blit(glow_surface, 
                          (self.x - self.width // 2 - offset * 2, self.y - self.height // 2 - offset * 2))
            
            # Pothole
            pygame.draw.ellipse(screen, MATTE_BLACK, [self.x - self.width // 2, self.y - self.height // 2, 
                                              self.width, self.height])
            # Inner pothole with gradient
            inner_color = (20, 20, 40)
            pygame.draw.ellipse(screen, inner_color, [self.x - self.width // 2 + 5, self.y - self.height // 2 + 5, 
                                                  self.width - 10, self.height - 10])
        
    def move(self, speed):
        self.y += speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2
        
    def collides_with(self, car):
        return (abs(self.x - car.x) < (self.width + car.width) // 2 and 
                abs(self.y - car.y) < (self.height + car.height) // 2)

class MovingObstacle(Obstacle):
    def __init__(self, lane):
        super().__init__(lane)
        self.move_direction = random.choice([-1, 1])
        self.move_speed = random.uniform(0.5, 2.0)
        self.original_x = self.x
        self.move_range = LANE_WIDTH * 0.4
        self.move_progress = 0
    
    def update(self, dt):
        # Move side to side
        self.move_progress += self.move_speed * dt
        offset = math.sin(self.move_progress) * self.move_range
        self.x = self.original_x + offset
class OtherCar:
    def __init__(self, lane):
        self.lane = lane
        self.x = LANE_POSITIONS[lane]
        self.y = -CAR_HEIGHT // 2
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = random.choice([NEON_GREEN, ELECTRIC_PURPLE, (255, 165, 0), (128, 0, 128), METALLIC_SILVER])
        self.car_type = random.choice(['sedan', 'suv', 'truck'])
        if self.car_type == 'truck':
            self.height = int(CAR_HEIGHT * 1.3)
        elif self.car_type == 'suv':
            self.height = int(CAR_HEIGHT * 1.1)
        
    def draw(self, screen):
        # Car body
        if self.car_type == 'truck':
            # Truck body (cab + trailer)
            cab_height = self.height // 3
            
            # Trailer
            pygame.draw.rect(screen, METALLIC_SILVER, [self.x - self.width // 2, self.y - self.height // 2 + cab_height, 
                                            self.width, self.height - cab_height], 0, 5)
            
            # Add metallic effect with gradient
            highlight_color = (min(METALLIC_SILVER[0] + 40, 255), min(METALLIC_SILVER[1] + 40, 255), min(METALLIC_SILVER[2] + 40, 255))
            pygame.draw.rect(screen, highlight_color, 
                           [self.x - self.width // 2, self.y - self.height // 2 + cab_height, 
                            self.width // 2, self.height - cab_height], 0, 5)
            
            # Cab
            pygame.draw.rect(screen, self.color, [self.x - self.width // 2, self.y - self.height // 2, 
                                                self.width, cab_height], 0, 5)
            
            # Add metallic effect with gradient to cab
            highlight_color = (min(self.color[0] + 40, 255), min(self.color[1] + 40, 255), min(self.color[2] + 40, 255))
            pygame.draw.rect(screen, highlight_color, 
                           [self.x - self.width // 2, self.y - self.height // 2, 
                            self.width // 2, cab_height], 0, 5)
            
            # Windshield
            windshield_width = int(self.width * 0.7)
            windshield_height = int(cab_height * 0.6)
            windshield_x = self.x - windshield_width // 2
            windshield_y = self.y - self.height // 2 + int(cab_height * 0.2)
            pygame.draw.rect(screen, (100, 200, 255), [windshield_x, windshield_y, 
                                                     windshield_width, windshield_height], 0, 3)
            
            # Wheels (6 wheels for truck)
            wheel_width = int(self.width * 0.2)
            wheel_height = int(self.height * 0.1)
            
            wheel_positions = [
                (self.x - self.width // 2 - 3, self.y - self.height // 2 + cab_height - wheel_height // 2),
                (self.x + self.width // 2 - wheel_width + 3, self.y - self.height // 2 + cab_height - wheel_height // 2),
                (self.x - self.width // 2 - 3, self.y),
                (self.x + self.width // 2 - wheel_width + 3, self.y),
                (self.x - self.width // 2 - 3, self.y + self.height // 2 - wheel_height),
                (self.x + self.width // 2 - wheel_width + 3, self.y + self.height // 2 - wheel_height)
            ]
            
            for pos in wheel_positions:
                pygame.draw.rect(screen, MATTE_BLACK, [pos[0], pos[1], wheel_width, wheel_height], 0, 3)
                # Add wheel rim
                pygame.draw.rect(screen, SLEEK_SILVER, [pos[0] + 3, pos[1] + 3, wheel_width - 6, wheel_height - 6], 0, 3)
                
        else:  # sedan or SUV
            # Car body
            pygame.draw.rect(screen, self.color, [self.x - self.width // 2, self.y - self.height // 2, 
                                                self.width, self.height], 0, 10)
            
            # Add metallic effect with gradient
            highlight_color = (min(self.color[0] + 40, 255), min(self.color[1] + 40, 255), min(self.color[2] + 40, 255))
            pygame.draw.rect(screen, highlight_color, 
                           [self.x - self.width // 2, self.y - self.height // 2, 
                            self.width // 2, self.height], 0, 10)
            
            # Windshield
            windshield_width = int(self.width * 0.8)
            windshield_height = int(self.height * 0.25)
            windshield_x = self.x - windshield_width // 2
            windshield_y = self.y - self.height // 2 + int(self.height * 0.15)
            pygame.draw.rect(screen, (100, 200, 255), [windshield_x, windshield_y, 
                                                     windshield_width, windshield_height], 0, 5)
            
            # Roof
            roof_width = int(self.width * 0.8)
            roof_height = int(self.height * 0.2)
            roof_x = self.x - roof_width // 2
            roof_y = self.y - self.height // 2 + int(self.height * 0.15) + windshield_height
            pygame.draw.rect(screen, self.color, [roof_x, roof_y, 
                                                roof_width, roof_height], 0, 5)
            
            # Rear window
            rear_window_width = int(self.width * 0.7)
            rear_window_height = int(self.height * 0.2)
            rear_window_x = self.x - rear_window_width // 2
            rear_window_y = roof_y + roof_height
            pygame.draw.rect(screen, (100, 200, 255), [rear_window_x, rear_window_y, 
                                                     rear_window_width, rear_window_height], 0, 5)
            
            # Wheels
            wheel_width = int(self.width * 0.25)
            wheel_height = int(self.height * 0.15)
            
            wheel_positions = [
                (self.x - self.width // 2 - 3, self.y - self.height // 4),
                (self.x + self.width // 2 - wheel_width + 3, self.y - self.height // 4),
                (self.x - self.width // 2 - 3, self.y + self.height // 4 - wheel_height),
                (self.x + self.width // 2 - wheel_width + 3, self.y + self.height // 4 - wheel_height)
            ]
            
            for pos in wheel_positions:
                pygame.draw.rect(screen, MATTE_BLACK, [pos[0], pos[1], wheel_width, wheel_height], 0, 3)
                # Add wheel rim
                pygame.draw.rect(screen, SLEEK_SILVER, [pos[0] + 3, pos[1] + 3, wheel_width - 6, wheel_height - 6], 0, 3)
            
            # Headlights
            headlight_width = int(self.width * 0.15)
            headlight_height = int(self.height * 0.08)
            
            # Left headlight
            pygame.draw.rect(screen, NEON_YELLOW, [self.x - self.width // 2 + 5, 
                                            self.y - self.height // 2 + 5, 
                                            headlight_width, headlight_height], 0, 3)
            
            # Right headlight
            pygame.draw.rect(screen, NEON_YELLOW, [self.x + self.width // 2 - headlight_width - 5, 
                                            self.y - self.height // 2 + 5, 
                                            headlight_width, headlight_height], 0, 3)
            
            # Taillights
            taillight_width = int(self.width * 0.15)
            taillight_height = int(self.height * 0.08)
            
            # Left taillight
            pygame.draw.rect(screen, BRIGHT_RED, [self.x - self.width // 2 + 5, 
                                         self.y + self.height // 2 - taillight_height - 5, 
                                         taillight_width, taillight_height], 0, 3)
            
            # Right taillight
            pygame.draw.rect(screen, BRIGHT_RED, [self.x + self.width // 2 - taillight_width - 5, 
                                         self.y + self.height // 2 - taillight_height - 5, 
                                         taillight_width, taillight_height], 0, 3)
        
    def move(self, speed):
        self.y += speed
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2
        
    def collides_with(self, car):
        return (abs(self.x - car.x) < (self.width + car.width) // 2 and 
                abs(self.y - car.y) < (self.height + car.height) // 2)

class AIControlledCar(OtherCar):
    def __init__(self, lane):
        super().__init__(lane)
        self.ai_type = random.choice(['normal', 'aggressive', 'cautious'])
        self.lane_change_cooldown = 0
        self.brake_cooldown = 0
        self.is_braking = False
        self.target_lane = lane
    
    def update(self, dt, player_lane, obstacles):
        # Update lane change cooldown
        if self.lane_change_cooldown > 0:
            self.lane_change_cooldown -= dt
        
        # Update brake cooldown
        if self.brake_cooldown > 0:
            self.brake_cooldown -= dt
            if self.brake_cooldown <= 0:
                self.is_braking = False
        
        # AI decision making
        if self.lane_change_cooldown <= 0:
            # Check for obstacles in current lane
            obstacle_ahead = False
            for obstacle in obstacles:
                if obstacle.lane == self.lane and obstacle.y > self.y and obstacle.y - self.y < 200:
                    obstacle_ahead = True
                    break
            
            # Decide whether to change lanes
            if obstacle_ahead:
                # Find a safe lane to move to
                safe_lanes = []
                for l in range(6):  # Changed from 4 to 6 for 6 lanes
                    if l != self.lane:
                        lane_safe = True
                        for obstacle in obstacles:
                            if obstacle.lane == l and abs(obstacle.y - self.y) < 150:
                                lane_safe = False
                                break
                        if lane_safe:
                            safe_lanes.append(l)
                
                if safe_lanes:
                    self.target_lane = random.choice(safe_lanes)
                    self.lane_change_cooldown = random.uniform(1.0, 3.0)
                elif self.ai_type == 'aggressive':
                    # Aggressive cars might brake suddenly
                    if random.random() < 0.3 and self.brake_cooldown <= 0:
                        self.is_braking = True
                        self.brake_cooldown = random.uniform(0.5, 1.5)
            elif self.ai_type == 'aggressive' and random.random() < 0.05 and self.lane != player_lane:
                # Aggressive cars might randomly change lanes to block player
                self.target_lane = player_lane
                self.lane_change_cooldown = random.uniform(2.0, 4.0)
            elif self.ai_type == 'normal' and random.random() < 0.02:
                # Normal cars occasionally change lanes randomly
                new_lane = random.randint(0, 5)  # Changed from 0-3 to 0-5 for 6 lanes
                if new_lane != self.lane:
                    self.target_lane = new_lane
                    self.lane_change_cooldown = random.uniform(2.0, 5.0)
        
        # Move towards target lane
        if self.lane != self.target_lane:
            if self.target_lane > self.lane:
                self.lane += 1
            else:
                self.lane -= 1
            self.x = LANE_POSITIONS[self.lane]
class Game:
    def __init__(self):
        # Create a resizable window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Car Racing Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.particle_system = ParticleSystem()
        self.highscore_manager = HighScoreManager()
        self.reset_game()
    def reset_game(self):
        self.player_car = Car(LANE_POSITIONS[1], SCREEN_HEIGHT - 150, CAR_WIDTH, CAR_HEIGHT, RED)
        self.obstacles = []
        self.other_cars = []
        self.powerups = []
        self.coins = []
        self.speed = INITIAL_SPEED
        self.score = 0
        self.coins_collected = 0
        self.game_over = False
        self.last_obstacle_time = time.time()
        self.last_car_time = time.time()
        self.last_powerup_time = time.time()
        self.last_coin_time = time.time()
        self.last_update_time = time.time()
        self.combo_count = 0
        self.combo_timer = 0
        self.score_multiplier = 1
        self.game_mode = GAME_MODE_ENDLESS
        self.distance_traveled = 0
        self.time_remaining = 60  # for time attack mode
        self.mission_type = random.randint(0, 3)  # Keep this as is - it's for mission types, not lanes
        self.mission_target = 0
        self.mission_progress = 0
        self.set_mission()
        self.start_time = time.time()
        self.powerups_used = 0
        self.player_name = "Player"  # Default player name
        
    def set_mission(self):
        if self.mission_type == MISSION_COLLECT_COINS:
            self.mission_target = random.randint(10, 30)
            self.mission_description = f"Collect {self.mission_target} coins"
        elif self.mission_type == MISSION_DISTANCE:
            self.mission_target = random.randint(1000, 3000)
            self.mission_description = f"Travel {self.mission_target}m"
        elif self.mission_type == MISSION_AVOID_CRASHES:
            self.mission_target = random.randint(30, 60)
            self.mission_description = f"Survive {self.mission_target} seconds"
        elif self.mission_type == MISSION_USE_POWERUPS:
            self.mission_target = random.randint(3, 8)
            self.mission_description = f"Use {self.mission_target} power-ups"
    def show_name_input(self):
        """Show a screen to input player name for high score"""
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 400, 50)
        color_inactive = SLEEK_SILVER
        color_active = NEON_YELLOW
        color = color_inactive
        active = True
        text = self.player_name
        done = False
        
        title_font = pygame.font.SysFont("arial", 48, bold=True)
        input_font = pygame.font.SysFont("arial", 32)
        
        # Create a semi-transparent background
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))  # Semi-transparent black
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    active = input_box.collidepoint(event.pos)
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYUP:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.player_name = text
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            # Limit name length to 15 characters
                            if len(text) < 15:
                                text += event.unicode
            
            # Draw background
            self.screen.blit(background, (0, 0))
            
            # Draw title
            title_text = title_font.render("NEW HIGH SCORE!", True, NEON_YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(title_text, title_rect)
            
            # Draw score
            score_text = input_font.render(f"Score: {self.score}", True, ELECTRIC_PURPLE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
            self.screen.blit(score_text, score_rect)
            
            # Draw prompt
            prompt_text = input_font.render("Enter your name:", True, WHITE)
            prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(prompt_text, prompt_rect)
            
            # Draw input box
            pygame.draw.rect(self.screen, color, input_box, 2, border_radius=10)
            
            # Draw input text
            txt_surface = input_font.render(text, True, WHITE)
            # Ensure text doesn't overflow the input box
            width = max(400, txt_surface.get_width() + 10)
            input_box.w = width
            input_box.x = SCREEN_WIDTH // 2 - width // 2
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            
            # Draw instructions
            instruction_text = pygame.font.SysFont("arial", 24).render("Press ENTER to confirm", True, SLEEK_SILVER)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
        
        return text
    def show_highscores(self):
        """Show the high scores screen"""
        # Get high scores for current game mode
        highscores = self.highscore_manager.get_highscores(self.game_mode)
        
        # Create a semi-transparent background
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))  # Semi-transparent black
        
        title_font = pygame.font.SysFont("arial", 48, bold=True)
        score_font = pygame.font.SysFont("arial", 24)
        
        # Get mode name for display
        if self.game_mode == GAME_MODE_ENDLESS:
            mode_name = "ENDLESS MODE"
        elif self.game_mode == GAME_MODE_TIME_ATTACK:
            mode_name = "TIME ATTACK MODE"
        else:
            mode_name = "MISSIONS MODE"
        
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    done = True
            
            # Draw background
            self.screen.blit(background, (0, 0))
            
            # Draw title
            title_text = title_font.render("HIGH SCORES", True, NEON_YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
            self.screen.blit(title_text, title_rect)
            
            # Draw mode name
            mode_text = score_font.render(mode_name, True, ELECTRIC_PURPLE)
            mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 50))
            self.screen.blit(mode_text, mode_rect)
            
            # Draw column headers
            header_y = SCREEN_HEIGHT // 6 + 100
            rank_text = score_font.render("RANK", True, SLEEK_SILVER)
            name_text = score_font.render("NAME", True, SLEEK_SILVER)
            score_text = score_font.render("SCORE", True, SLEEK_SILVER)
            date_text = score_font.render("DATE", True, SLEEK_SILVER)
            
            self.screen.blit(rank_text, (SCREEN_WIDTH // 5 - rank_text.get_width() // 2, header_y))
            self.screen.blit(name_text, (SCREEN_WIDTH * 2 // 5 - name_text.get_width() // 2, header_y))
            self.screen.blit(score_text, (SCREEN_WIDTH * 3 // 5 - score_text.get_width() // 2, header_y))
            self.screen.blit(date_text, (SCREEN_WIDTH * 4 // 5 - date_text.get_width() // 2, header_y))
            
            # Draw horizontal line
            pygame.draw.line(self.screen, SLEEK_SILVER, 
                           (SCREEN_WIDTH // 10, header_y + 30), 
                           (SCREEN_WIDTH * 9 // 10, header_y + 30), 2)
            
            # Draw high scores
            if not highscores:
                no_scores_text = score_font.render("No high scores yet!", True, WHITE)
                no_scores_rect = no_scores_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(no_scores_text, no_scores_rect)
            else:
                for i, score in enumerate(highscores):
                    y_pos = header_y + 60 + i * 40
                    
                    # Highlight the player's score
                    if score["name"] == self.player_name:
                        highlight_rect = pygame.Rect(SCREEN_WIDTH // 10, y_pos - 5, 
                                                  SCREEN_WIDTH * 8 // 10, 30)
                        pygame.draw.rect(self.screen, (50, 50, 100, 100), highlight_rect, border_radius=5)
                    
                    # Rank
                    rank_text = score_font.render(f"{i+1}", True, WHITE)
                    self.screen.blit(rank_text, (SCREEN_WIDTH // 5 - rank_text.get_width() // 2, y_pos))
                    
                    # Name
                    name_text = score_font.render(score["name"], True, WHITE)
                    self.screen.blit(name_text, (SCREEN_WIDTH * 2 // 5 - name_text.get_width() // 2, y_pos))
                    
                    # Score
                    score_text = score_font.render(f"{score['score']}", True, WHITE)
                    self.screen.blit(score_text, (SCREEN_WIDTH * 3 // 5 - score_text.get_width() // 2, y_pos))
                    
                    # Date
                    date_text = score_font.render(score["date"], True, WHITE)
                    self.screen.blit(date_text, (SCREEN_WIDTH * 4 // 5 - date_text.get_width() // 2, y_pos))
            
            # Draw instructions
            instruction_text = score_font.render("Press any key to continue", True, SLEEK_SILVER)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(30)
    def show_menu(self):
        # Create gradient background
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            # Calculate gradient color
            r = int(DEEP_BLUE[0])
            g = int(DEEP_BLUE[1])
            b = int(DEEP_BLUE[2])
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        self.screen.blit(background, (0, 0))
        
        # Add some decorative elements
        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            pygame.draw.circle(self.screen, SLEEK_SILVER, (x, y), size)
        
        # Draw some decorative lines
        for i in range(5):
            start_x = random.randint(0, SCREEN_WIDTH)
            end_x = random.randint(0, SCREEN_WIDTH)
            pygame.draw.line(self.screen, NEON_YELLOW, (start_x, 0), (end_x, SCREEN_HEIGHT), 1)
        
        title_font = pygame.font.SysFont("arial", 72, bold=True)
        menu_font = pygame.font.SysFont("arial", 48)
        
        # Draw a metallic border around the title
        title_text = title_font.render("CAR RACING", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        
        # Draw a glowing effect around the title
        for offset in range(5, 0, -1):
            glow_rect = title_rect.copy()
            glow_rect.inflate_ip(offset * 2, offset * 2)
            pygame.draw.rect(self.screen, (min(NEON_YELLOW[0], 255), min(NEON_YELLOW[1] - offset * 10, 255), min(NEON_YELLOW[2], 255)), 
                           glow_rect, 2, border_radius=10)
        
        self.screen.blit(title_text, title_rect)
        
        # If game over, show game over text and score with special effects
        if self.game_over:
            game_over_text = title_font.render("GAME OVER", True, BRIGHT_RED)
            score_text = menu_font.render(f"FINAL SCORE: {self.score}", True, NEON_YELLOW)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80))
            
            # Add glow effect to game over text
            for offset in range(8, 0, -1):
                glow_rect = game_over_rect.copy()
                glow_rect.inflate_ip(offset * 3, offset * 3)
                pygame.draw.rect(self.screen, (min(BRIGHT_RED[0], 255), min(BRIGHT_RED[1], 255), min(BRIGHT_RED[2] + offset * 5, 255)), 
                               glow_rect, 2, border_radius=5)
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            
            # Check if this is a high score
            if self.highscore_manager.is_high_score(self.game_mode, self.score):
                # Get player name and save high score
                self.player_name = self.show_name_input()
                self.highscore_manager.add_score(
                    self.game_mode,
                    self.player_name,
                    self.score,
                    distance=int(self.distance_traveled),
                    coins=self.coins_collected
                )
                # Show high scores
                self.show_highscores()
        
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Create stylish menu buttons with hover effects
        options = [
            ("GAME MODES", ELECTRIC_PURPLE, -2),
            ("NEW GAME", NEON_YELLOW, -1), 
            ("HIGH SCORES", NEON_GREEN, -3),
            ("EXIT", BRIGHT_RED, pygame.K_ESCAPE)
        ]
        
        button_rects = []
        
        for i, (text, default_color, key) in enumerate(options):
            option_text = menu_font.render(text, True, default_color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70 * i))
            
            # Draw button background
            button_rect = option_rect.copy()
            button_rect.inflate_ip(40, 20)
            
            # Check if mouse is hovering over this button
            is_hovering = button_rect.collidepoint(mouse_pos)
            
            # Store button rect for click detection
            button_rects.append((button_rect, key))
            
            # Change color when hovering
            if is_hovering:
                # Hover effect - brighter color and pulsating glow
                hover_color = (min(default_color[0] + 50, 255), 
                              min(default_color[1] + 50, 255), 
                              min(default_color[2] + 50, 255))
                
                # Pulsating effect based on time
                pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
                
                # Draw multiple glowing borders
                for offset in range(5, 0, -1):
                    glow_rect = button_rect.copy()
                    glow_rect.inflate_ip(offset * pulse, offset * pulse)
                    pygame.draw.rect(self.screen, hover_color, glow_rect, 2, border_radius=10)
                
                # Draw filled button with hover color
                pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                pygame.draw.rect(self.screen, hover_color, button_rect, 2, border_radius=10)
                
                # Render text with hover color
                option_text = menu_font.render(text, True, hover_color)
            else:
                # Normal state
                pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                pygame.draw.rect(self.screen, default_color, button_rect, 2, border_radius=10)
            
            self.screen.blit(option_text, option_rect)
        
        pygame.display.flip()
        
        waiting = True
        clock = pygame.time.Clock()
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for rect, key in button_rects:
                            if rect.collidepoint(event.pos):
                                if key == -1:  # New Game (Endless mode)
                                    self.game_mode = GAME_MODE_ENDLESS
                                    self.reset_game()
                                    return True
                                elif key == -2:  # Game Modes
                                    return self.show_game_mode_menu()
                                elif key == -3:  # High Scores
                                    self.show_highscores()
                                    # Redraw menu after returning from high scores
                                    return self.show_menu()
                                elif key == pygame.K_ESCAPE:
                                    return False
            
            # Update display for hover effects
            mouse_pos = pygame.mouse.get_pos()
            redraw_needed = False
            
            # Check if any button state has changed
            for i, (text, default_color, key) in enumerate(options):
                button_rect = button_rects[i][0]
                is_hovering = button_rect.collidepoint(mouse_pos)
                if is_hovering:
                    redraw_needed = True
                    break
            
            # Only redraw if needed
            if redraw_needed:
                # Redraw background
                self.screen.blit(background, (0, 0))
                
                # Redraw decorative elements
                for i in range(20):
                    x = random.randint(0, SCREEN_WIDTH)
                    y = random.randint(0, SCREEN_HEIGHT)
                    size = random.randint(1, 3)
                    pygame.draw.circle(self.screen, SLEEK_SILVER, (x, y), size)
                
                # Redraw title
                self.screen.blit(title_text, title_rect)
                
                # Redraw game over if needed
                if self.game_over:
                    self.screen.blit(game_over_text, game_over_rect)
                    self.screen.blit(score_text, score_rect)
                
                # Redraw buttons with updated hover states
                for i, (text, default_color, key) in enumerate(options):
                    option_text = menu_font.render(text, True, default_color)
                    option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70 * i))
                    
                    button_rect = option_rect.copy()
                    button_rect.inflate_ip(40, 20)
                    
                    is_hovering = button_rect.collidepoint(mouse_pos)
                    
                    if is_hovering:
                        hover_color = (min(default_color[0] + 50, 255), 
                                      min(default_color[1] + 50, 255), 
                                      min(default_color[2] + 50, 255))
                        
                        pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
                        
                        for offset in range(5, 0, -1):
                            glow_rect = button_rect.copy()
                            glow_rect.inflate_ip(offset * pulse, offset * pulse)
                            pygame.draw.rect(self.screen, hover_color, glow_rect, 2, border_radius=10)
                        
                        pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                        pygame.draw.rect(self.screen, hover_color, button_rect, 2, border_radius=10)
                        
                        option_text = menu_font.render(text, True, hover_color)
                    else:
                        pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                        pygame.draw.rect(self.screen, default_color, button_rect, 2, border_radius=10)
                    
                    self.screen.blit(option_text, option_rect)
                
                pygame.display.flip()
            
            clock.tick(30)

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    finally:
        pygame.quit()
        sys.exit()
    def run(self):
        running = True
        in_menu = True
        
        while running:
            if in_menu:
                running = self.show_menu()
                in_menu = False
            else:
                running = self.handle_events()
                if not self.game_over:
                    self.update()
                    self.draw()
                else:
                    in_menu = True
                    
            self.clock.tick(60)
    def handle_events(self):
        global SCREEN_WIDTH, SCREEN_HEIGHT, LANE_WIDTH, LANE_POSITIONS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player_car.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.player_car.move_right()
                elif event.key == pygame.K_SPACE:
                    # Use boost when space is pressed
                    self.player_car.use_boost_energy()
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    # Show pause menu when ESC or P is pressed
                    pause_result = self.show_pause_menu()
                    if not pause_result:
                        return False
            # Handle mouse clicks for pause button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if pause button was clicked
                    pause_button_rect = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)
                    if pause_button_rect.collidepoint(event.pos):
                        pause_result = self.show_pause_menu()
                        if not pause_result:
                            return False
            # Handle window resize
            if event.type == pygame.VIDEORESIZE:
                # Update screen dimensions
                SCREEN_WIDTH = event.w
                SCREEN_HEIGHT = event.h
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                # Update player position
                self.player_car.x = LANE_POSITIONS[self.player_car.lane]
                self.player_car.y = SCREEN_HEIGHT - 150
                # Resize the screen
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        return True
    def show_pause_menu(self):
        # Create pause menu
        pause_menu = PauseMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Store the current game state
        game_state_surface = self.screen.copy()
        
        # Main pause menu loop
        clock = pygame.time.Clock()
        while True:
            # Restore the game state as background
            self.screen.blit(game_state_surface, (0, 0))
            
            # Draw and handle the pause menu
            pause_menu.draw()
            result = pause_menu.handle_input()
            
            if result == "RESUME":
                return True
            elif result == "OPTIONS":
                self.show_settings_menu(game_state_surface)
            elif result == "MAIN MENU":
                self.game_over = True
                return True
            elif result == "EXIT":
                return False
            elif result == "RESIZE":
                # Update the stored game state after resize
                game_state_surface = self.screen.copy()
            
            clock.tick(30)
            game_state_surface = self.screen.copy()
            
            clock.tick(30)
    
    def show_settings_menu(self, background_surface):
        # Create settings menu
        settings_menu = SettingsMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Main settings menu loop
        clock = pygame.time.Clock()
        while True:
            # Restore the background
            self.screen.blit(background_surface, (0, 0))
            
            # Draw and handle the settings menu
            settings_menu.draw()
            result = settings_menu.handle_input()
            
            if result == "BACK":
                return
            elif result == "EXIT":
                pygame.quit()
                sys.exit()
            elif result == "RESIZE":
                # Update the stored background after resize
                background_surface = self.screen.copy()
            
            clock.tick(30)
class PauseMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont("arial", int(screen_height * 0.06), bold=True)
        self.font_medium = pygame.font.SysFont("arial", int(screen_height * 0.04), bold=True)
        self.font_small = pygame.font.SysFont("arial", int(screen_height * 0.03))
        self.options = ["RESUME", "OPTIONS", "MAIN MENU", "EXIT"]
        self.selected_option = 0
        self.background = None
        self.create_background()
        
    def create_background(self):
        # Create a semi-transparent background
        self.background = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 180))  # Semi-transparent black
        
        # Add some decorative elements
        for i in range(20):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 3)
            pygame.draw.circle(self.background, SLEEK_SILVER, (x, y), size)
    
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont("arial", int(screen_height * 0.06), bold=True)
        self.font_medium = pygame.font.SysFont("arial", int(screen_height * 0.04), bold=True)
        self.font_small = pygame.font.SysFont("arial", int(screen_height * 0.03))
        self.create_background()
    
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title_text = self.font_large.render("PAUSED", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.2))
        
        # Draw glow effect around title
        for offset in range(5, 0, -1):
            glow_rect = title_rect.copy()
            glow_rect.inflate_ip(offset * 2, offset * 2)
            pygame.draw.rect(self.screen, (min(NEON_YELLOW[0], 255), min(NEON_YELLOW[1] - offset * 10, 255), min(NEON_YELLOW[2], 255)), 
                           glow_rect, 2, border_radius=10)
        
        self.screen.blit(title_text, title_rect)
        
        # Draw menu options
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = ELECTRIC_PURPLE
                # Pulsating effect
                pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
                text = self.font_medium.render(f"> {option} <", True, color)
            else:
                color = WHITE
                text = self.font_medium.render(option, True, color)
            
            rect = text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.4 + i * self.screen_height * 0.08))
            
            if i == self.selected_option:
                # Draw glowing border around selected option
                button_rect = rect.copy()
                button_rect.inflate_ip(20, 10)
                for offset in range(3, 0, -1):
                    glow_rect = button_rect.copy()
                    glow_rect.inflate_ip(offset * pulse, offset * pulse)
                    pygame.draw.rect(self.screen, color, glow_rect, 2, border_radius=5)
            
            self.screen.blit(text, rect)
        
        # Draw controls hint
        controls_text = self.font_small.render("UP/DOWN: Navigate | ENTER: Select | ESC: Resume", True, SLEEK_SILVER)
        controls_rect = controls_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.85))
        self.screen.blit(controls_text, controls_rect)
        
        pygame.display.flip()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "RESUME"
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected_option]
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
                return "RESIZE"
        return None

class SettingsMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont("arial", int(screen_height * 0.06), bold=True)
        self.font_medium = pygame.font.SysFont("arial", int(screen_height * 0.04), bold=True)
        self.font_small = pygame.font.SysFont("arial", int(screen_height * 0.03))
        
        # Settings options and their values
        self.settings = {
            "DIFFICULTY": ["EASY", "NORMAL", "HARD"],
            "MUSIC VOLUME": ["OFF", "LOW", "MEDIUM", "HIGH"],
            "SFX VOLUME": ["OFF", "LOW", "MEDIUM", "HIGH"],
            "FULLSCREEN": ["OFF", "ON"],
            "BACK": None
        }
        
        # Current values for each setting
        self.current_values = {
            "DIFFICULTY": 1,  # NORMAL
            "MUSIC VOLUME": 2,  # MEDIUM
            "SFX VOLUME": 2,  # MEDIUM
            "FULLSCREEN": 0,  # OFF
        }
        
        self.options = list(self.settings.keys())
        self.selected_option = 0
        self.background = None
        self.create_background()
    
    def create_background(self):
        # Create a semi-transparent background
        self.background = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 180))  # Semi-transparent black
        
        # Add some decorative elements
        for i in range(20):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 3)
            pygame.draw.circle(self.background, SLEEK_SILVER, (x, y), size)
    
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont("arial", int(screen_height * 0.06), bold=True)
        self.font_medium = pygame.font.SysFont("arial", int(screen_height * 0.04), bold=True)
        self.font_small = pygame.font.SysFont("arial", int(screen_height * 0.03))
        self.create_background()
    
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title_text = self.font_large.render("SETTINGS", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.15))
        
        # Draw glow effect around title
        for offset in range(5, 0, -1):
            glow_rect = title_rect.copy()
            glow_rect.inflate_ip(offset * 2, offset * 2)
            pygame.draw.rect(self.screen, (min(NEON_YELLOW[0], 255), min(NEON_YELLOW[1] - offset * 10, 255), min(NEON_YELLOW[2], 255)), 
                           glow_rect, 2, border_radius=10)
        
        self.screen.blit(title_text, title_rect)
        
        # Draw settings options
        for i, option in enumerate(self.options):
            # Determine text color based on selection
            if i == self.selected_option:
                option_color = ELECTRIC_PURPLE
                value_color = NEON_GREEN
            else:
                option_color = WHITE
                value_color = SLEEK_SILVER
            
            # Draw option name
            option_text = self.font_medium.render(option, True, option_color)
            option_rect = option_text.get_rect(midleft=(self.screen_width * 0.3, self.screen_height * 0.3 + i * self.screen_height * 0.08))
            
            # Draw option value if applicable
            if self.settings[option] is not None:
                value_text = self.font_medium.render(self.settings[option][self.current_values[option]], True, value_color)
                value_rect = value_text.get_rect(midright=(self.screen_width * 0.7, self.screen_height * 0.3 + i * self.screen_height * 0.08))
                
                # Draw arrows for selected option
                if i == self.selected_option:
                    # Left arrow
                    if self.current_values[option] > 0:
                        left_arrow = self.font_medium.render("<", True, NEON_GREEN)
                        left_rect = left_arrow.get_rect(midright=(value_rect.left - 10, value_rect.centery))
                        self.screen.blit(left_arrow, left_rect)
                    
                    # Right arrow
                    if self.current_values[option] < len(self.settings[option]) - 1:
                        right_arrow = self.font_medium.render(">", True, NEON_GREEN)
                        right_rect = right_arrow.get_rect(midleft=(value_rect.right + 10, value_rect.centery))
                        self.screen.blit(right_arrow, right_rect)
                
                self.screen.blit(value_text, value_rect)
            
            # Draw selection indicator and glow for selected option
            if i == self.selected_option:
                # Pulsating effect
                pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
                
                if option == "BACK":
                    # Special handling for BACK button
                    back_rect = option_rect.copy()
                    back_rect.inflate_ip(40, 20)
                    for offset in range(3, 0, -1):
                        glow_rect = back_rect.copy()
                        glow_rect.inflate_ip(offset * pulse, offset * pulse)
                        pygame.draw.rect(self.screen, ELECTRIC_PURPLE, glow_rect, 2, border_radius=5)
                else:
                    # Draw indicator for other options
                    pygame.draw.circle(self.screen, ELECTRIC_PURPLE, (option_rect.left - 15, option_rect.centery), 5)
            
            self.screen.blit(option_text, option_rect)
        
        # Draw controls hint
        controls_text = self.font_small.render("UP/DOWN: Navigate | LEFT/RIGHT: Change Value | ENTER: Select | ESC: Back", True, SLEEK_SILVER)
        controls_rect = controls_text.get_rect(center=(self.screen_width // 2, self.screen_height * 0.85))
        self.screen.blit(controls_text, controls_rect)
        
        pygame.display.flip()
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "BACK"
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    option = self.options[self.selected_option]
                    if self.settings[option] is not None and self.current_values[option] > 0:
                        self.current_values[option] -= 1
                        self.apply_setting(option)
                elif event.key == pygame.K_RIGHT:
                    option = self.options[self.selected_option]
                    if self.settings[option] is not None and self.current_values[option] < len(self.settings[option]) - 1:
                        self.current_values[option] += 1
                        self.apply_setting(option)
                elif event.key == pygame.K_RETURN:
                    option = self.options[self.selected_option]
                    if option == "BACK":
                        return "BACK"
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
                return "RESIZE"
        return None
    
    def apply_setting(self, option):
        # Apply the setting change
        if option == "FULLSCREEN":
            if self.current_values[option] == 1:  # ON
                pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
            else:  # OFF
                pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        
        # Other settings would be applied here
        # For now, we'll just print the change
        print(f"Setting {option} changed to {self.settings[option][self.current_values[option]]}")
    def draw_road(self):
        # Create gradient background for the road
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            # Calculate gradient color between DARK_SLATE and TEAL
            ratio = y / SCREEN_HEIGHT
            r = int(DARK_SLATE[0] * (1 - ratio) + TEAL[0] * ratio)
            g = int(DARK_SLATE[1] * (1 - ratio) + TEAL[1] * ratio)
            b = int(DARK_SLATE[2] * (1 - ratio) + TEAL[2] * ratio)
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        self.screen.blit(background, (0, 0))
        
        # Draw lane markings with metallic effect
        for i in range(7):  # Changed from 5 to 7 for 6 lanes
            x = i * LANE_WIDTH
            pygame.draw.line(self.screen, METALLIC_SILVER, (x, 0), (x, SCREEN_HEIGHT), 3)
            
        # Draw dashed lines in the middle of lanes with neon effect
        for i in range(1, 6):  # Changed from 1-4 to 1-6 for 6 lanes
            x = i * LANE_WIDTH
            for y in range(0, SCREEN_HEIGHT, 40):
                # Add a subtle glow effect to the lane markers
                for offset in range(2, 0, -1):
                    pygame.draw.line(self.screen, (min(WHITE[0] - offset * 30, 255), 
                                                min(WHITE[1] - offset * 30, 255), 
                                                min(WHITE[2], 255)), 
                                   (x - offset, y), (x - offset, y + 20), 1)
                    pygame.draw.line(self.screen, (min(WHITE[0] - offset * 30, 255), 
                                                min(WHITE[1] - offset * 30, 255), 
                                                min(WHITE[2], 255)), 
                                   (x + offset, y), (x + offset, y + 20), 1)
                pygame.draw.line(self.screen, WHITE, (x, y), (x, y + 20), 2)
    def draw(self):
        self.draw_road()
        
        # Draw coins
        for coin in self.coins:
            coin.draw(self.screen)
        
        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw player car
        self.player_car.draw(self.screen)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
            
        # Draw other cars
        for car in self.other_cars:
            car.draw(self.screen)
            
        # Draw particles
        self.particle_system.draw(self.screen)
            
        # Create a semi-transparent UI overlay at the top
        ui_height = 80
        ui_surface = pygame.Surface((SCREEN_WIDTH, ui_height), pygame.SRCALPHA)
        ui_surface.fill((MATTE_BLACK[0], MATTE_BLACK[1], MATTE_BLACK[2], 180))  # Semi-transparent
        self.screen.blit(ui_surface, (0, 0))
        
        # Draw score with electric purple glow
        score_font = pygame.font.SysFont("arial", 36, bold=True)
        score_text = score_font.render(f"SCORE: {self.score}", True, ELECTRIC_PURPLE)
        score_shadow = score_font.render(f"SCORE: {self.score}", True, (ELECTRIC_PURPLE[0]//3, ELECTRIC_PURPLE[1]//3, ELECTRIC_PURPLE[2]//3))
        self.screen.blit(score_shadow, (12, 12))  # Shadow effect
        self.screen.blit(score_text, (10, 10))
        
        # Draw combo and multiplier if active
        if self.combo_count > 0:
            combo_text = score_font.render(f"COMBO: {self.combo_count} x{self.score_multiplier}", True, NEON_YELLOW)
            combo_shadow = score_font.render(f"COMBO: {self.combo_count} x{self.score_multiplier}", True, 
                                          (NEON_YELLOW[0]//3, NEON_YELLOW[1]//3, NEON_YELLOW[2]//3))
            self.screen.blit(combo_shadow, (SCREEN_WIDTH - 252, 12))
            self.screen.blit(combo_text, (SCREEN_WIDTH - 250, 10))
        
        # Draw coins collected
        coin_text = score_font.render(f"COINS: {self.coins_collected}", True, COIN_COLOR)
        coin_shadow = score_font.render(f"COINS: {self.coins_collected}", True, 
                                     (COIN_COLOR[0]//3, COIN_COLOR[1]//3, COIN_COLOR[2]//3))
        self.screen.blit(coin_shadow, (12, 52))
        self.screen.blit(coin_text, (10, 50))
        
        # Draw speed with neon green effect
        speed_value = int(self.speed * 10)
        speed_text = score_font.render(f"SPEED: {speed_value} km/h", True, NEON_GREEN)
        speed_shadow = score_font.render(f"SPEED: {speed_value} km/h", True, (NEON_GREEN[0]//3, NEON_GREEN[1]//3, NEON_GREEN[2]//3))
        self.screen.blit(speed_shadow, (SCREEN_WIDTH // 2 - 102, 12))  # Shadow effect
        self.screen.blit(speed_text, (SCREEN_WIDTH // 2 - 100, 10))
        
        # Draw pause button
        pause_button_rect = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)
        pygame.draw.rect(self.screen, DEEP_BLUE, pause_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, NEON_YELLOW, pause_button_rect, 2, border_radius=5)
        
        # Draw pause symbol
        pygame.draw.rect(self.screen, NEON_YELLOW, (SCREEN_WIDTH - 40, 18, 8, 24))
        pygame.draw.rect(self.screen, NEON_YELLOW, (SCREEN_WIDTH - 28, 18, 8, 24))
        
        # Draw game mode specific UI
        if self.game_mode == GAME_MODE_TIME_ATTACK:
            # Draw time remaining
            time_text = score_font.render(f"TIME: {int(self.time_remaining)}s", True, BRIGHT_RED)
            time_shadow = score_font.render(f"TIME: {int(self.time_remaining)}s", True, 
                                         (BRIGHT_RED[0]//3, BRIGHT_RED[1]//3, BRIGHT_RED[2]//3))
            self.screen.blit(time_shadow, (SCREEN_WIDTH - 152, 52))
            self.screen.blit(time_text, (SCREEN_WIDTH - 150, 50))
        elif self.game_mode == GAME_MODE_MISSIONS:
            # Draw mission progress
            mission_text = score_font.render(f"{self.mission_description}: {self.mission_progress}/{self.mission_target}", 
                                          True, ELECTRIC_PURPLE)
            mission_shadow = score_font.render(f"{self.mission_description}: {self.mission_progress}/{self.mission_target}", 
                                            True, (ELECTRIC_PURPLE[0]//3, ELECTRIC_PURPLE[1]//3, ELECTRIC_PURPLE[2]//3))
            self.screen.blit(mission_shadow, (SCREEN_WIDTH // 2 - 202, 52))
            self.screen.blit(mission_text, (SCREEN_WIDTH // 2 - 200, 50))
        
        # Draw speed indicator bar
        max_speed = 150  # Maximum expected speed
        bar_width = 200
        bar_height = 15
        bar_x = SCREEN_WIDTH - bar_width - 20
        bar_y = 50
        
        # Background bar
        pygame.draw.rect(self.screen, SLEEK_SILVER, (bar_x, bar_y, bar_width, bar_height), 0, 5)
        
        # Speed fill
        speed_ratio = min(speed_value / max_speed, 1.0)
        speed_width = int(bar_width * speed_ratio)
        
        # Gradient color for speed bar based on speed
        if speed_ratio < 0.3:
            bar_color = NEON_GREEN
        elif speed_ratio < 0.7:
            bar_color = NEON_YELLOW
        else:
            bar_color = BRIGHT_RED
            
        pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, speed_width, bar_height), 0, 5)
        
        # Add a border to the speed bar
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1, 5)
        
        # Apply slow motion effect if active
        if self.player_car.has_slow_mo:
            slow_mo_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            slow_mo_overlay.fill((SLOW_MO_COLOR[0], SLOW_MO_COLOR[1], SLOW_MO_COLOR[2], 30))
            self.screen.blit(slow_mo_overlay, (0, 0))
            
            # Add time distortion visual effect
            for i in range(10):
                y = random.randint(0, SCREEN_HEIGHT)
                width = random.randint(50, 200)
                height = random.randint(1, 3)
                alpha = random.randint(20, 80)
                distortion = pygame.Surface((width, height), pygame.SRCALPHA)
                distortion.fill((255, 255, 255, alpha))
                self.screen.blit(distortion, (random.randint(0, SCREEN_WIDTH - width), y))
        
        pygame.display.flip()
    def update_mission_progress(self):
        if self.game_mode != GAME_MODE_MISSIONS:
            return
            
        if self.mission_type == MISSION_COLLECT_COINS:
            self.mission_progress = self.coins_collected
        elif self.mission_type == MISSION_DISTANCE:
            self.mission_progress = int(self.distance_traveled)
        elif self.mission_type == MISSION_AVOID_CRASHES:
            self.mission_progress = int(time.time() - self.start_time)
        elif self.mission_type == MISSION_USE_POWERUPS:
            self.mission_progress = self.powerups_used
            
        # Check if mission is complete
        if self.mission_progress >= self.mission_target:
            self.score += 100  # Bonus for completing mission
            self.mission_type = (self.mission_type + 1) % 4
            self.set_mission()
            self.mission_progress = 0
    def show_game_mode_menu(self):
        self.screen.fill(DEEP_BLUE)
        
        title_font = pygame.font.SysFont("arial", 72, bold=True)
        menu_font = pygame.font.SysFont("arial", 48)
        
        title_text = title_font.render("SELECT GAME MODE", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        self.screen.blit(title_text, title_rect)
        
        # Game mode options
        options = [
            ("ENDLESS", NEON_GREEN, GAME_MODE_ENDLESS),
            ("TIME ATTACK", ELECTRIC_PURPLE, GAME_MODE_TIME_ATTACK),
            ("MISSIONS", NEON_YELLOW, GAME_MODE_MISSIONS),
            ("BACK", BRIGHT_RED, -1)
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        button_rects = []
        
        for i, (text, color, mode) in enumerate(options):
            option_text = menu_font.render(text, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 70 * i))
            
            button_rect = option_rect.copy()
            button_rect.inflate_ip(40, 20)
            button_rects.append((button_rect, mode))
            
            is_hovering = button_rect.collidepoint(mouse_pos)
            
            if is_hovering:
                hover_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
                pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                pygame.draw.rect(self.screen, hover_color, button_rect, 2, border_radius=10)
                option_text = menu_font.render(text, True, hover_color)
            else:
                pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                pygame.draw.rect(self.screen, color, button_rect, 2, border_radius=10)
            
            self.screen.blit(option_text, option_rect)
        
        pygame.display.flip()
        
        waiting = True
        clock = pygame.time.Clock()
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for rect, mode in button_rects:
                            if rect.collidepoint(event.pos):
                                if mode == -1:
                                    return self.show_menu()  # Back to main menu
                                else:
                                    self.game_mode = mode
                                    self.reset_game()
                                    return True
            
            # Update display for hover effects
            mouse_pos = pygame.mouse.get_pos()
            redraw_needed = False
            
            # Check if any button state has changed
            for i, (text, color, mode) in enumerate(options):
                button_rect = button_rects[i][0]
                is_hovering = button_rect.collidepoint(mouse_pos)
                if is_hovering:
                    redraw_needed = True
                    break
            
            # Only redraw if needed
            if redraw_needed:
                self.screen.fill(DEEP_BLUE)
                self.screen.blit(title_text, title_rect)
                
                for i, (text, color, mode) in enumerate(options):
                    option_text = menu_font.render(text, True, color)
                    option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 70 * i))
                    
                    button_rect = option_rect.copy()
                    button_rect.inflate_ip(40, 20)
                    
                    is_hovering = button_rect.collidepoint(mouse_pos)
                    
                    if is_hovering:
                        hover_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
                        pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                        pygame.draw.rect(self.screen, hover_color, button_rect, 2, border_radius=10)
                        option_text = menu_font.render(text, True, hover_color)
                    else:
                        pygame.draw.rect(self.screen, DEEP_BLUE, button_rect, border_radius=10)
                        pygame.draw.rect(self.screen, color, button_rect, 2, border_radius=10)
                    
                    self.screen.blit(option_text, option_rect)
                
                pygame.display.flip()
            
            clock.tick(30)
        
        return False
    def update(self):
        if self.game_over:
            return
            
        # Calculate delta time
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Update player car
        self.player_car.update(dt)
        
        # Update particle system
        self.particle_system.update(dt)
        
        # Create tire smoke if car is turning
        if self.player_car.tire_smoke_cooldown > 0:
            # Create smoke at each wheel position
            wheel_positions = [
                (self.player_car.x - self.player_car.width // 2 + 5, self.player_car.y - self.player_car.height // 4),
                (self.player_car.x + self.player_car.width // 2 - 5, self.player_car.y - self.player_car.height // 4),
                (self.player_car.x - self.player_car.width // 2 + 5, self.player_car.y + self.player_car.height // 4),
                (self.player_car.x + self.player_car.width // 2 - 5, self.player_car.y + self.player_car.height // 4)
            ]
            
            for pos in wheel_positions:
                if random.random() < 0.3:  # Only create smoke sometimes for a more natural effect
                    self.particle_system.create_smoke(pos[0], pos[1], count=1)
        
        # Create boost trail if boosting
        if self.player_car.is_boosting and random.random() < 0.5:
            boost_x = self.player_car.x
            boost_y = self.player_car.y + self.player_car.height // 2
            self.particle_system.create_boost_trail(boost_x, boost_y)
        
        # Apply slow motion if active
        speed_factor = SLOW_MO_FACTOR if self.player_car.has_slow_mo else 1.0
        
        # Apply boost if active
        if self.player_car.has_boost:
            speed_factor *= BOOST_MULTIPLIER
        
        # Increase speed over time
        self.speed += SPEED_INCREMENT * speed_factor
        
        # Cap speed at 15 (which will display as 150 km/h)
        if self.speed > 15:
            self.speed = 15
            
        # Update distance traveled
        self.distance_traveled += self.speed * dt * 10  # 10 meters per unit of speed
        
        # Update time remaining for time attack mode
        if self.game_mode == GAME_MODE_TIME_ATTACK:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.game_over = True
        
        # Update mission progress
        self.update_mission_progress()
        
        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo_count = 0
                self.score_multiplier = 1
        
        # Generate new obstacles
        if current_time - self.last_obstacle_time > random.uniform(1.0, 3.0):
            lane = random.randint(0, 5)  # Changed from 0-3 to 0-5 for 6 lanes
            # Sometimes create moving obstacles
            if random.random() < 0.3:
                self.obstacles.append(MovingObstacle(lane))
            else:
                self.obstacles.append(Obstacle(lane))
            self.last_obstacle_time = current_time
        
        # Generate other cars
        if current_time - self.last_car_time > random.uniform(2.0, 5.0):
            lane = random.randint(0, 5)  # Changed from 0-3 to 0-5 for 6 lanes
            # Sometimes create AI-controlled cars
            if random.random() < 0.5:
                self.other_cars.append(AIControlledCar(lane))
            else:
                self.other_cars.append(OtherCar(lane))
            self.last_car_time = current_time
        
        # Generate new power-ups
        if current_time - self.last_powerup_time > random.uniform(5.0, 15.0):
            lane = random.randint(0, 5)  # Changed from 0-3 to 0-5 for 6 lanes
            powerup_type = random.choice(['boost', 'shield', 'magnet', 'slow_mo'])
            self.powerups.append(PowerUp(lane, powerup_type))
            self.last_powerup_time = current_time
        
        # Generate new coins
        if current_time - self.last_coin_time > random.uniform(0.5, 2.0):
            lane = random.randint(0, 5)  # Changed from 0-3 to 0-5 for 6 lanes
            x = LANE_POSITIONS[lane] + random.randint(-LANE_WIDTH//4, LANE_WIDTH//4)
            self.coins.append(Coin(x, -20))
            self.last_coin_time = current_time
        
        # Update moving obstacles
        for obstacle in self.obstacles[:]:
            if isinstance(obstacle, MovingObstacle):
                obstacle.update(dt)
        
        # Update AI cars
        for car in self.other_cars[:]:
            if isinstance(car, AIControlledCar):
                car.update(dt, self.player_car.lane, self.obstacles)
        
        # Move obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move(self.speed * speed_factor)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 1
                # Add to combo for avoiding obstacle
                self.combo_count += 1
                self.combo_timer = 2.0
                # Update score multiplier
                if self.combo_count >= 10:
                    self.score_multiplier = 3
                elif self.combo_count >= 5:
                    self.score_multiplier = 2
            elif obstacle.collides_with(self.player_car):
                if self.player_car.has_shield:
                    # Shield protects from collision
                    self.obstacles.remove(obstacle)
                    self.score += 2
                    # Add to combo
                    self.combo_count += 2
                    self.combo_timer = 2.0
                    # Create spark effect for shield collision
                    self.particle_system.create_spark(obstacle.x, obstacle.y, count=15)
                else:
                    # Create crash effect
                    self.particle_system.create_crash(self.player_car.x, self.player_car.y)
                    self.game_over = True
        
        # Move other cars
        for car in self.other_cars[:]:
            # Apply braking for AI cars
            speed_modifier = 0.5 if isinstance(car, AIControlledCar) and car.is_braking else 0.8
            car.move(self.speed * speed_factor * speed_modifier)
            
            if car.is_off_screen():
                self.other_cars.remove(car)
                self.score += 2 * self.score_multiplier
                # Add to combo
                self.combo_count += 1
                self.combo_timer = 2.0
            elif car.collides_with(self.player_car):
                if self.player_car.has_shield:
                    # Shield protects from collision
                    self.other_cars.remove(car)
                    self.score += 3
                    # Add to combo
                    self.combo_count += 2
                    self.combo_timer = 2.0
                    # Create spark effect for shield collision
                    self.particle_system.create_spark(car.x, car.y, count=20)
                else:
                    # Create crash effect
                    self.particle_system.create_crash(self.player_car.x, self.player_car.y)
                    self.game_over = True
        
        # Move and check power-ups
        for powerup in self.powerups[:]:
            powerup.move(self.speed * speed_factor)
            if powerup.is_off_screen():
                self.powerups.remove(powerup)
            elif powerup.collides_with(self.player_car):
                powerup.collect()
                self.powerups.remove(powerup)
                
                # Apply power-up effect
                if powerup.type == 'boost':
                    self.player_car.activate_boost()
                    # Create spark effect for boost activation
                    self.particle_system.create_spark(self.player_car.x, self.player_car.y + self.player_car.height // 2, count=15)
                elif powerup.type == 'shield':
                    self.player_car.activate_shield()
                elif powerup.type == 'magnet':
                    self.player_car.activate_magnet()
                elif powerup.type == 'slow_mo':
                    self.player_car.activate_slow_mo()
                
                # Add points for collecting power-up
                self.score += 5 * self.score_multiplier
                # Add to combo
                self.combo_count += 1
                self.combo_timer = 2.0
                # Track power-ups used for missions
                self.powerups_used += 1
        
        # Move and check coins
        for coin in self.coins[:]:
            coin.move(self.speed * speed_factor)
            
            # Check if coin is in magnet range
            if self.player_car.has_magnet:
                dx = self.player_car.x - coin.x
                dy = self.player_car.y - coin.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < MAGNET_RANGE:
                    # Move coin towards player
                    angle = math.atan2(dy, dx)
                    coin.x += math.cos(angle) * 5
                    coin.y += math.sin(angle) * 5
            
            if coin.is_off_screen():
                self.coins.remove(coin)
            elif coin.collides_with(self.player_car):
                coin.collect()
                self.coins.remove(coin)
                self.coins_collected += 1
                
                # Create spark effect for coin collection
                self.particle_system.create_spark(coin.x, coin.y, count=5)
                
                # Add points for collecting coin with combo multiplier
                self.score += COIN_VALUE * self.score_multiplier
                
                # Increase combo
                self.combo_count += 1
                self.combo_timer = 2.0  # Reset combo timer
                
                # Update score multiplier
                if self.combo_count >= 10:
                    self.score_multiplier = 3
                elif self.combo_count >= 5:
                    self.score_multiplier = 2
                else:
                    self.score_multiplier = 1
                    
                # Add boost energy
                self.player_car.add_boost_energy(5)
