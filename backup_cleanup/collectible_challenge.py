#!/usr/bin/env python3
import pygame
import random
import sys
import time
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game settings
LANE_WIDTH = SCREEN_WIDTH // 4
LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(4)]
CAR_WIDTH = 60
CAR_HEIGHT = 100
INITIAL_SPEED = 5
COLLECTIBLE_SIZE = 30

# Challenge settings
CHALLENGE_TIME = 30  # seconds
COLLECTIBLES_TO_COLLECT = 10

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collect N Objects Challenge")
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Collectible types
COLLECTIBLE_TYPES = {
    'fuel': {'color': RED, 'points': 1, 'image': None},
    'coin': {'color': YELLOW, 'points': 2, 'image': None},
    'star': {'color': BLUE, 'points': 3, 'image': None}
}

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([CAR_WIDTH, CAR_HEIGHT])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (LANE_POSITIONS[1], SCREEN_HEIGHT - 100)
        self.lane = 1
        self.speed = INITIAL_SPEED
        
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.rect.centerx = LANE_POSITIONS[self.lane]
            
    def move_right(self):
        if self.lane < 3:
            self.lane += 1
            self.rect.centerx = LANE_POSITIONS[self.lane]
            
    def update(self):
        # Any continuous updates to the car can go here
        pass
        
    def draw(self, surface):
        # Draw car body
        pygame.draw.rect(surface, GREEN, self.rect)
        
        # Draw windshield
        windshield_width = int(self.rect.width * 0.8)
        windshield_height = int(self.rect.height * 0.3)
        windshield_x = self.rect.centerx - windshield_width // 2
        windshield_y = self.rect.top + int(self.rect.height * 0.15)
        pygame.draw.rect(
            surface,
            (100, 200, 255),
            [windshield_x, windshield_y, windshield_width, windshield_height],
            0,
            5
        )
        
        # Draw wheels
        wheel_width = int(self.rect.width * 0.25)
        wheel_height = int(self.rect.height * 0.15)
        
        # Front left wheel
        pygame.draw.rect(
            surface,
            BLACK,
            [
                self.rect.left - 3,
                self.rect.centery - self.rect.height // 4,
                wheel_width,
                wheel_height
            ],
            0,
            3
        )
        
        # Front right wheel
        pygame.draw.rect(
            surface,
            BLACK,
            [
                self.rect.right - wheel_width + 3,
                self.rect.centery - self.rect.height // 4,
                wheel_width,
                wheel_height
            ],
            0,
            3
        )
        
        # Rear left wheel
        pygame.draw.rect(
            surface,
            BLACK,
            [
                self.rect.left - 3,
                self.rect.centery + self.rect.height // 4 - wheel_height,
                wheel_width,
                wheel_height
            ],
            0,
            3
        )
        
        # Rear right wheel
        pygame.draw.rect(
            surface,
            BLACK,
            [
                self.rect.right - wheel_width + 3,
                self.rect.centery + self.rect.height // 4 - wheel_height,
                wheel_width,
                wheel_height
            ],
            0,
            3
        )

