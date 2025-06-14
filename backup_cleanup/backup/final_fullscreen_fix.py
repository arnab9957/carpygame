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
            if self.current_values[option] == 1:  # ON
                # Save current window size before going fullscreen
                self.windowed_size = (self.screen_width, self.screen_height)
                
                # Set fullscreen mode
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                
                # Update menu dimensions
                self.screen = screen
                self.screen_width = screen.get_width()
                self.screen_height = screen.get_height()
                
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
                
                print(f"Switched to fullscreen mode: {self.screen_width}x{self.screen_height}")
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
                
                # Update menu dimensions
                self.screen = screen
                self.screen_width = screen.get_width()
                self.screen_height = screen.get_height()
                
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
                
                print(f"Switched to windowed mode: {self.screen_width}x{self.screen_height}")

        # Other settings would be applied here
        # For now, we'll just print the change
        print(f"Setting {option} changed to {self.settings[option][self.current_values[option]]}")
        return None
"""
    
    # Replace the method
    lines[apply_setting_start:apply_setting_end] = fixed_method.splitlines(True)
    
    # Write the modified file
    with open('car_game_advanced_new.py', 'w') as file:
        file.writelines(lines)
    
    print("Applied final fix for fullscreen mode")
else:
    print("Could not find apply_setting method")
