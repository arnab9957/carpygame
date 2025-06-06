#!/usr/bin/env python3
import pygame
import math
import sys

def show_game_over(screen, clock, score, distance_traveled, coins_collected, game_mode, highscore_manager):
    """Show game over screen and handle high score if applicable"""
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BRIGHT_RED = (255, 62, 65)
    NEON_YELLOW = (255, 255, 0)
    ELECTRIC_PURPLE = (191, 64, 191)
    SLEEK_SILVER = (204, 204, 204)
    COIN_COLOR = (255, 223, 0)
    
    # Get screen dimensions
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    
    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    title_font = pygame.font.SysFont("arial", 72, bold=True)
    score_font = pygame.font.SysFont("arial", 48)
    info_font = pygame.font.SysFont("arial", 36)
    
    # Draw game over text
    game_over_text = title_font.render("GAME OVER", True, BRIGHT_RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    
    # Add glow effect
    for offset in range(5, 0, -1):
        glow_rect = game_over_rect.copy()
        glow_rect.inflate_ip(offset * 2, offset * 2)
        pygame.draw.rect(screen, (min(BRIGHT_RED[0], 255), min(BRIGHT_RED[1], 255), min(BRIGHT_RED[2] + offset * 5, 255)), 
                       glow_rect, 2, border_radius=5)
    
    screen.blit(game_over_text, game_over_rect)
    
    # Draw score
    score_text = score_font.render(f"SCORE: {score}", True, NEON_YELLOW)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
    screen.blit(score_text, score_rect)
    
    # Draw distance and coins
    distance_text = info_font.render(f"Distance: {int(distance_traveled)}m", True, WHITE)
    coins_text = info_font.render(f"Coins: {coins_collected}", True, COIN_COLOR)
    
    distance_rect = distance_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 160))
    coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 210))
    
    screen.blit(distance_text, distance_rect)
    screen.blit(coins_text, coins_rect)
    
    # Check if this is a new highest score
    is_highest_score = highscore_manager.is_high_score(game_mode, score)
    
    if is_highest_score:
        # Show new high score message
        high_score_text = info_font.render("NEW HIGHEST SCORE!", True, ELECTRIC_PURPLE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 270))
        
        # Add pulsating effect
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 10
        pygame.draw.rect(screen, ELECTRIC_PURPLE, high_score_rect.inflate(pulse, pulse), 2, border_radius=5)
        
        screen.blit(high_score_text, high_score_rect)
        
        # Prompt for name
        name_prompt = info_font.render("Enter your name:", True, WHITE)
        name_prompt_rect = name_prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(name_prompt, name_prompt_rect)
        
        # Get player name
        player_name = get_player_name(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Save high score
        highscore_manager.add_score(
            game_mode,
            player_name,
            score,
            distance=int(distance_traveled),
            coins=coins_collected
        )
        
        # Show high scores
        show_highscores(screen, clock, game_mode, highscore_manager, player_name)
    else:
        # Show message that it's not a high score
        not_high_score_text = info_font.render("Not a new highest score", True, SLEEK_SILVER)
        not_high_score_rect = not_high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 270))
        screen.blit(not_high_score_text, not_high_score_rect)
        
        # Show continue prompt
        continue_text = info_font.render("Press any key to continue", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

def get_player_name(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT):
    """Get player name for high score"""
    # Define colors
    WHITE = (255, 255, 255)
    SLEEK_SILVER = (204, 204, 204)
    NEON_YELLOW = (255, 255, 0)
    
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 80, 400, 50)
    color_inactive = SLEEK_SILVER
    color_active = NEON_YELLOW
    color = color_active
    active = True
    text = "Player"  # Default name
    done = False
    
    input_font = pygame.font.SysFont("arial", 32)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # Limit name length to 15 characters
                        if len(text) < 15:
                            text += event.unicode
        
        # Draw input box
        pygame.draw.rect(screen, color, input_box, 2, border_radius=10)
        
        # Draw input text
        txt_surface = input_font.render(text, True, WHITE)
        # Ensure text doesn't overflow the input box
        width = max(400, txt_surface.get_width() + 10)
        input_box.w = width
        input_box.x = SCREEN_WIDTH // 2 - width // 2
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        
        # Draw instructions
        instruction_text = pygame.font.SysFont("arial", 24).render("Press ENTER to confirm", True, SLEEK_SILVER)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
        clock.tick(30)
    
    return text

