#!/usr/bin/env python3
import pygame
import sys
import traceback

# Initialize pygame
pygame.init()

# Create a simple window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Debug Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game modes
GAME_MODE_ENDLESS = 0
GAME_MODE_TIME_ATTACK = 1
GAME_MODE_MISSIONS = 2

class SimpleGame:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.game_mode = GAME_MODE_ENDLESS
        self.in_menu = True
        
    def show_menu(self):
        screen.fill(BLACK)
        
        # Draw title
        title = self.font.render("SIMPLE GAME MENU", True, WHITE)
        screen.blit(title, (400 - title.get_width() // 2, 100))
        
        # Draw buttons
        buttons = [
            ("ENDLESS MODE", GAME_MODE_ENDLESS, (400, 250)),
            ("TIME ATTACK", GAME_MODE_TIME_ATTACK, (400, 300)),
            ("MISSIONS", GAME_MODE_MISSIONS, (400, 350)),
            ("EXIT", -1, (400, 450))
        ]
        
        button_rects = []
        
        for text, mode, pos in buttons:
            text_surf = self.font.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=pos)
            button_rect = text_rect.inflate(20, 10)
            
            # Draw button
            pygame.draw.rect(screen, BLUE, button_rect, 2, border_radius=5)
            screen.blit(text_surf, text_rect)
            
            button_rects.append((button_rect, mode))
            
        pygame.display.flip()
        
        # Handle events
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for rect, mode in button_rects:
                            if rect.collidepoint(event.pos):
                                if mode == -1:
                                    return False
                                else:
                                    print(f"Selected game mode: {mode}")
                                    self.game_mode = mode
                                    self.in_menu = False
                                    return True
            
            clock.tick(60)
        
        return False
    
    def play_game(self):
        screen.fill(BLACK)
        
        # Draw game mode info
        if self.game_mode == GAME_MODE_ENDLESS:
            mode_text = "ENDLESS MODE"
            color = GREEN
        elif self.game_mode == GAME_MODE_TIME_ATTACK:
            mode_text = "TIME ATTACK MODE"
            color = BLUE
        else:
            mode_text = "MISSIONS MODE"
            color = RED
            
        mode_surf = self.font.render(f"Playing: {mode_text}", True, color)
        screen.blit(mode_surf, (400 - mode_surf.get_width() // 2, 200))
        
        # Draw back button
        back_text = self.font.render("BACK TO MENU", True, WHITE)
        back_rect = back_text.get_rect(center=(400, 400))
        button_rect = back_rect.inflate(20, 10)
        pygame.draw.rect(screen, RED, button_rect, 2, border_radius=5)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()
        
        # Handle events
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and button_rect.collidepoint(event.pos):
                        self.in_menu = True
                        return True
            
            clock.tick(60)
        
        return False
    
    def run(self):
        running = True
        
        while running:
            if self.in_menu:
                running = self.show_menu()
            else:
                running = self.play_game()
                
            clock.tick(60)

# Run the game
try:
    game = SimpleGame()
    game.run()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
finally:
    pygame.quit()
    sys.exit()
