#!/usr/bin/env python3

# This script adds a method to the SettingsMenu class to handle fullscreen changes
# and updates the handle_input method to use it

import re

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    content = file.read()

# Find the SettingsMenu class
settings_menu_pattern = r'class SettingsMenu:(.*?)def handle_input\(self\):'
settings_menu_match = re.search(settings_menu_pattern, content, re.DOTALL)

if settings_menu_match:
    # Add the handle_fullscreen_change method before handle_input
    settings_menu_code = settings_menu_match.group(1)
    new_settings_menu_code = settings_menu_code + """    def handle_fullscreen_change(self, option):
        \"\"\"Special handler for fullscreen changes to ensure proper screen updates\"\"\"
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
        
        if option == "FULLSCREEN":
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
                return True
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
                return True
        
        return False

    def handle_input(self):
"""
    
    # Replace the old settings menu code with the new one
    content = content.replace(settings_menu_code, new_settings_menu_code)
    
    # Update the apply_setting method to use the new handler
    apply_setting_pattern = r'def apply_setting\(self, option\):(.*?)# Other settings would be applied here(.*?)print\('
    apply_setting_replacement = r'''def apply_setting(self, option):
        # Apply the setting change
        if option == "FULLSCREEN":
            # Use the special handler for fullscreen changes
            if self.handle_fullscreen_change(option):
                return "FULLSCREEN_CHANGED"
        
        # Other settings would be applied here\2print('''
    
    content = re.sub(apply_setting_pattern, apply_setting_replacement, content, flags=re.DOTALL)
    
    # Write the modified content back to the file
    with open('car_game_advanced_new.py', 'w') as file:
        file.write(content)
    
    print("Added fullscreen handler method to SettingsMenu class")
else:
    print("Could not find SettingsMenu class")
