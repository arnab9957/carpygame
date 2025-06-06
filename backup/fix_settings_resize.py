#!/usr/bin/env python3
import os

def fix_settings_resize():
    """Fix the resize method in SettingsMenu class"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the resize method in SettingsMenu class
    start_line = -1
    end_line = -1
    for i, line in enumerate(lines):
        if "def resize(self, screen_width, screen_height):" in line and i > 2000:
            start_line = i
            break
    
    if start_line == -1:
        print("Could not find resize method in SettingsMenu class!")
        return
    
    # Find the end of the method
    for i in range(start_line + 1, len(lines)):
        if lines[i].strip().startswith("def "):
            end_line = i
            break
    
    if end_line == -1:
        end_line = len(lines)
    
    # Create the fixed method
    fixed_method = """    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = get_font(int(screen_height * 0.06), bold=True)
        self.font_medium = get_font(int(screen_height * 0.04), bold=True)
        self.font_small = get_font(int(screen_height * 0.03))
        self.create_background()
"""
    
    # Replace the method
    new_lines = lines[:start_line] + [fixed_method] + lines[end_line:]
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_lines)
    
    print("resize method in SettingsMenu class fixed successfully!")

if __name__ == "__main__":
    fix_settings_resize()
