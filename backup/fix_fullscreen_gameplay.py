#!/usr/bin/env python3

# This script fixes fullscreen gameplay issues by ensuring the game properly
# updates all screen-dependent variables when toggling fullscreen mode

import re

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    content = file.read()

# Update the apply_setting method to properly update global variables and recalculate game elements
apply_setting_pattern = r'def apply_setting\(self, option\):(.*?)# Other settings would be applied here'
apply_setting_replacement = r'''def apply_setting(self, option):
        # Apply the setting change
        if option == "FULLSCREEN":
            global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
            
            if self.current_values[option] == 1:  # ON
                # Save current window size before going fullscreen
                self.windowed_size = (self.screen_width, self.screen_height)
                
                # Set fullscreen mode
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                
                # Update global dimensions
                SCREEN_WIDTH = screen.get_width()
                SCREEN_HEIGHT = screen.get_height()
                
                # Update scale factors
                SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                
                # Update menu dimensions
                self.screen = screen
                self.screen_width = SCREEN_WIDTH
                self.screen_height = SCREEN_HEIGHT
                
                # Update fonts for new screen size
                self.font_large = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.06), bold=True
                )
                self.font_medium = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.04), bold=True
                )
                self.font_small = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.03)
                )
                
                print(f"Switched to fullscreen mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
            else:  # OFF
                # Restore previous window size
                if hasattr(self, 'windowed_size'):
                    window_width, window_height = self.windowed_size
                else:
                    # Default size if no previous size is stored
                    window_width, window_height = 1280, 720
                
                # Set windowed mode
                screen = pygame.display.set_mode(
                    (window_width, window_height), 
                    pygame.RESIZABLE
                )
                
                # Update global dimensions
                SCREEN_WIDTH = screen.get_width()
                SCREEN_HEIGHT = screen.get_height()
                
                # Update scale factors
                SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                
                # Update menu dimensions
                self.screen = screen
                self.screen_width = SCREEN_WIDTH
                self.screen_height = SCREEN_HEIGHT
                
                # Update fonts for new screen size
                self.font_large = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.06), bold=True
                )
                self.font_medium = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.04), bold=True
                )
                self.font_small = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.03)
                )
                
                print(f"Switched to windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        # Other settings would be applied here'''

# Update the show_settings_menu method to properly update the game state after fullscreen changes
show_settings_pattern = r'def show_settings_menu\(self, background_surface\):(.*?)# Main settings menu loop(.*?)while True:(.*?)if result == "BACK":(.*?)return(.*?)elif result == "RESIZE":(.*?)background_surface = self\.screen\.copy\(\)'
show_settings_replacement = r'''def show_settings_menu(self, background_surface):
        # Create settings menu
        settings_menu = SettingsMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Main settings menu loop
        clock = pygame.time.Clock()
        while True:
            try:
                # Restore the background
                self.screen.blit(background_surface, (0, 0))

                # Draw and handle the settings menu
                settings_menu.draw()
                result = settings_menu.handle_input()

                if result == "BACK":
                    # When returning from settings, make sure we have the correct screen
                    self.screen = pygame.display.get_surface()
                    
                    # Update player car position based on new lane positions if they changed
                    if hasattr(self, "player_car"):
                        self.player_car.x = LANE_POSITIONS[self.player_car.lane]
                        self.player_car.y = SCREEN_HEIGHT - scale_value(150)
                    
                    return
                elif result == "EXIT":
                    pygame.quit()
                    sys.exit()
                elif result == "RESIZE":
                    # Update the stored background after resize
                    background_surface = self.screen.copy()
                
                # Maintain consistent frame rate
                clock.tick(30)
            except Exception as e:
                print(f"Error in settings menu: {e}")
                traceback.print_exc()
                return'''

# Apply the replacements
content = re.sub(apply_setting_pattern, apply_setting_replacement, content, flags=re.DOTALL)
content = re.sub(show_settings_pattern, show_settings_replacement, content, flags=re.DOTALL)

# Write the modified content back to the file
with open('car_game_advanced_new.py', 'w') as file:
    file.write(content)

print("Fixed fullscreen gameplay issues")
