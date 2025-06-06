#!/usr/bin/env python3
import os
import sys
import re

def add_run_method_with_exception_handling(file_path):
    """Add an enhanced run method with exception handling to the game file"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Define the new run method with exception handling
        new_run_method = """
class Game:
    def __init__(self):
        try:
            # Create a resizable window with error handling
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            pygame.display.set_caption("Car Racing Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont(None, 36)
            self.particle_system = ParticleSystem()
            self.highscore_manager = HighScoreManager()
            
            # Day-night cycle variables
            self.cycle_time = 0
            self.day_phase = 0  # 0 = day, 0.25 = sunset, 0.5 = night, 0.75 = sunrise
            self.stars = []
            self.generate_stars()
            
            self.reset_game()
            logging.info("Game initialized successfully")
        except Exception as e:
            logging.critical(f"Error initializing game: {e}")
            logging.critical(traceback.format_exc())
            pygame.quit()
            sys.exit(1)
            
    def run(self):
        \"\"\"Main game loop with enhanced exception handling\"\"\"
        try:
            running = True
            in_menu = True
            
            # Log game start
            logging.info("Game loop started")
            
            # Track FPS
            fps_counter = 0
            fps_timer = time.time()
            
            while running:
                try:
                    if in_menu:
                        running = self.show_menu()
                        in_menu = False
                    else:
                        running = self.handle_events()
                        if not self.game_over and running:
                            self.update()
                            self.draw()
                        else:
                            in_menu = True
                    
                    # FPS counter
                    fps_counter += 1
                    if time.time() - fps_timer > 1:
                        current_fps = fps_counter / (time.time() - fps_timer)
                        if SHOW_FPS:
                            pygame.display.set_caption(f"Car Racing Game - FPS: {current_fps:.1f}")
                        fps_counter = 0
                        fps_timer = time.time()
                        
                        # Log FPS periodically
                        logging.debug(f"Current FPS: {current_fps:.1f}")
                    
                    # Cap the frame rate
                    self.clock.tick(FPS)
                    
                except Exception as e:
                    # Handle exceptions during gameplay without crashing
                    error_msg = f"Error during gameplay: {str(e)}"
                    logging.error(error_msg)
                    logging.error(traceback.format_exc())
                    
                    # Show error message to user
                    self.show_error_message(str(e))
                    
                    # Return to menu instead of crashing
                    in_menu = True
                    
                    # Give a short pause before continuing
                    time.sleep(1)
                    
        except Exception as e:
            # Handle critical exceptions that break the main loop
            error_msg = f"Critical error: {str(e)}"
            logging.critical(error_msg)
            logging.critical(traceback.format_exc())
            
            # Try to show error message before exiting
            try:
                self.show_critical_error(str(e))
            except:
                pass
                
        finally:
            # Log game end
            logging.info("Game loop ended")
            logging.info("=== Car Racing Game Exiting ===")
            
            # Clean up resources
            pygame.quit()
            sys.exit()
            
    def show_error_message(self, error_text):
        \"\"\"Display a non-critical error message to the user\"\"\"
        try:
            # Create a semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Semi-transparent black
            self.screen.blit(overlay, (0, 0))
            
            # Prepare fonts
            title_font = pygame.font.SysFont("arial", 36, bold=True)
            error_font = pygame.font.SysFont("arial", 24)
            
            # Draw error message
            title_text = title_font.render("Game Error", True, BRIGHT_RED)
            error_lines = self._wrap_text(error_text, error_font, SCREEN_WIDTH - 100)
            
            # Position text
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(title_text, title_rect)
            
            # Draw error text
            y_offset = SCREEN_HEIGHT // 3 + 50
            for line in error_lines:
                line_surf = error_font.render(line, True, WHITE)
                line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(line_surf, line_rect)
                y_offset += 30
            
            # Draw continue message
            continue_text = error_font.render("Press any key to continue", True, SLEEK_SILVER)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
            self.screen.blit(continue_text, continue_rect)
            
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
        except Exception as e:
            # If we can't show the error message, log it
            logging.error(f"Failed to show error message: {str(e)}")

    def show_critical_error(self, error_text):
        \"\"\"Display a critical error message before exiting\"\"\"
        try:
            # Create a new surface in case the main screen is corrupted
            screen = pygame.display.set_mode((800, 600))
            screen.fill(BLACK)
            
            # Prepare fonts
            title_font = pygame.font.SysFont("arial", 36, bold=True)
            error_font = pygame.font.SysFont("arial", 24)
            
            # Draw error message
            title_text = title_font.render("Critical Error", True, BRIGHT_RED)
            error_lines = self._wrap_text(f"A critical error has occurred: {error_text}", error_font, 700)
            log_text = error_font.render(f"Error details have been saved to: {log_file}", True, WHITE)
            
            # Position text
            title_rect = title_text.get_rect(center=(400, 150))
            screen.blit(title_text, title_rect)
            
            # Draw error text
            y_offset = 200
            for line in error_lines:
                line_surf = error_font.render(line, True, WHITE)
                line_rect = line_surf.get_rect(center=(400, y_offset))
                screen.blit(line_surf, line_rect)
                y_offset += 30
            
            # Draw log file info
            log_rect = log_text.get_rect(center=(400, 400))
            screen.blit(log_text, log_rect)
            
            # Draw exit message
            exit_text = error_font.render("Press any key to exit", True, SLEEK_SILVER)
            exit_rect = exit_text.get_rect(center=(400, 500))
            screen.blit(exit_text, exit_rect)
            
            pygame.display.flip()
            
            # Wait for key press
            waiting = True
            start_time = time.time()
            while waiting and time.time() - start_time < 10:  # 10 second timeout
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        return
                time.sleep(0.1)
        except Exception as e:
            # If we can't show the critical error, just log it
            logging.critical(f"Failed to show critical error screen: {str(e)}")

    def _wrap_text(self, text, font, max_width):
        \"\"\"Helper function to wrap text to fit within a given width\"\"\"
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Test width with current word added
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                # Line is full, start a new line
                lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines"""
        
        # Find the Game class definition
        game_class_pattern = r"class Game:"
        game_class_match = re.search(game_class_pattern, content)
        
        if not game_class_match:
            print("Error: Could not find Game class definition")
            return False
        
        # Replace the Game class with our enhanced version
        updated_content = content[:game_class_match.start()] + new_run_method + content[game_class_match.end():]
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        print("Successfully added enhanced run method with exception handling")
        return True
    
    except Exception as e:
        print(f"Error adding run method with exception handling: {e}")
        return False

def add_exception_handling_to_update_draw(file_path):
    """Add exception handling to update and draw methods"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Add exception handling to update method
        update_pattern = r"def update\(self\):"
        update_match = re.search(update_pattern, content)
        
        if update_match:
            # Find the start of the method body
            method_start = content.find(":", update_match.start()) + 1
            
            # Add try-except block
            updated_content = content[:method_start] + """
        try:
""" + content[method_start:]
            
            # Find the end of the update method
            next_def = content.find("def ", method_start)
            if next_def != -1:
                # Add except block before the next method
                updated_content = updated_content[:next_def] + """        except Exception as e:
            error_msg = f"Error in update method: {str(e)}"
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            raise  # Re-raise to be caught by the main loop
            
""" + updated_content[next_def:]
                
                content = updated_content
        
        # Add exception handling to draw method
        draw_pattern = r"def draw\(self\):"
        draw_match = re.search(draw_pattern, content)
        
        if draw_match:
            # Find the start of the method body
            method_start = content.find(":", draw_match.start()) + 1
            
            # Add try-except block
            updated_content = content[:method_start] + """
        try:
""" + content[method_start:]
            
            # Find the end of the draw method
            next_def = content.find("def ", method_start)
            if next_def != -1:
                # Add except block before the next method
                updated_content = updated_content[:next_def] + """        except Exception as e:
            error_msg = f"Error in draw method: {str(e)}"
            logging.error(error_msg)
            logging.error(traceback.format_exc())
            raise  # Re-raise to be caught by the main loop
            
""" + updated_content[next_def:]
                
                content = updated_content
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("Successfully added exception handling to update and draw methods")
        return True
    
    except Exception as e:
        print(f"Error adding exception handling to update and draw methods: {e}")
        return False

def main():
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        return
    
    print(f"Adding exception handling and crash logging to {game_file}...")
    
    # Add run method with exception handling
    if not add_run_method_with_exception_handling(game_file):
        print("Failed to add run method with exception handling")
        return
    
    # Add exception handling to update and draw methods
    if not add_exception_handling_to_update_draw(game_file):
        print("Failed to add exception handling to update and draw methods")
        return
    
    print("Successfully added exception handling and crash logging!")
    print("The game will now log errors to the 'logs' directory and display user-friendly error messages.")

if __name__ == "__main__":
    main()
