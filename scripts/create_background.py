#!/usr/bin/env python3
"""
Background Creation Script for Car Racing Game
Creates the main background image with horizontal roads, buildings, trees, and sea.
"""
import pygame
import random
import math
import os

# Initialize pygame
pygame.init()

# Create assets/images directory if it doesn't exist
os.makedirs('../assets/images', exist_ok=True)

# Create a 1920x1080 background image
width, height = 1920, 1080
surface = pygame.Surface((width, height))

# Create gradient background (night sky)
for y in range(height):
    ratio = y / height
    r = int(15 + (50 - 15) * ratio)
    g = int(20 + (70 - 20) * ratio)  
    b = int(35 + (110 - 35) * ratio)
    pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

# Add stars for night racing feel
random.seed(42)
for _ in range(200):
    x = random.randint(0, width)
    y = random.randint(0, height//2)
    size = random.randint(1, 3)
    brightness = random.randint(150, 255)
    pygame.draw.circle(surface, (brightness, brightness, 255), (x, y), size)

# Function to draw buildings and houses
def draw_house(surf, x, y, house_width, house_height, house_color, roof_color):
    pygame.draw.rect(surf, house_color, (x, y, house_width, house_height))
    roof_points = [(x, y), (x + house_width, y), (x + house_width // 2, y - house_height // 3)]
    pygame.draw.polygon(surf, roof_color, roof_points)
    
    # Windows
    window_size = house_width // 6
    window_color = (255, 255, 150)
    pygame.draw.rect(surf, window_color, (x + house_width // 6, y + house_height // 4, window_size, window_size))
    pygame.draw.rect(surf, window_color, (x + 4 * house_width // 6, y + house_height // 4, window_size, window_size))

# Add background buildings
horizon_y = height * 0.35
for i in range(20):
    x = random.randint(0, width - 60)
    y = random.randint(int(horizon_y), int(horizon_y + 100))
    house_width = random.randint(25, 45)
    house_height = random.randint(20, 35)
    
    house_colors = [(50, 50, 70), (60, 50, 80), (40, 60, 70), (70, 60, 50)]
    roof_colors = [(30, 30, 50), (40, 30, 60), (20, 40, 50), (50, 40, 30)]
    
    house_color = random.choice(house_colors)
    roof_color = random.choice(roof_colors)
    
    draw_house(surface, x, y, house_width, house_height, house_color, roof_color)

# Create horizontal roads
road_positions = [height * 0.55, height * 0.65, height * 0.75]

for road_y in road_positions:
    road_height = 60
    road_rect = pygame.Rect(0, int(road_y), width, road_height)
    pygame.draw.rect(surface, (80, 80, 80), road_rect)
    
    # Road markings
    center_y = int(road_y + road_height // 2)
    for x in range(0, width, 80):
        pygame.draw.rect(surface, (255, 255, 0), (x, center_y - 2, 40, 4))

# Add trees and street lights along roads
for road_y in road_positions:
    # Trees
    tree_y_above = int(road_y - 15)
    for x in range(100, width - 100, 150):
        trunk_color = (101, 67, 33)
        pygame.draw.rect(surface, trunk_color, (x - 4, tree_y_above - 30, 8, 30))
        pygame.draw.circle(surface, (34, 139, 34), (x, tree_y_above - 30), 20)
    
    # Street lights
    light_y_above = int(road_y - 10)
    for x in range(200, width - 200, 250):
        pygame.draw.line(surface, (80, 80, 80), (x, light_y_above), (x, light_y_above - 40), 4)
        pygame.draw.circle(surface, (255, 255, 200), (x, light_y_above - 35), 8)

# Add houses between roads
road1_bottom = int(road_positions[0] + 60)
road2_top = int(road_positions[1])
space_between = road2_top - road1_bottom

if space_between > 40:
    house_y = road1_bottom + 10
    for x in range(100, width - 100, 200):
        house_width = random.randint(60, 90)
        house_height = min(40, space_between - 20)
        house_colors = [(90, 90, 110), (100, 90, 120), (80, 100, 110)]
        roof_colors = [(70, 70, 90), (80, 70, 100), (60, 80, 90)]
        draw_house(surface, x, house_y, house_width, house_height, 
                  random.choice(house_colors), random.choice(roof_colors))

# Add small sea at bottom
sea_height = 40
sea_y = height - sea_height
for y in range(sea_height):
    ratio = y / sea_height
    r = int(20 + (40 - 20) * ratio)
    g = int(60 + (100 - 60) * ratio)
    b = int(120 + (160 - 120) * ratio)
    pygame.draw.line(surface, (r, g, b), (0, sea_y + y), (width, sea_y + y))

# Save the image
pygame.image.save(surface, '../assets/images/bgm.jpg')
print('Background created: assets/images/bgm.jpg')

pygame.quit()
