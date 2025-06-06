#!/usr/bin/env python3
import os
import re

def fix_fullscreen_display():
    """Fix the fullscreen setting display in the settings menu"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Update the SettingsMenu class to check current fullscreen state
    pattern1 = r'(class SettingsMenu:.*?# Current values \(indexes into the settings arrays\)\s+self\.current_values = \{\s+)"FULLSCREEN": 0,  # OFF by default'
    replacement1 = r'\1"FULLSCREEN": 1 if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN else 0,  # Check if already in fullscreen'
    
    content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
    
    # Fix 2: Remove duplicate flags in fullscreen mode setting
    pattern2 = r'pygame\.FULLSCREEN \| pygame\.HWSURFACE \| pygame\.DOUBLEBUF \| pygame\.HWSURFACE \| pygame\.DOUBLEBUF'
    replacement2 = r'pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF'
    
    content = re.sub(pattern2, replacement2, content)
    
    # Fix 3: Update the show_settings_menu method to update fullscreen setting when opened
    pattern3 = r'(def show_settings_menu\(self, background_surface\):.*?# Create settings menu\s+)settings_menu = SettingsMenu\(self\.screen, screen_width, screen_height\)'
    replacement3 = r'\1# Check if we\'re in fullscreen mode\n        is_fullscreen = bool(pygame.display.get_surface().get_flags() & pygame.FULLSCREEN)\n        \n        # Create settings menu\n        settings_menu = SettingsMenu(self.screen, screen_width, screen_height)\n        \n        # Update fullscreen setting to match current state\n        settings_menu.current_values["FULLSCREEN"] = 1 if is_fullscreen else 0'
    
    content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("Fullscreen display fix applied successfully!")

if __name__ == "__main__":
    fix_fullscreen_display()
