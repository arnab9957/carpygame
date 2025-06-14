#!/usr/bin/env python3
import os
import re

def fix_fullscreen_background():
    """Fix the background display when switching to fullscreen mode"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Update the apply_setting method to recreate the background when switching to fullscreen
    pattern1 = r'(# Update fonts for new screen size\n\s+)self\.font_large = (pygame\.font\.SysFont|get_font)\(\s+.*?\s+\)\s+self\.font_medium = (pygame\.font\.SysFont|get_font)\(\s+.*?\s+\)\s+self\.font_small = (pygame\.font\.SysFont|get_font)\(\s+.*?\s+\)(\s+\n\s+print\(f"Switched to fullscreen mode)'
    replacement1 = r'\1self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n                self.font_small = get_font(int(self.screen_height * 0.03))\n                \n                # Recreate background for new dimensions\n                self.create_background()\6'
    
    content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
    
    # Fix 2: Also update the windowed mode section to recreate the background
    pattern2 = r'(# Update fonts for new screen size\n\s+)self\.font_large = (pygame\.font\.SysFont|get_font)\(\s+.*?\s+\)\s+self\.font_medium = (pygame\.font\.SysFont|get_font)\(\s+.*?\s+\)\s+self\.font_small = (pygame\.font\.SysFont|get_font)\(\s+.*?\s+\)(\s+\n\s+print\(f"Switched to windowed mode)'
    replacement2 = r'\1self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n                self.font_small = get_font(int(self.screen_height * 0.03))\n                \n                # Recreate background for new dimensions\n                self.create_background()\5'
    
    content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
    
    # Fix 3: Update the show_settings_menu method to properly handle background when resolution changes
    pattern3 = r'(elif result == "RESIZE" or result == "FULLSCREEN_CHANGED":.*?# Recreate settings menu with new dimensions\s+settings_menu = SettingsMenu\(self\.screen, screen_width, screen_height\))'
    replacement3 = r'\1\n                    \n                    # Recreate the background surface for the new resolution\n                    try:\n                        # Try to load the background image\n                        background_image = pygame.image.load("bgm.jpg")\n                        # Scale the image to fit the new screen size\n                        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))\n                        # Create a new background surface\n                        background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))\n                        background_surface.blit(background_image, (0, 0))\n                        # Add semi-transparent overlay\n                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)\n                        overlay.fill((0, 0, 0, 120))\n                        background_surface.blit(overlay, (0, 0))\n                    except Exception as e:\n                        print(f"Error recreating background after resolution change: {e}")'
    
    content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("Fullscreen background fix applied successfully!")

if __name__ == "__main__":
    fix_fullscreen_background()
