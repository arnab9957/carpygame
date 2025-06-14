#!/usr/bin/env python3
import pygame
import sys

# Initialize pygame
pygame.init()

# Create a small window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Car Game Test")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill screen with black
    screen.fill((0, 0, 0))
    
    # Draw some text
    font = pygame.font.SysFont(None, 36)
    text = font.render("Car Game Test - Press ESC to exit", True, (255, 255, 255))
    screen.blit(text, (200, 250))
    
    # Update display
    pygame.display.flip()
    
    # Check for ESC key
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

# Quit pygame
pygame.quit()
sys.exit()
