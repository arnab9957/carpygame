#!/usr/bin/env python3
import os
import re

def fix_fullscreen_mode():
    """Fix fullscreen mode in the car racing game"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Update the apply_setting method in SettingsMenu class
    # Replace pygame.font.SysFont with get_font
    # Replace self.screen_width with SCREEN_WIDTH for saving window size
    pattern1 = r'(def apply_setting\(self, option\):.*?# Save current window size before going fullscreen\n\s+)self\.windowed_size = \(self\.screen_width, self\.screen_height\)(.*?# Update fonts for new screen size\n\s+)self\.font_large = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.06\), bold=True\s+\)\s+self\.font_medium = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.04\), bold=True\s+\)\s+self\.font_small = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.03\)\s+\)(.*?# Update fonts for new screen size\n\s+)self\.font_large = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.06\), bold=True\s+\)\s+self\.font_medium = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.04\), bold=True\s+\)\s+self\.font_small = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.03\)\s+\)'
    replacement1 = r'\1self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)\2self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n                self.font_small = get_font(int(self.screen_height * 0.03))\3self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n                self.font_small = get_font(int(self.screen_height * 0.03))'
    
    content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
    
    # Fix 2: Update the apply_setting method in PauseMenu class
    # Replace pygame.font.SysFont with get_font
    # Replace self.screen_width with SCREEN_WIDTH for saving window size
    pattern2 = r'(def apply_setting\(self, option\):.*?# Save current window size before going fullscreen\n\s+)self\.windowed_size = \(self\.screen_width, self\.screen_height\)(.*?# Update fonts for new screen size\n\s+)self\.font_large = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.06\), bold=True\s+\)\s+self\.font_medium = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.04\), bold=True\s+\)\s+self\.font_small = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.03\)\s+\)(.*?# Update fonts for new screen size\n\s+)self\.font_large = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.06\), bold=True\s+\)\s+self\.font_medium = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.04\), bold=True\s+\)\s+self\.font_small = pygame\.font\.SysFont\(\s+"arial", int\(self\.screen_height \* 0\.03\)\s+\)'
    replacement2 = r'\1self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)\2self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n                self.font_small = get_font(int(self.screen_height * 0.03))\3self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n                self.font_small = get_font(int(self.screen_height * 0.03))'
    
    content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
    
    # Fix 3: Update the resize method in SettingsMenu class
    pattern3 = r'(def resize\(self, screen_width, screen_height\):\n\s+self\.screen_width = screen_width\n\s+self\.screen_height = screen_height\n\s+)self\.font_large = pygame\.font\.SysFont\(\s+"arial", int\(screen_height \* 0\.06\), bold=True\s+\)\s+self\.font_medium = pygame\.font\.SysFont\(\s+"arial", int\(screen_height \* 0\.04\), bold=True\s+\)\s+self\.font_small = pygame\.font\.SysFont\("arial", int\(screen_height \* 0\.03\)\)'
    replacement3 = r'\1self.font_large = get_font(int(screen_height * 0.06), bold=True)\n        self.font_medium = get_font(int(screen_height * 0.04), bold=True)\n        self.font_small = get_font(int(screen_height * 0.03))'
    
    content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)
    
    # Fix 4: Update the resize method in PauseMenu class
    pattern4 = r'(def resize\(self, screen_width, screen_height\):\n\s+self\.screen_width = screen_width\n\s+self\.screen_height = screen_height\n\s+)self\.font_large = pygame\.font\.SysFont\(\s+"arial", int\(screen_height \* 0\.06\), bold=True\s+\)\s+self\.font_medium = pygame\.font\.SysFont\(\s+"arial", int\(screen_height \* 0\.04\), bold=True\s+\)\s+self\.font_small = pygame\.font\.SysFont\("arial", int\(screen_height \* 0\.03\)\)'
    replacement4 = r'\1self.font_large = get_font(int(screen_height * 0.06), bold=True)\n        self.font_medium = get_font(int(screen_height * 0.04), bold=True)\n        self.font_small = get_font(int(screen_height * 0.03))'
    
    content = re.sub(pattern4, replacement4, content, flags=re.DOTALL)
    
    # Fix 5: Update the show_settings_menu method to properly handle fullscreen changes
    pattern5 = r'(def show_settings_menu\(self, background_surface\):\n)(\s+# Get current screen dimensions)'
    replacement5 = r'\1    # Global variables that will be updated\n    global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS\n\2'
    
    content = re.sub(pattern5, replacement5, content, flags=re.DOTALL)
    
    # Fix 6: Update the handle_resize method to properly update all global variables
    pattern6 = r'(def handle_resize\(self, width, height\):.*?# Regenerate stars for new screen size\n\s+self\.generate_stars\(\)\n)'
    replacement6 = r'\1    # Regenerate sparkles for new screen size\n    if hasattr(self, "generate_sparkles"):\n        self.generate_sparkles(100)\n\n'
    
    content = re.sub(pattern6, replacement6, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("Fullscreen mode fix applied successfully!")

if __name__ == "__main__":
    fix_fullscreen_mode()
