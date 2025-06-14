#!/usr/bin/env python3
import os

def fix_settings_menu():
    """Fix the show_settings_menu method to properly handle fullscreen changes"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the show_settings_menu method
    start_line = -1
    end_line = -1
    for i, line in enumerate(lines):
        if "def show_settings_menu(self, background_surface):" in line:
            start_line = i
        elif start_line != -1 and line.strip().startswith("def "):
            end_line = i
            break
    
    if start_line == -1:
        print("Could not find show_settings_menu method!")
        return
    
    if end_line == -1:
        end_line = len(lines)
    
    # Create the fixed method
    fixed_method = """    def show_settings_menu(self, background_surface):
        # Global variables that will be updated
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
        
        # Get current screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Create settings menu
        settings_menu = SettingsMenu(self.screen, screen_width, screen_height)

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
                    return
                elif result == "EXIT":
                    pygame.quit()
                    sys.exit()
                elif result == "RESIZE" or result == "FULLSCREEN_CHANGED":
                    # Update the stored background after resize or fullscreen change
                    # Get the current screen surface which may have changed
                    self.screen = pygame.display.get_surface()
                    background_surface = self.screen.copy()
                    
                    # Update game dimensions
                    screen_width = self.screen.get_width()
                    screen_height = self.screen.get_height()
                    
                    # Update global variables to match new screen dimensions
                    SCREEN_WIDTH = screen_width
                    SCREEN_HEIGHT = screen_height
                    SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                    SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                    LANE_WIDTH = SCREEN_WIDTH // 6
                    LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                    
                    # Recreate settings menu with new dimensions
                    settings_menu = SettingsMenu(self.screen, screen_width, screen_height)

                clock.tick(30)
            except Exception as e:
                print(f"Error in settings menu: {e}")
                traceback.print_exc()
                return
"""
    
    # Replace the method
    new_lines = lines[:start_line] + [fixed_method] + lines[end_line:]
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_lines)
    
    print("Settings menu method fixed successfully!")

if __name__ == "__main__":
    fix_settings_menu()