def show_highscores(screen, clock, game_mode, highscore_manager, player_name=None):
    """Show the high scores screen"""
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    NEON_YELLOW = (255, 255, 0)
    ELECTRIC_PURPLE = (191, 64, 191)
    SLEEK_SILVER = (204, 204, 204)
    
    # Get screen dimensions
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    
    # Get high scores for current game mode
    highscores = highscore_manager.get_highscores(game_mode)
    
    # Create a semi-transparent background
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    background.fill((0, 0, 0, 180))  # Semi-transparent black
    
    title_font = pygame.font.SysFont("arial", 48, bold=True)
    score_font = pygame.font.SysFont("arial", 24)
    
    # Get mode name for display
    if game_mode == 0:  # GAME_MODE_ENDLESS
        mode_name = "ENDLESS MODE"
    elif game_mode == 1:  # GAME_MODE_TIME_ATTACK
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
        screen.blit(background, (0, 0))
        
        # Draw title
        title_text = title_font.render("HIGH SCORES", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        screen.blit(title_text, title_rect)
        
        # Draw mode name
        mode_text = score_font.render(mode_name, True, ELECTRIC_PURPLE)
        mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 50))
        screen.blit(mode_text, mode_rect)
        
        # Draw column headers
        header_y = SCREEN_HEIGHT // 6 + 100
        rank_text = score_font.render("RANK", True, SLEEK_SILVER)
        name_text = score_font.render("NAME", True, SLEEK_SILVER)
        score_text = score_font.render("SCORE", True, SLEEK_SILVER)
        date_text = score_font.render("DATE", True, SLEEK_SILVER)
        
        screen.blit(rank_text, (SCREEN_WIDTH // 5 - rank_text.get_width() // 2, header_y))
        screen.blit(name_text, (SCREEN_WIDTH * 2 // 5 - name_text.get_width() // 2, header_y))
        screen.blit(score_text, (SCREEN_WIDTH * 3 // 5 - score_text.get_width() // 2, header_y))
        screen.blit(date_text, (SCREEN_WIDTH * 4 // 5 - date_text.get_width() // 2, header_y))
        
        # Draw horizontal line
        pygame.draw.line(screen, SLEEK_SILVER, 
                       (SCREEN_WIDTH // 10, header_y + 30), 
                       (SCREEN_WIDTH * 9 // 10, header_y + 30), 2)
        
        # Draw high scores
        if not highscores:
            no_scores_text = score_font.render("No high scores yet!", True, WHITE)
            no_scores_rect = no_scores_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(no_scores_text, no_scores_rect)
        else:
            for i, score in enumerate(highscores):
                y_pos = header_y + 60 + i * 40
                
                # Highlight the player's score
                if player_name and score["name"] == player_name:
                    highlight_rect = pygame.Rect(SCREEN_WIDTH // 10, y_pos - 5, 
                                              SCREEN_WIDTH * 8 // 10, 30)
                    pygame.draw.rect(screen, (50, 50, 100, 100), highlight_rect, border_radius=5)
                
                # Rank
                rank_text = score_font.render(f"{i+1}", True, WHITE)
                screen.blit(rank_text, (SCREEN_WIDTH // 5 - rank_text.get_width() // 2, y_pos))
                
                # Name
                name_text = score_font.render(score["name"], True, WHITE)
                screen.blit(name_text, (SCREEN_WIDTH * 2 // 5 - name_text.get_width() // 2, y_pos))
                
                # Score
                score_text = score_font.render(f"{score['score']}", True, WHITE)
                screen.blit(score_text, (SCREEN_WIDTH * 3 // 5 - score_text.get_width() // 2, y_pos))
                
                # Date
                date_text = score_font.render(score["date"], True, WHITE)
                screen.blit(date_text, (SCREEN_WIDTH * 4 // 5 - date_text.get_width() // 2, y_pos))
        
        # Draw instructions
        instruction_text = score_font.render("Press any key to continue", True, SLEEK_SILVER)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
        
        pygame.display.flip()
        clock.tick(30)
