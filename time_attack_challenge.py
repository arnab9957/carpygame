#!/usr/bin/env python3
"""
Time Attack Challenge Module for Car Racing Game
Implements "Collect N Objects Within Time" challenge
"""
import pygame
import random
import math
import time
from typing import List, Dict, Any, Tuple, Optional

# Define collectible types with their properties
COLLECTIBLE_TYPES = {
    'fuel': {
        'color': (255, 0, 0),  # Red
        'points': 1,
        'name': 'Fuel Can',
        'spawn_weight': 5,  # Higher weight = more common
    },
    'coin': {
        'color': (255, 223, 0),  # Gold
        'points': 2,
        'name': 'Coin',
        'spawn_weight': 3,
    },
    'star': {
        'color': (0, 191, 255),  # Light blue
        'points': 3,
        'name': 'Star',
        'spawn_weight': 1,  # Rarest
    }
}

class CollectibleSprite(pygame.sprite.Sprite):
    """Sprite class for collectible objects in the challenge"""
    
    def __init__(self, collectible_type: str, x: int, y: int, size: int = 30):
        super().__init__()
        self.type = collectible_type
        self.info = COLLECTIBLE_TYPES[collectible_type]
        self.size = size
        self.pulse_effect = random.random() * 2 * math.pi  # Random start phase for pulsing
        
        # Create the collectible image
        self.image = pygame.Surface([size, size], pygame.SRCALPHA)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        # Draw the collectible based on its type
        self._draw_collectible()
    
    def _draw_collectible(self):
        """Draw the collectible based on its type"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparency
        
        if self.type == 'fuel':
            # Draw a fuel can
            pygame.draw.rect(
                self.image, 
                self.info['color'], 
                [5, 0, self.size-10, self.size-5], 
                0, 3
            )
            pygame.draw.rect(
                self.image, 
                self.info['color'], 
                [self.size//3, -5, self.size//3, 10], 
                0
            )
            
            # Add highlight
            pygame.draw.rect(
                self.image, 
                (255, 255, 255, 100), 
                [7, 2, self.size//3, self.size-9], 
                0, 2
            )
            
        elif self.type == 'coin':
            # Draw a coin with gradient
            pygame.draw.circle(
                self.image, 
                self.info['color'], 
                (self.size//2, self.size//2), 
                self.size//2-2
            )
            
            # Inner circle for 3D effect
            pygame.draw.circle(
                self.image, 
                (255, 200, 0), 
                (self.size//2, self.size//2), 
                self.size//2-5
            )
            
            # Highlight
            pygame.draw.circle(
                self.image, 
                (255, 255, 200), 
                (self.size//2 - 3, self.size//2 - 3), 
                self.size//6
            )
            
        elif self.type == 'star':
            # Draw a star
            points = []
            for i in range(5):
                # Outer point
                angle = math.pi/2 + i * 2*math.pi/5
                x = self.size//2 + int((self.size//2-2) * math.cos(angle))
                y = self.size//2 + int((self.size//2-2) * math.sin(angle))
                points.append((x, y))
                
                # Inner point
                angle += math.pi/5
                x = self.size//2 + int((self.size//4) * math.cos(angle))
                y = self.size//2 + int((self.size//4) * math.sin(angle))
                points.append((x, y))
            
            pygame.draw.polygon(self.image, self.info['color'], points)
            
            # Add glow effect
            for offset in range(3, 0, -1):
                glow_points = []
                for x, y in points:
                    glow_x = self.size//2 + (x - self.size//2) * (1 + offset * 0.1)
                    glow_y = self.size//2 + (y - self.size//2) * (1 + offset * 0.1)
                    glow_points.append((glow_x, glow_y))
                
                pygame.draw.polygon(
                    self.image, 
                    (*self.info['color'], 50), 
                    glow_points
                )
        
        # Store the original image for rotation/scaling
        self.original_image = self.image.copy()
    
    def update(self, speed: float, dt: float = 1/60):
        """Update the collectible position and animation"""
        # Move down the screen
        self.rect.y += speed * dt * 60  # Scale by dt for frame rate independence
        
        # Animate the collectible
        self.pulse_effect = (self.pulse_effect + 0.1) % (2 * math.pi)
        pulse_scale = 1.0 + 0.1 * math.sin(self.pulse_effect)
        
        # Scale the image for pulsing effect
        new_size = int(self.size * pulse_scale)
        self.image = pygame.transform.scale(
            self.original_image, 
            (new_size, new_size)
        )
        
        # Keep the center position
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        
        # Rotate star collectibles
        if self.type == 'star':
            self.image = pygame.transform.rotate(
                self.image, 
                (pygame.time.get_ticks() // 20) % 360
            )
            self.rect = self.image.get_rect(center=old_center)

class TimeAttackChallenge:
    """Implements a time-limited collection challenge"""
    
    def __init__(self, game_instance):
        self.game = game_instance
        self.screen = game_instance.screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        # Challenge settings
        self.challenge_time = 30  # seconds
        self.collectibles_required = 15
        self.difficulty_level = 1  # 1=easy, 2=medium, 3=hard
        
        # Sprite groups
        self.collectibles = pygame.sprite.Group()
        
        # Challenge state
        self.start_time = 0
        self.collected = 0
        self.active = False
        self.completed = False
        self.success = False
        self.spawn_timer = 0
        
        # Load fonts
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        # Sound effects
        self.collect_sound = None
        self.success_sound = None
        self.fail_sound = None
        
        # Try to load sounds if available
        try:
            if pygame.mixer.get_init():
                self.collect_sound = pygame.mixer.Sound("sounds/coin.wav")
                self.success_sound = pygame.mixer.Sound("sounds/powerup.wav")
                self.fail_sound = pygame.mixer.Sound("sounds/crash.wav")
        except:
            print("Could not load challenge sounds")
    
    def start(self, difficulty: int = 1):
        """Start a new challenge with the given difficulty"""
        self.difficulty_level = max(1, min(3, difficulty))  # Clamp between 1-3
        
        # Set challenge parameters based on difficulty
        if self.difficulty_level == 1:  # Easy
            self.challenge_time = 40
            self.collectibles_required = 10
        elif self.difficulty_level == 2:  # Medium
            self.challenge_time = 30
            self.collectibles_required = 15
        else:  # Hard
            self.challenge_time = 25
            self.collectibles_required = 20
        
        # Reset challenge state
        self.collectibles.empty()
        self.start_time = time.time()
        self.collected = 0
        self.active = True
        self.completed = False
        self.success = False
        self.spawn_timer = 0
        
        # Initial collectibles
        for _ in range(3):
            self._spawn_collectible()
    
    def _spawn_collectible(self):
        """Spawn a new collectible at a random position"""
        # Determine which lane to spawn in
        lane = random.randint(0, len(self.game.LANE_POSITIONS) - 1)
        x = self.game.LANE_POSITIONS[lane]
        
        # Randomize y position above the screen
        y = random.randint(-100, -30)
        
        # Choose collectible type based on weights
        types = []
        weights = []
        for ctype, info in COLLECTIBLE_TYPES.items():
            types.append(ctype)
            weights.append(info['spawn_weight'])
        
        collectible_type = random.choices(types, weights=weights, k=1)[0]
        
        # Create and add the collectible
        new_collectible = CollectibleSprite(collectible_type, x, y)
        self.collectibles.add(new_collectible)
    
    def update(self, player_car, dt: float = 1/60):
        """Update the challenge state"""
        if not self.active:
            return
        
        # Calculate elapsed time
        current_time = time.time()
        elapsed = current_time - self.start_time
        remaining_time = max(0, self.challenge_time - elapsed)
        
        # Check if time is up
        if remaining_time <= 0 and not self.completed:
            self.completed = True
            self.active = False
            self.success = (self.collected >= self.collectibles_required)
            
            # Play appropriate sound
            if self.success and self.success_sound:
                self.success_sound.play()
            elif not self.success and self.fail_sound:
                self.fail_sound.play()
            
            return
        
        # Spawn new collectibles
        self.spawn_timer += dt
        spawn_interval = 1.0  # seconds between spawns
        
        # Adjust spawn rate based on difficulty
        if self.difficulty_level == 1:
            max_collectibles = 5
            spawn_interval = 1.2
        elif self.difficulty_level == 2:
            max_collectibles = 4
            spawn_interval = 1.0
        else:
            max_collectibles = 3
            spawn_interval = 0.8
        
        if self.spawn_timer >= spawn_interval and len(self.collectibles) < max_collectibles:
            self._spawn_collectible()
            self.spawn_timer = 0
        
        # Update collectibles
        game_speed = player_car.speed
        if hasattr(player_car, 'has_boost') and player_car.has_boost:
            game_speed *= 1.8  # Match the BOOST_MULTIPLIER from the main game
            
        for collectible in self.collectibles:
            collectible.update(game_speed, dt)
            
            # Remove if it goes off screen
            if collectible.rect.top > self.screen_height:
                collectible.kill()
        
        # Check for collisions with player car
        if hasattr(player_car, 'rect'):
            hits = pygame.sprite.spritecollide(player_car, self.collectibles, True)
            for hit in hits:
                self.collected += hit.info['points']
                
                # Play collect sound
                if self.collect_sound:
                    self.collect_sound.play()
                
                # Check if challenge is complete
                if self.collected >= self.collectibles_required:
                    self.completed = True
                    self.active = False
                    self.success = True
                    
                    # Play success sound
                    if self.success_sound:
                        self.success_sound.play()
    
    def draw(self, screen):
        """Draw the challenge elements"""
        # Draw all collectibles
        self.collectibles.draw(screen)
        
        # Draw HUD elements
        if self.active or self.completed:
            # Calculate remaining time
            if self.active:
                current_time = time.time()
                elapsed = current_time - self.start_time
                remaining_time = max(0, self.challenge_time - elapsed)
            else:
                remaining_time = 0
            
            # Draw time remaining
            time_color = (255, 255, 255)
            if remaining_time < 5:  # Flash red when time is running out
                if int(remaining_time * 2) % 2 == 0:
                    time_color = (255, 50, 50)
            
            time_text = self.font.render(f"Time: {int(remaining_time)}s", True, time_color)
            screen.blit(time_text, (10, 10))
            
            # Draw collection progress
            progress_text = self.font.render(
                f"Collected: {self.collected}/{self.collectibles_required}", 
                True, (255, 255, 255)
            )
            screen.blit(progress_text, (10, 50))
            
            # Draw progress bar
            progress_width = 200
            progress_height = 20
            progress_x = self.screen_width - progress_width - 10
            progress_y = 10
            
            # Background bar
            pygame.draw.rect(
                screen, 
                (50, 50, 50), 
                (progress_x, progress_y, progress_width, progress_height), 
                0, 5
            )
            
            # Fill based on progress
            fill_width = int(progress_width * (self.collected / self.collectibles_required))
            fill_color = (0, 255, 0)  # Green
            
            # Change color based on progress
            if self.collected / self.collectibles_required < 0.5:
                fill_color = (255, 165, 0)  # Orange
            
            pygame.draw.rect(
                screen, 
                fill_color, 
                (progress_x, progress_y, fill_width, progress_height), 
                0, 5
            )
            
            # Border
            pygame.draw.rect(
                screen, 
                (255, 255, 255), 
                (progress_x, progress_y, progress_width, progress_height), 
                2, 5
            )
        
        # Draw completion message if challenge is completed
        if self.completed:
            self._draw_completion_message(screen)
    
    def _draw_completion_message(self, screen):
        """Draw the challenge completion message"""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Draw result message
        if self.success:
            result_text = self.large_font.render("SUCCESS!", True, (0, 255, 0))
            sub_text = self.font.render(
                f"Collected {self.collected} out of {self.collectibles_required} required items", 
                True, (255, 255, 255)
            )
        else:
            result_text = self.large_font.render("FAILED!", True, (255, 50, 50))
            sub_text = self.font.render(
                f"Collected only {self.collected} out of {self.collectibles_required} required items", 
                True, (255, 255, 255)
            )
        
        # Position and draw the text
        result_rect = result_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 40))
        sub_rect = sub_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 20))
        
        screen.blit(result_text, result_rect)
        screen.blit(sub_text, sub_rect)
        
        # Draw continue message
        continue_text = self.font.render("Press ENTER to continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 80))
        
        # Make it pulse
        if int(time.time() * 2) % 2 == 0:
            screen.blit(continue_text, continue_rect)
    
    def handle_event(self, event):
        """Handle events for the challenge"""
        if self.completed and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return True  # Signal that the challenge is done
        return False

# Example of how to integrate this with the main game:
"""
# In the main game class:
from time_attack_challenge import TimeAttackChallenge

class Game:
    def __init__(self):
        # ... existing initialization ...
        self.time_attack_challenge = TimeAttackChallenge(self)
        
    def start_time_attack_challenge(self, difficulty=1):
        self.time_attack_challenge.start(difficulty)
        
    def update(self):
        # ... existing update code ...
        
        # Update challenge if active
        if self.time_attack_challenge.active or self.time_attack_challenge.completed:
            self.time_attack_challenge.update(self.player_car, dt)
            
            # Handle challenge completion
            if self.time_attack_challenge.completed:
                if self.time_attack_challenge.success:
                    # Award points, unlock features, etc.
                    self.score += 1000
                    
    def draw(self):
        # ... existing drawing code ...
        
        # Draw challenge elements
        if self.time_attack_challenge.active or self.time_attack_challenge.completed:
            self.time_attack_challenge.draw(self.screen)
            
    def handle_events(self):
        # ... existing event handling ...
        
        # Handle challenge events
        if self.time_attack_challenge.completed:
            if self.time_attack_challenge.handle_event(event):
                # Challenge is done, return to normal gameplay
                self.game_mode = GAME_MODE_ENDLESS  # or whatever is appropriate
"""
