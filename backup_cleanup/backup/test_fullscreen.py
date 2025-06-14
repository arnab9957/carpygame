#!/usr/bin/env python3
import pygame
import sys

# Initialize pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Fullscreen Test")

# Font for text
font = pygame.font.SysFont(None, 36)

# Track fullscreen state
is_fullscreen = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_f:
                # Toggle fullscreen
                is_fullscreen = not is_fullscreen
                print(f"Toggling fullscreen: {is_fullscreen}")
                
                if is_fullscreen:
                    # Get display info for proper fullscreen resolution
                    info = pygame.display.Info()
                    width, height = info.current_w, info.current_h
                    print(f"Setting fullscreen mode: {width}x{height}")
                    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
                else:
                    # Return to windowed mode
                    print("Setting windowed mode: 800x600")
                    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                
                # Print actual screen size after change
                actual_width, actual_height = screen.get_size()
                print(f"Actual screen size: {actual_width}x{actual_height}")
        
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize
            if not is_fullscreen:
                width, height = event.w, event.h
                print(f"Window resized to: {width}x{height}")
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    
    # Fill screen with dark blue
    screen.fill((20, 30, 80))
    
    # Draw instructions
    text1 = font.render("Press F to toggle fullscreen", True, (255, 255, 255))
    text2 = font.render("Press ESC to exit", True, (255, 255, 255))
    text3 = font.render(f"Current mode: {'Fullscreen' if is_fullscreen else 'Windowed'}", True, (255, 255, 0))
    
    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 100))
    screen.blit(text3, (50, 150))
    
    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
