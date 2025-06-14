#!/usr/bin/env python3
import os

def fix_resize():
    """Fix the resize methods in both SettingsMenu and PauseMenu classes"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the SettingsMenu class resize method
    settings_start = content.find("class SettingsMenu:")
    if settings_start == -1:
        print("Could not find SettingsMenu class!")
        return
    
    resize_start = content.find("def resize(self, screen_width, screen_height):", settings_start)
    if resize_start == -1:
        print("Could not find resize method in SettingsMenu class!")
        return
    
    # Find the PauseMenu class resize method
    pause_start = content.find("class PauseMenu:")
    if pause_start == -1:
        print("Could not find PauseMenu class!")
        return
    
    pause_resize_start = content.find("def resize(self, screen_width, screen_height):", pause_start)
    if pause_resize_start == -1:
        print("Could not find resize method in PauseMenu class!")
        return
    
    # Create the fixed resize method
    fixed_method = """    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = get_font(int(screen_height * 0.06), bold=True)
        self.font_medium = get_font(int(screen_height * 0.04), bold=True)
        self.font_small = get_font(int(screen_height * 0.03))
        self.create_background()
"""
    
    # Find the end of the resize methods
    settings_resize_end = content.find("    def", resize_start + 10)
    pause_resize_end = content.find("    def", pause_resize_start + 10)
    
    if settings_resize_end == -1 or pause_resize_end == -1:
        print("Could not find the end of resize methods!")
        return
    
    # Replace the methods
    new_content = (
        content[:resize_start] + 
        fixed_method + 
        content[settings_resize_end:pause_resize_start] + 
        fixed_method + 
        content[pause_resize_end:]
    )
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print("resize methods fixed successfully!")

if __name__ == "__main__":
    fix_resize()
