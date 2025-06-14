#!/usr/bin/env python3

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    lines = file.readlines()

# Find the SettingsMenu class
settings_menu_start = 0
for i, line in enumerate(lines):
    if line.strip() == "class SettingsMenu:":
        settings_menu_start = i
        break

# Find the apply_setting method
apply_setting_start = 0
for i in range(settings_menu_start, len(lines)):
    if "def apply_setting(self, option):" in lines[i]:
        apply_setting_start = i
        break

# Replace the apply_setting method with a fixed version
if apply_setting_start > 0:
    # Find the end of the method
    apply_setting_end = apply_setting_start + 1
    indent_level = len(lines[apply_setting_start]) - len(lines[apply_setting_start].lstrip())
    
    while apply_setting_end < len(lines):
        if lines[apply_setting_end].strip() == "" or (len(lines[apply_setting_end]) - len(lines[apply_setting_end].lstrip()) <= indent_level and lines[apply_setting_end].strip().startswith("def ")):
            break
        apply_setting_end += 1
    
    # Create the fixed method
    fixed_method = """    def apply_setting(self, option):
        # Apply the setting change
        if option == "FULLSCREEN":
            # Access global variables
            import pygame
            global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
            
            if self.current_values[option] == 1:  # ON
                # Save current window size before going fullscreen
                self.windowed_size = (self.screen_width, self.screen_height)
                
                # Get the display info for proper fullscreen resolution
                info = pygame.display.Info()
                
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
                return "FULLSCREEN_CHANGED"
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
                return "FULLSCREEN_CHANGED"

        # Other settings would be applied here
        # For now, we'll just print the change
        print(
            f"Setting {option} changed to {self.settings[option][self.current_values[option]]}"
        )
        return None
"""
    
    # Replace the method
    lines[apply_setting_start:apply_setting_end] = fixed_method.splitlines(True)
    
    # Find the show_settings_menu method
    show_settings_start = 0
    for i, line in enumerate(lines):
        if "def show_settings_menu(self, background_surface):" in line:
            show_settings_start = i
            break
    
    if show_settings_start > 0:
        # Find the end of the method
        show_settings_end = show_settings_start + 1
        indent_level = len(lines[show_settings_start]) - len(lines[show_settings_start].lstrip())
        
        while show_settings_end < len(lines):
            if lines[show_settings_end].strip() == "" or (len(lines[show_settings_end]) - len(lines[show_settings_end].lstrip()) <= indent_level and lines[show_settings_end].strip().startswith("def ")):
                break
            show_settings_end += 1
        
        # Create the fixed method
        fixed_show_settings = """    def show_settings_menu(self, background_surface):
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
                    global SCREEN_WIDTH, SCREEN_HEIGHT
                    SCREEN_WIDTH = self.screen.get_width()
                    SCREEN_HEIGHT = self.screen.get_height()
                    
                    # Update player car position if it exists
                    if hasattr(self, "player_car"):
                        self.player_car.x = LANE_POSITIONS[self.player_car.lane]
                        self.player_car.y = SCREEN_HEIGHT - scale_value(150)
                    
                    # Recreate settings menu with new dimensions
                    settings_menu = SettingsMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

                clock.tick(30)
            except Exception as e:
                print(f"Error in settings menu: {e}")
                traceback.print_exc()
                return
"""
        
        # Replace the method
        lines[show_settings_start:show_settings_end] = fixed_show_settings.splitlines(True)
    
    # Write the modified file
    with open('car_game_advanced_new.py', 'w') as file:
        file.writelines(lines)
    
    print("Applied comprehensive fix for fullscreen mode")
else:
    print("Could not find apply_setting method")
