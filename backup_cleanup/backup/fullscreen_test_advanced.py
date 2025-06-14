#!/usr/bin/env python3
import pygame
import sys
import time
import traceback

# Initialize pygame
pygame.init()

# Create a window
try:
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Advanced Fullscreen Test")
except Exception as e:
    print(f"Error creating display: {e}")
    sys.exit(1)

# Font for text
try:
    font = pygame.font.SysFont(None, 36)
except Exception as e:
    print(f"Error loading font: {e}")
    font = pygame.font.Font(None, 36)  # Fallback to default font

# Track fullscreen state
is_fullscreen = False
windowed_size = (800, 600)

# Function to toggle fullscreen
def toggle_fullscreen():
    global screen, is_fullscreen, windowed_size
    
    try:
        print(f"\nToggling fullscreen. Current state: {'Fullscreen' if is_fullscreen else 'Windowed'}")
        
        # Store current screen content
        try:
            old_surface = pygame.display.get_surface().copy()
        except:
            old_surface = None
            print("Could not copy old surface")
        
        if is_fullscreen:
            # Switch to windowed mode
            print(f"Restoring windowed size: {windowed_size[0]}x{windowed_size[1]}")
            
            # Completely reinitialize the display
            pygame.display.quit()
            pygame.display.init()
            
            screen = pygame.display.set_mode(
                windowed_size, 
                pygame.RESIZABLE
            )
            pygame.display.set_caption("Advanced Fullscreen Test")
            print(f"New screen size: {screen.get_width()}x{screen.get_height()}")
        else:
            # Save current window size before going fullscreen
            windowed_size = (screen.get_width(), screen.get_height())
            print(f"Saving windowed size: {windowed_size}")
            
            # Get the display info for proper fullscreen resolution
            info = pygame.display.Info()
            width, height = info.current_w, info.current_h
            print(f"Setting fullscreen resolution: {width}x{height}")
            
            # Completely reinitialize the display
            pygame.display.quit()
            pygame.display.init()
            
            screen = pygame.display.set_mode(
                (width, height), 
                pygame.FULLSCREEN
            )
            pygame.display.set_caption("Advanced Fullscreen Test")
            print(f"New screen size: {screen.get_width()}x{screen.get_height()}")
        
        # Toggle the state
        is_fullscreen = not is_fullscreen
        
        # Try to restore the previous surface content
        try:
            if old_surface:
                scaled_surface = pygame.transform.scale(old_surface, (screen.get_width(), screen.get_height()))
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()
        except Exception as e:
            print(f"Could not restore previous screen content: {e}")
        
        return True
    except Exception as e:
        print(f"Error in toggle_fullscreen: {e}")
        traceback.print_exc()
        return False

# Function to handle window resize
def handle_resize(width, height):
    global screen
    
    try:
        print(f"\nHandling resize event: {width}x{height}")
        
        # Store current screen content
        try:
            old_surface = pygame.display.get_surface().copy()
        except:
            old_surface = None
            print("Could not copy old surface")
        
        # Resize the screen
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        print(f"New screen size: {screen.get_width()}x{screen.get_height()}")
        
        # Try to restore the previous surface content
        try:
            if old_surface:
                scaled_surface = pygame.transform.scale(old_surface, (width, height))
                screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()
        except Exception as e:
            print(f"Could not restore previous screen content: {e}")
        
        return True
    except Exception as e:
        print(f"Error handling resize: {e}")
        traceback.print_exc()
        return False

# Main loop
running = True
last_time = time.time()
frame_count = 0
fps = 0

while running:
    # Calculate FPS
    current_time = time.time()
    frame_count += 1
    if current_time - last_time >= 1.0:
        fps = frame_count
        frame_count = 0
        last_time = current_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_f:
                # Toggle fullscreen
                toggle_fullscreen()
            elif event.key == pygame.K_r:
                # Force redraw
                pygame.display.flip()
                print("Forced screen redraw")
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize
            if not is_fullscreen:
                handle_resize(event.w, event.h)
    
    # Fill screen with dark blue
    screen.fill((20, 30, 80))
    
    # Draw instructions
    try:
        text1 = font.render("Press F to toggle fullscreen", True, (255, 255, 255))
        text2 = font.render("Press ESC to exit", True, (255, 255, 255))
        text3 = font.render(f"Current mode: {'Fullscreen' if is_fullscreen else 'Windowed'}", True, (255, 255, 0))
        text4 = font.render(f"Screen size: {screen.get_width()}x{screen.get_height()}", True, (255, 255, 0))
        text5 = font.render(f"FPS: {fps}", True, (255, 255, 0))
        text6 = font.render("Press R to force redraw", True, (255, 255, 255))
        
        screen.blit(text1, (50, 50))
        screen.blit(text2, (50, 100))
        screen.blit(text3, (50, 150))
        screen.blit(text4, (50, 200))
        screen.blit(text5, (50, 250))
        screen.blit(text6, (50, 300))
    except Exception as e:
        print(f"Error rendering text: {e}")
    
    # Draw a moving object to verify animation works
    try:
        pygame.draw.circle(
            screen, 
            (255, 0, 0), 
            (int(400 + 200 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 20).x),
             int(400 + 200 * pygame.math.Vector2(1, 0).rotate(pygame.time.get_ticks() / 20).y)),
            20
        )
    except Exception as e:
        print(f"Error drawing animation: {e}")
    
    # Update display
    try:
        pygame.display.flip()
    except Exception as e:
        print(f"Error updating display: {e}")
    
    # Cap the frame rate
    pygame.time.delay(16)  # ~60 FPS

# Quit pygame
pygame.quit()
sys.exit()
