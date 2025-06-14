#!/usr/bin/env python3
import os
import sys
import re

def update_show_highscores_method(file_path):
    """Update the show_highscores method to stay on the screen after deletion"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the show_highscores method
        show_highscores_pattern = r'def show_highscores\(self.*?\):.*?self\.clock\.tick\(30\)'
        show_highscores_match = re.search(show_highscores_pattern, content, re.DOTALL)
        
        if not show_highscores_match:
            print("Error: Could not find show_highscores method")
            return False
        
        old_show_highscores = show_highscores_match.group(0)
        
        # Create the new show_highscores method with fixed delete functionality
        new_show_highscores = """def show_highscores(self, player_name=None):
        \"\"\"Show the high scores screen with delete buttons\"\"\"
        # Define colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        NEON_YELLOW = (255, 255, 0)
        ELECTRIC_PURPLE = (191, 64, 191)
        SLEEK_SILVER = (204, 204, 204)
        BRIGHT_RED = (255, 62, 65)
        
        # Get screen dimensions
        SCREEN_WIDTH = self.screen.get_width()
        SCREEN_HEIGHT = self.screen.get_height()
        
        # Create a semi-transparent background
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        background.fill((0, 0, 0, 180))  # Semi-transparent black
        
        title_font = pygame.font.SysFont("arial", 48, bold=True)
        score_font = pygame.font.SysFont("arial", 24)
        
        # Get mode name for display
        if self.game_mode == GAME_MODE_ENDLESS:
            mode_name = "ENDLESS MODE"
        elif self.game_mode == GAME_MODE_TIME_ATTACK:
            mode_name = "TIME ATTACK MODE"
        else:
            mode_name = "MISSIONS MODE"
        
        # Get high scores for current game mode
        highscores = self.highscore_manager.get_highscores(self.game_mode)
        
        # Create delete buttons for each score
        delete_buttons = []
        
        done = False
        while not done:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    else:
                        done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Check if any delete button was clicked
                        button_clicked = False
                        for i, button_rect in enumerate(delete_buttons):
                            if button_rect.collidepoint(mouse_pos):
                                button_clicked = True
                                # Delete the score
                                if self.highscore_manager.delete_score(self.game_mode, i):
                                    # Refresh the high scores list
                                    highscores = self.highscore_manager.get_highscores(self.game_mode)
                                    # Don't exit the screen, just refresh the display
                                break
                        
                        # Only exit if we clicked outside any button and not on a delete button
                        if not button_clicked:
                            # Check if we clicked on the "back" area at the bottom
                            back_area = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 70, 
                                                  SCREEN_WIDTH // 2, 40)
                            if back_area.collidepoint(mouse_pos):
                                done = True
            
            # Draw background
            self.screen.blit(background, (0, 0))
            
            # Draw title
            title_text = title_font.render("HIGH SCORES", True, NEON_YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
            self.screen.blit(title_text, title_rect)
            
            # Draw mode name
            mode_text = score_font.render(mode_name, True, ELECTRIC_PURPLE)
            mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 50))
            self.screen.blit(mode_text, mode_rect)
            
            # Draw column headers
            header_y = SCREEN_HEIGHT // 6 + 100
            rank_text = score_font.render("RANK", True, SLEEK_SILVER)
            name_text = score_font.render("NAME", True, SLEEK_SILVER)
            score_text = score_font.render("SCORE", True, SLEEK_SILVER)
            date_text = score_font.render("DATE", True, SLEEK_SILVER)
            action_text = score_font.render("ACTION", True, SLEEK_SILVER)
            
            self.screen.blit(rank_text, (SCREEN_WIDTH // 6 - rank_text.get_width() // 2, header_y))
            self.screen.blit(name_text, (SCREEN_WIDTH * 2 // 6 - name_text.get_width() // 2, header_y))
            self.screen.blit(score_text, (SCREEN_WIDTH * 3 // 6 - score_text.get_width() // 2, header_y))
            self.screen.blit(date_text, (SCREEN_WIDTH * 4 // 6 - date_text.get_width() // 2, header_y))
            self.screen.blit(action_text, (SCREEN_WIDTH * 5 // 6 - action_text.get_width() // 2, header_y))
            
            # Draw horizontal line
            pygame.draw.line(self.screen, SLEEK_SILVER, 
                           (SCREEN_WIDTH // 10, header_y + 30), 
                           (SCREEN_WIDTH * 9 // 10, header_y + 30), 2)
            
            # Draw high scores
            delete_buttons = []  # Clear previous buttons
            
            if not highscores:
                no_scores_text = score_font.render("No high scores yet!", True, WHITE)
                no_scores_rect = no_scores_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(no_scores_text, no_scores_rect)
            else:
                for i, score in enumerate(highscores):
                    y_pos = header_y + 60 + i * 40
                    
                    # Highlight the player's score
                    if player_name and score["name"] == player_name:
                        highlight_rect = pygame.Rect(SCREEN_WIDTH // 10, y_pos - 5, 
                                                  SCREEN_WIDTH * 8 // 10, 30)
                        pygame.draw.rect(self.screen, (50, 50, 100, 100), highlight_rect, border_radius=5)
                    
                    # Rank
                    rank_text = score_font.render(f"{i+1}", True, WHITE)
                    self.screen.blit(rank_text, (SCREEN_WIDTH // 6 - rank_text.get_width() // 2, y_pos))
                    
                    # Name
                    name_text = score_font.render(score["name"], True, WHITE)
                    self.screen.blit(name_text, (SCREEN_WIDTH * 2 // 6 - name_text.get_width() // 2, y_pos))
                    
                    # Score
                    score_text = score_font.render(f"{score['score']}", True, WHITE)
                    self.screen.blit(score_text, (SCREEN_WIDTH * 3 // 6 - score_text.get_width() // 2, y_pos))
                    
                    # Date
                    date_text = score_font.render(score["date"], True, WHITE)
                    self.screen.blit(date_text, (SCREEN_WIDTH * 4 // 6 - date_text.get_width() // 2, y_pos))
                    
                    # Delete button
                    delete_button_rect = pygame.Rect(SCREEN_WIDTH * 5 // 6 - 40, y_pos - 10, 80, 30)
                    pygame.draw.rect(self.screen, BRIGHT_RED, delete_button_rect, border_radius=5)
                    delete_text = score_font.render("Delete", True, WHITE)
                    delete_text_rect = delete_text.get_rect(center=delete_button_rect.center)
                    self.screen.blit(delete_text, delete_text_rect)
                    
                    # Add button to the list
                    delete_buttons.append(delete_button_rect)
            
            # Draw back button area
            back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 40)
            pygame.draw.rect(self.screen, SLEEK_SILVER, back_button_rect, 2, border_radius=10)
            
            # Draw instructions
            instruction_text = score_font.render("Back to Menu", True, SLEEK_SILVER)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(instruction_text, instruction_rect)
            
            pygame.display.flip()
            self.clock.tick(30)"""
        
        # Replace the old implementation with the new one
        updated_content = content.replace(old_show_highscores, new_show_highscores)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        print("Successfully updated show_highscores method to stay on screen after deletion")
        return True
    
    except Exception as e:
        print(f"Error updating show_highscores method: {e}")
        return False

def main():
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        return
    
    print(f"Fixing delete button functionality in {game_file}...")
    
    # Update show_highscores method
    if not update_show_highscores_method(game_file):
        print("Failed to update show_highscores method")
        return
    
    print("Successfully fixed delete button functionality!")
    print("Now you can delete scores and remain on the high score screen.")

if __name__ == "__main__":
    main()
