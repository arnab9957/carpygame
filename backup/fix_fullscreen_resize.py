#!/usr/bin/env python3

# This script adds code to update the game state when toggling fullscreen mode

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    lines = file.readlines()

# Find the apply_setting method in SettingsMenu class
settings_menu_start = 0
for i, line in enumerate(lines):
    if line.strip() == "class SettingsMenu:":
        settings_menu_start = i
        break

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
                # Get current screen info
                info = pygame.display.Info()
                
                # Set fullscreen mode
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                
                # Update screen dimensions
                self.screen = pygame.display.get_surface()
                self.screen_width = self.screen.get_width()
                self.screen_height = self.screen.get_height()
                
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
                return "FULLSCREEN_CHANGED"
            else:  # OFF
                # Set windowed mode
                pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                
                # Update screen dimensions
                self.screen = pygame.display.get_surface()
                self.screen_width = self.screen.get_width()
                self.screen_height = self.screen.get_height()
                
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
                return "FULLSCREEN_CHANGED"

        # Other settings would be applied here
        # For now, we'll just print the change
        print(f"Setting {option} changed to {self.settings[option][self.current_values[option]]}")
        return None
"""
    
    # Replace the method
    lines[apply_setting_start:apply_setting_end] = fixed_method.splitlines(True)
    
    # Find the handle_input method in SettingsMenu class
    handle_input_start = 0
    for i in range(apply_setting_end, len(lines)):
        if "def handle_input(self):" in lines[i]:
            handle_input_start = i
            break
    
    if handle_input_start > 0:
        # Find the part where LEFT key is handled
        left_key_start = 0
        for i in range(handle_input_start, len(lines)):
            if "elif event.key == pygame.K_LEFT:" in lines[i]:
                left_key_start = i
                break
        
        # Find the part where RIGHT key is handled
        right_key_start = 0
        for i in range(left_key_start + 1, len(lines)):
            if "elif event.key == pygame.K_RIGHT:" in lines[i]:
                right_key_start = i
                break
        
        # Update the LEFT key handler
        if left_key_start > 0:
            for i in range(left_key_start, right_key_start):
                if "self.apply_setting(option)" in lines[i]:
                    lines[i] = lines[i].replace("self.apply_setting(option)", "result = self.apply_setting(option)")
                    # Add code to handle fullscreen change
                    indent = lines[i].split("self.")[0]
                    lines.insert(i + 1, f"{indent}# Return special result if fullscreen changed\n")
                    lines.insert(i + 2, f"{indent}if option == \"FULLSCREEN\" and result == \"FULLSCREEN_CHANGED\":\n")
                    lines.insert(i + 3, f"{indent}    return \"FULLSCREEN_CHANGED\"\n")
                    break
        
        # Update the RIGHT key handler
        if right_key_start > 0:
            for i in range(right_key_start, len(lines)):
                if "self.apply_setting(option)" in lines[i]:
                    lines[i] = lines[i].replace("self.apply_setting(option)", "result = self.apply_setting(option)")
                    # Add code to handle fullscreen change
                    indent = lines[i].split("self.")[0]
                    lines.insert(i + 1, f"{indent}# Return special result if fullscreen changed\n")
                    lines.insert(i + 2, f"{indent}if option == \"FULLSCREEN\" and result == \"FULLSCREEN_CHANGED\":\n")
                    lines.insert(i + 3, f"{indent}    return \"FULLSCREEN_CHANGED\"\n")
                    break
    
    # Find the show_settings_menu method
    show_settings_start = 0
    for i, line in enumerate(lines):
        if "def show_settings_menu(self, background_surface):" in line:
            show_settings_start = i
            break
    
    if show_settings_start > 0:
        # Find the part where result is checked
        result_check_start = 0
        for i in range(show_settings_start, len(lines)):
            if "if result == \"BACK\":" in lines[i]:
                result_check_start = i
                break
        
        # Find the part where RESIZE is handled
        resize_start = 0
        for i in range(result_check_start, len(lines)):
            if "elif result == \"RESIZE\":" in lines[i]:
                resize_start = i
                break
        
        # Update the RESIZE handler to also handle FULLSCREEN_CHANGED
        if resize_start > 0:
            lines[resize_start] = lines[resize_start].replace("elif result == \"RESIZE\":", "elif result == \"RESIZE\" or result == \"FULLSCREEN_CHANGED\":")
            
            # Add code to update game dimensions
            for i in range(resize_start, len(lines)):
                if "background_surface = self.screen.copy()" in lines[i]:
                    indent = lines[i].split("background_surface")[0]
                    lines.insert(i + 1, f"{indent}# Update game dimensions\n")
                    lines.insert(i + 2, f"{indent}global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS\n")
                    lines.insert(i + 3, f"{indent}SCREEN_WIDTH = self.screen.get_width()\n")
                    lines.insert(i + 4, f"{indent}SCREEN_HEIGHT = self.screen.get_height()\n")
                    lines.insert(i + 5, f"{indent}SCALE_X = SCREEN_WIDTH / BASE_WIDTH\n")
                    lines.insert(i + 6, f"{indent}SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT\n")
                    lines.insert(i + 7, f"{indent}LANE_WIDTH = SCREEN_WIDTH // 6\n")
                    lines.insert(i + 8, f"{indent}LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]\n")
                    lines.insert(i + 9, f"{indent}\n")
                    lines.insert(i + 10, f"{indent}# Update player car position if it exists\n")
                    lines.insert(i + 11, f"{indent}if hasattr(self, \"player_car\"):\n")
                    lines.insert(i + 12, f"{indent}    self.player_car.x = LANE_POSITIONS[self.player_car.lane]\n")
                    lines.insert(i + 13, f"{indent}    self.player_car.y = SCREEN_HEIGHT - scale_value(150)\n")
                    lines.insert(i + 14, f"{indent}\n")
                    lines.insert(i + 15, f"{indent}# Recreate settings menu with new dimensions\n")
                    lines.insert(i + 16, f"{indent}settings_menu = SettingsMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)\n")
                    break
    
    # Write the modified file
    with open('car_game_advanced_new.py', 'w') as file:
        file.writelines(lines)
    
    print("Fixed fullscreen resize handling")
else:
    print("Could not find apply_setting method")