class Collectible(pygame.sprite.Sprite):
    def __init__(self, collectible_type):
        super().__init__()
        self.type = collectible_type
        self.info = COLLECTIBLE_TYPES[collectible_type]
        
        # Create the collectible image
        self.image = pygame.Surface([COLLECTIBLE_SIZE, COLLECTIBLE_SIZE], pygame.SRCALPHA)
        
        if self.type == 'fuel':
            # Draw a fuel can
            pygame.draw.rect(self.image, self.info['color'], 
                            [5, 0, COLLECTIBLE_SIZE-10, COLLECTIBLE_SIZE-5], 0, 3)
            pygame.draw.rect(self.image, self.info['color'], 
                            [COLLECTIBLE_SIZE//3, -5, COLLECTIBLE_SIZE//3, 10], 0)
        elif self.type == 'coin':
            # Draw a coin
            pygame.draw.circle(self.image, self.info['color'], 
                              (COLLECTIBLE_SIZE//2, COLLECTIBLE_SIZE//2), COLLECTIBLE_SIZE//2-2)
            pygame.draw.circle(self.image, ORANGE, 
                              (COLLECTIBLE_SIZE//2, COLLECTIBLE_SIZE//2), COLLECTIBLE_SIZE//2-5)
        elif self.type == 'star':
            # Draw a star
            points = []
            for i in range(5):
                # Outer point
                angle = math.pi/2 + i * 2*math.pi/5
                x = COLLECTIBLE_SIZE//2 + int((COLLECTIBLE_SIZE//2-2) * math.cos(angle))
                y = COLLECTIBLE_SIZE//2 + int((COLLECTIBLE_SIZE//2-2) * math.sin(angle))
                points.append((x, y))
                
                # Inner point
                angle += math.pi/5
                x = COLLECTIBLE_SIZE//2 + int((COLLECTIBLE_SIZE//4) * math.cos(angle))
                y = COLLECTIBLE_SIZE//2 + int((COLLECTIBLE_SIZE//4) * math.sin(angle))
                points.append((x, y))
            
            pygame.draw.polygon(self.image, self.info['color'], points)
        
        self.rect = self.image.get_rect()
        
        # Position the collectible in a random lane
        lane = random.randint(0, 3)
        self.rect.centerx = LANE_POSITIONS[lane]
        self.rect.centery = -COLLECTIBLE_SIZE  # Start above the screen
        
    def update(self, speed):
        self.rect.y += speed
        
        # Remove if it goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def draw_road():
    # Fill background
    screen.fill((50, 50, 50))  # Dark gray road
    
    # Draw lane markings
    for i in range(5):  # 5 lines for 4 lanes
        x = i * LANE_WIDTH
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT), 3)
    
    # Draw dashed lines in the middle of lanes
    for i in range(1, 4):  # 3 dashed lines
        x = i * LANE_WIDTH
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(screen, WHITE, (x, y), (x, y + 20), 2)

def show_message(message, color=WHITE, y_offset=0):
    text = large_font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
    
    # Add a semi-transparent background
    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(20, 20)
    bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 180))
    screen.blit(bg_surface, bg_rect)
    
    screen.blit(text, text_rect)

def run_challenge():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    
    # Create player car
    player = Car()
    all_sprites.add(player)
    
    # Game variables
    running = True
    game_over = False
    start_time = time.time()
    collected = 0
    spawn_timer = 0
    
    while running:
        # Calculate elapsed time
        current_time = time.time()
        elapsed = current_time - start_time
        remaining_time = max(0, CHALLENGE_TIME - elapsed)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit the game
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True  # Return to main menu
                
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
                else:
                    if event.key == pygame.K_RETURN:
                        return True  # Return to main menu
        
        # Game logic (only if game is not over)
        if not game_over:
            # Spawn new collectibles
            spawn_timer += 1
            if spawn_timer >= 30 and len(collectibles) < 5:  # Limit number of collectibles on screen
                collectible_type = random.choice(list(COLLECTIBLE_TYPES.keys()))
                new_collectible = Collectible(collectible_type)
                collectibles.add(new_collectible)
                all_sprites.add(new_collectible)
                spawn_timer = 0
            
            # Update collectibles
            for collectible in collectibles:
                collectible.update(player.speed)
            
            # Check for collisions
            hits = pygame.sprite.spritecollide(player, collectibles, True)
            for hit in hits:
                collected += hit.info['points']
                
                # Create a brief visual effect for collection
                pygame.draw.circle(screen, hit.info['color'], 
                                  player.rect.center, 30, 3)
                pygame.display.flip()
                
                # Check if challenge is complete
                if collected >= COLLECTIBLES_TO_COLLECT:
                    game_over = True
                    result = "SUCCESS!"
            
            # Check if time is up
            if remaining_time <= 0 and not game_over:
                game_over = True
                result = "FAILED!"
        
        # Drawing
        draw_road()
        
        # Draw all sprites
        for sprite in all_sprites:
            if isinstance(sprite, Car):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)
        
        # Draw HUD
        # Time remaining
        time_text = font.render(f"Time: {int(remaining_time)}s", True, WHITE)
        screen.blit(time_text, (10, 10))
        
        # Collection progress
        progress_text = font.render(f"Collected: {collected}/{COLLECTIBLES_TO_COLLECT}", True, WHITE)
        screen.blit(progress_text, (10, 50))
        
        # Draw progress bar
        progress_width = 200
        progress_height = 20
        progress_x = SCREEN_WIDTH - progress_width - 10
        progress_y = 10
        
        # Background bar
        pygame.draw.rect(screen, (50, 50, 50), (progress_x, progress_y, progress_width, progress_height), 0, 5)
        
        # Fill based on progress
        fill_width = int(progress_width * (collected / COLLECTIBLES_TO_COLLECT))
        pygame.draw.rect(screen, GREEN, (progress_x, progress_y, fill_width, progress_height), 0, 5)
        
        # Border
        pygame.draw.rect(screen, WHITE, (progress_x, progress_y, progress_width, progress_height), 2, 5)
        
        # Show game over message if applicable
        if game_over:
            if result == "SUCCESS!":
                show_message(result, GREEN)
                show_message("Challenge Complete!", GREEN, 70)
            else:
                show_message(result, RED)
                show_message("Try Again!", RED, 70)
            
            # Show press enter message
            press_enter = font.render("Press ENTER to continue", True, WHITE)
            press_enter_rect = press_enter.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 140))
            screen.blit(press_enter, press_enter_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return True

def main():
    # Main game loop
    while True:
        if not run_challenge():
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
