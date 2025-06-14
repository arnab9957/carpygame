#!/usr/bin/env python3
"""
Simplified car racing game with color selection
"""
import pygame
import sys
import random
import time
import math

# Initialize pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing - Color Selection")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)

# Car colors
CAR_COLORS = [
    {"name": "RED RACER", "color": RED, "description": "Fast and agile sports car"},
    {"name": "BLUE BOLT", "color": BLUE, "description": "Powerful sports car with high top speed"},
    {"name": "GREEN MACHINE", "color": GREEN, "description": "Nimble sports car with excellent handling"},
    {"name": "YELLOW FLASH", "color": YELLOW, "description": "Well-balanced sports car"},
    {"name": "PURPLE PHANTOM", "color": PURPLE, "description": "Premium sports car"}
]

# Game variables
selected_car = 0
clock = pygame.time.Clock()
font_large = pygame.font.SysFont('arial', 48, bold=True)
font_medium = pygame.font.SysFont('arial', 36)
font_small = pygame.font.SysFont('arial', 24)

def draw_car(surface, color, x, y, width, height):
    """Draw a car with the specified color"""
    # Car body
    pygame.draw.rect(surface, color, [x - width//2, y - height//2, width, height], 0, 10)
    
    # Windshield
    windshield_width = int(width * 0.8)
    windshield_height = int(height * 0.3)
    windshield_x = x - windshield_width // 2
    windshield_y = y - height // 2 + int(height * 0.15)
    pygame.draw.rect(surface, (100, 200, 255), [windshield_x, windshield_y, windshield_width, windshield_height], 0, 5)
    
    # Wheels
    wheel_width = int(width * 0.25)
    wheel_height = int(height * 0.15)
    
    # Front left wheel
    pygame.draw.rect(surface, BLACK, [x - width//2 - 3, y - height//4, wheel_width, wheel_height], 0, 3)
    
    # Front right wheel
    pygame.draw.rect(surface, BLACK, [x + width//2 - wheel_width + 3, y - height//4, wheel_width, wheel_height], 0, 3)
    
    # Rear left wheel
    pygame.draw.rect(surface, BLACK, [x - width//2 - 3, y + height//4 - wheel_height, wheel_width, wheel_height], 0, 3)
    
    # Rear right wheel
    pygame.draw.rect(surface, BLACK, [x + width//2 - wheel_width + 3, y + height//4 - wheel_height, wheel_width, wheel_height], 0, 3)
    
    # Headlights
    headlight_width = int(width * 0.15)
    headlight_height = int(height * 0.08)
    
    # Left headlight
    pygame.draw.rect(surface, YELLOW, [x - width//2 + 5, y - height//2 + 5, headlight_width, headlight_height], 0, 3)
    
    # Right headlight
    pygame.draw.rect(surface, YELLOW, [x + width//2 - headlight_width - 5, y - height//2 + 5, headlight_width, headlight_height], 0, 3)

def show_garage():
    """Show the garage screen for car selection"""
    global selected_car
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    selected_car = (selected_car - 1) % len(CAR_COLORS)
                elif event.key == pygame.K_RIGHT:
                    selected_car = (selected_car + 1) % len(CAR_COLORS)
                elif event.key == pygame.K_RETURN:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for button clicks
                pass
        
        # Draw background
        screen.fill(GRAY)
        
        # Draw title
        title_text = font_large.render("GARAGE", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw car
        car_color = CAR_COLORS[selected_car]["color"]
        draw_car(screen, car_color, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50, 200, 100)
        
        # Draw car name
        name_text = font_medium.render(CAR_COLORS[selected_car]["name"], True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
        
        # Draw car description
        desc_text = font_small.render(CAR_COLORS[selected_car]["description"], True, WHITE)
        screen.blit(desc_text, (SCREEN_WIDTH//2 - desc_text.get_width()//2, SCREEN_HEIGHT//2 + 130))
        
        # Draw navigation arrows
        left_arrow = font_large.render("<", True, WHITE)
        screen.blit(left_arrow, (SCREEN_WIDTH//4, SCREEN_HEIGHT//2 - 50))
        
        right_arrow = font_large.render(">", True, WHITE)
        screen.blit(right_arrow, (3*SCREEN_WIDTH//4 - right_arrow.get_width(), SCREEN_HEIGHT//2 - 50))
        
        # Draw instructions
        instructions = font_small.render("LEFT/RIGHT: Change Car | ENTER: Select | ESC: Back", True, WHITE)
        screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, SCREEN_HEIGHT - 50))
        
        # Update display
        pygame.display.flip()
        clock.tick(30)
    
    return selected_car

def game_loop():
    """Main game loop"""
    global selected_car
    
    # Game variables
    car_x = SCREEN_WIDTH // 2
    car_y = SCREEN_HEIGHT - 100
    car_width = 60
    car_height = 120
    car_speed = 5
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_g:
                    # Go to garage
                    selected_car = show_garage()
        
        # Get key states for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x = max(car_width//2, car_x - car_speed)
        if keys[pygame.K_RIGHT]:
            car_x = min(SCREEN_WIDTH - car_width//2, car_x + car_speed)
        
        # Draw background
        screen.fill((50, 50, 50))  # Dark gray road
        
        # Draw road lines
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, [SCREEN_WIDTH//2 - 5, y, 10, 20])
        
        # Draw car with selected color
        car_color = CAR_COLORS[selected_car]["color"]
        draw_car(screen, car_color, car_x, car_y, car_width, car_height)
        
        # Draw HUD
        car_name = font_small.render(f"Car: {CAR_COLORS[selected_car]['name']}", True, WHITE)
        screen.blit(car_name, (10, 10))
        
        instructions = font_small.render("Press G to change car", True, WHITE)
        screen.blit(instructions, (10, 40))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)

# Start with garage to select car
selected_car = show_garage()

# Start game loop
game_loop()

# Clean up
pygame.quit()
sys.exit()
