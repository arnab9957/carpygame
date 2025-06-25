#!/usr/bin/env python3
"""
Test script to display the enhanced glowing moon
"""
import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
DEEP_BLUE = (5, 5, 25)
WHITE = (255, 255, 255)

def draw_moon(surface, screen_width, screen_height):
    """Draw a full glowing moon in the night sky with enhanced glow effects"""
    # Moon position (more to the corner - upper left)
    moon_x = int(screen_width * 0.15)  # Changed from 0.2 to 0.15 for more corner placement
    moon_y = int(screen_height * 0.15)  # Changed from 0.2 to 0.15 for more corner placement
    moon_radius = 50  # Even larger moon for better visibility
    
    # Get current time for animation
    current_time = pygame.time.get_ticks() / 1000.0
    
    # Animated glow intensity (pulsing effect) - much brighter
    glow_pulse = (math.sin(current_time * 0.8) + 1) * 0.5  # 0 to 1
    base_glow_intensity = 0.8 + glow_pulse * 0.6  # 0.8 to 1.4 - much brighter
    
    # Enhanced glow effect with multiple layers - much more intense
    glow_layers = [
        (150, (255, 255, 255, int(20 * base_glow_intensity))),   # Outermost bright white glow
        (120, (255, 255, 220, int(30 * base_glow_intensity))),   # Bright white glow
        (90, (255, 245, 180, int(45 * base_glow_intensity))),    # Warm yellow glow
        (70, (255, 235, 160, int(60 * base_glow_intensity))),    # Medium yellow glow
        (50, (255, 225, 140, int(80 * base_glow_intensity))),    # Inner warm glow
    ]
    
    # Draw glow layers
    for glow_radius, glow_color in glow_layers:
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surface, (moon_x - glow_radius, moon_y - glow_radius))
    
    # Draw main moon body with much brighter colors (FULL MOON - no shadow)
    moon_brightness = 1.0 + glow_pulse * 0.2  # Brighter variation
    moon_color = (
        min(255, int(255 * moon_brightness)),  # Full brightness
        min(255, int(250 * moon_brightness)), 
        min(255, int(220 * moon_brightness))
    )
    pygame.draw.circle(surface, moon_color, (moon_x, moon_y), moon_radius)
    
    # Add a much brighter rim light effect all around the moon for full moon
    rim_light_color = (255, 255, 255)  # Pure white
    for angle in range(0, 360, 45):  # Rim lights all around the moon
        rim_angle_rad = math.radians(angle)
        for i in range(3):
            rim_x = moon_x + (moon_radius - 8 - i * 2) * math.cos(rim_angle_rad)
            rim_y = moon_y + (moon_radius - 8 - i * 2) * math.sin(rim_angle_rad)
            rim_radius = 3 - i
            if rim_radius > 0:
                pygame.draw.circle(surface, rim_light_color, (int(rim_x), int(rim_y)), rim_radius)
    
    # Add MUCH MORE VISIBLE moon craters (bark spots) distributed across the full moon
    crater_base_color = (180, 180, 140)  # Much darker base color for better contrast
    crater_glow_color = (220, 220, 180)  # Darker glow color for better visibility
    crater_shadow_color = (120, 120, 90)  # Dark shadow color for depth
    
    # Multiple craters across the full moon surface - MUCH MORE VISIBLE
    craters = [
        (moon_x + 18, moon_y - 15, 12, 8, 6),   # Large crater with shadow
        (moon_x - 22, moon_y + 10, 10, 6, 4),   # Medium crater left side
        (moon_x + 12, moon_y + 22, 9, 5, 3),    # Medium crater bottom
        (moon_x - 10, moon_y - 18, 8, 4, 2),    # Small crater top left
        (moon_x + 28, moon_y + 12, 7, 3, 2),    # Small crater right
        (moon_x - 15, moon_y + 28, 6, 3, 2),    # Tiny crater bottom left
        (moon_x + 8, moon_y - 28, 6, 3, 2),     # Tiny crater top
        (moon_x - 25, moon_y - 8, 5, 2, 1),     # Extra small crater
        (moon_x + 25, moon_y - 5, 5, 2, 1),     # Extra small crater right
    ]
    
    # Draw craters with much better visibility
    for crater_x, crater_y, glow_radius, base_radius, shadow_radius in craters:
        # Draw shadow first for depth
        pygame.draw.circle(surface, crater_shadow_color, (int(crater_x + 1), int(crater_y + 1)), shadow_radius + 1)
        
        # Draw glow background
        pygame.draw.circle(surface, crater_glow_color, (int(crater_x), int(crater_y)), glow_radius)
        
        # Draw main crater
        pygame.draw.circle(surface, crater_base_color, (int(crater_x), int(crater_y)), base_radius)
        
        # Add inner shadow for realistic crater depth
        inner_shadow_color = (100, 100, 70)
        if base_radius > 2:
            pygame.draw.circle(surface, inner_shadow_color, (int(crater_x - 1), int(crater_y - 1)), max(1, base_radius - 2))
    
    # Add some additional surface texture spots for more realistic moon appearance
    texture_spots = [
        (moon_x - 5, moon_y + 5, 2),
        (moon_x + 15, moon_y - 5, 1),
        (moon_x - 12, moon_y - 12, 1),
        (moon_x + 20, moon_y + 20, 2),
        (moon_x - 20, moon_y + 15, 1),
        (moon_x + 5, moon_y + 15, 1),
    ]
    
    texture_color = (200, 200, 160)
    for spot_x, spot_y, spot_radius in texture_spots:
        pygame.draw.circle(surface, texture_color, (int(spot_x), int(spot_y)), spot_radius)
    
    # Add much brighter twinkling stars around the moon
    for i in range(8):  # More stars
        star_angle = current_time * 0.5 + i * 0.8  # Rotating positions
        star_distance = 90 + i * 8
        star_x = moon_x + math.cos(star_angle) * star_distance
        star_y = moon_y + math.sin(star_angle) * star_distance
        
        # Much brighter twinkling effect
        twinkle = (math.sin(current_time * 3 + i) + 1) * 0.5
        star_alpha = int(200 + twinkle * 55)  # 200 to 255 - much brighter
        star_size = 2 + int(twinkle * 3)  # 2 to 5 - larger stars
        
        # Draw star with glow
        star_glow_color = (255, 255, 255, max(100, star_alpha - 50))
        star_color = (255, 255, 255, star_alpha)
        
        # Draw glow first
        glow_surface = pygame.Surface((star_size * 6, star_size * 6), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, star_glow_color, (star_size * 3, star_size * 3), star_size * 2)
        surface.blit(glow_surface, (star_x - star_size * 3, star_y - star_size * 3))
        
        # Draw main star
        star_surface = pygame.Surface((star_size * 2, star_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, star_color, (star_size, star_size), star_size)
        surface.blit(star_surface, (star_x - star_size, star_y - star_size))

def main():
    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Enhanced Glowing Moon Test")
    clock = pygame.time.Clock()
    
    # Create night sky background
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        # Create gradient from deep blue to slightly lighter blue
        r = int(DEEP_BLUE[0] + (y / SCREEN_HEIGHT) * 10)
        g = int(DEEP_BLUE[1] + (y / SCREEN_HEIGHT) * 10)
        b = int(DEEP_BLUE[2] + (y / SCREEN_HEIGHT) * 15)
        pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Add some stars
    import random
    for i in range(50):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)  # Stars in upper half
        size = random.randint(1, 3)
        pygame.draw.circle(background, WHITE, (x, y), size)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Draw background
        screen.blit(background, (0, 0))
        
        # Draw the enhanced glowing moon
        draw_moon(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Add title
        font = pygame.font.Font(None, 48)
        title = font.render("Enhanced Glowing Full Moon", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(title, title_rect)
        
        # Add instructions
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Press ESC to exit", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(instruction, instruction_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
