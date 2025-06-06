#!/usr/bin/env python3
import os
import re

def fix_fullscreen_mode():
    """Apply a comprehensive fix to the fullscreen mode"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Update the apply_setting method in SettingsMenu class
    settings_apply_setting_pattern = r'(def apply_setting\(self, option\):.*?# Set fullscreen mode\n\s+self\.screen = pygame\.display\.set_mode\(\s+\(SCREEN_WIDTH, SCREEN_HEIGHT\),\s+)pygame\.FULLSCREEN(\s+\))'
    settings_apply_setting_replacement = r'\1pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF\2'
    
    content = re.sub(settings_apply_setting_pattern, settings_apply_setting_replacement, content, flags=re.DOTALL)
    
    # Fix 2: Update the show_settings_menu method to properly handle fullscreen changes
    show_settings_menu_pattern = r'(def show_settings_menu\(self, background_surface\):.*?# Update global variables to match new screen dimensions.*?LANE_POSITIONS = \[LANE_WIDTH \* i \+ LANE_WIDTH // 2 for i in range\(6\)\]\s+)(\s+# Recreate settings menu)'
    show_settings_menu_replacement = r'\1    # Force a redraw of the screen to apply changes\n        pygame.display.flip()\n\2'
    
    content = re.sub(show_settings_menu_pattern, show_settings_menu_replacement, content, flags=re.DOTALL)
    
    # Fix 3: Add a proper fullscreen toggle function
    handle_resize_pattern = r'(def handle_resize\(self, width, height\):.*?# Regenerate stars for new screen size\s+self\.generate_stars\(\)\s+)'
    handle_resize_replacement = r'\1        # Force a redraw of the screen to apply changes\n        pygame.display.flip()\n\n    def toggle_fullscreen(self):\n        """Toggle between fullscreen and windowed mode"""\n        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS\n        \n        # Check current display mode\n        current_flags = pygame.display.get_surface().get_flags()\n        is_fullscreen = bool(current_flags & pygame.FULLSCREEN)\n        \n        if is_fullscreen:\n            # Switch to windowed mode\n            if hasattr(self, "windowed_size"):\n                window_width, window_height = self.windowed_size\n            else:\n                # Default size if no previous size is stored\n                window_width, window_height = 1280, 720\n            \n            # Update global variables\n            SCREEN_WIDTH = window_width\n            SCREEN_HEIGHT = window_height\n            \n            # Set windowed mode\n            self.screen = pygame.display.set_mode(\n                (SCREEN_WIDTH, SCREEN_HEIGHT), \n                pygame.RESIZABLE\n            )\n        else:\n            # Save current window size before going fullscreen\n            self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)\n            \n            # Get the display info for proper fullscreen resolution\n            info = pygame.display.Info()\n            SCREEN_WIDTH = info.current_w\n            SCREEN_HEIGHT = info.current_h\n            \n            # Set fullscreen mode with proper flags\n            self.screen = pygame.display.set_mode(\n                (SCREEN_WIDTH, SCREEN_HEIGHT), \n                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF\n            )\n        \n        # Update scale factors\n        SCALE_X = SCREEN_WIDTH / BASE_WIDTH\n        SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT\n        \n        # Recalculate lane positions\n        LANE_WIDTH = SCREEN_WIDTH // 6\n        LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]\n        \n        # Update player position if it exists\n        if hasattr(self, "player_car"):\n            self.player_car.x = LANE_POSITIONS[self.player_car.lane]\n            self.player_car.y = SCREEN_HEIGHT - scale_value(150)\n        \n        # Update fonts\n        self.font = get_font(scale_value(36))\n        self.font_large = get_font(scale_value(48), bold=True)\n        self.font_medium = get_font(scale_value(36), bold=True)\n        self.font_small = get_font(scale_value(24))\n        \n        # Regenerate stars for new screen size\n        self.generate_stars()\n        \n        # Regenerate sparkles for new screen size\n        if hasattr(self, "generate_sparkles"):\n            self.generate_sparkles(100)\n        \n        # Force a redraw of the screen to apply changes\n        pygame.display.flip()\n        \n        return is_fullscreen\n'
    
    content = re.sub(handle_resize_pattern, handle_resize_replacement, content, flags=re.DOTALL)
    
    # Fix 4: Add a keyboard shortcut for toggling fullscreen (F11)
    handle_events_pattern = r'(def handle_events\(self\):.*?if event\.type == pygame\.KEYDOWN:.*?)(elif event\.key == pygame\.K_ESCAPE or event\.key == pygame\.K_p:)'
    handle_events_replacement = r'\1    elif event.key == pygame.K_F11:\n                        # Toggle fullscreen mode when F11 is pressed\n                        self.toggle_fullscreen()\n                    \2'
    
    content = re.sub(handle_events_pattern, handle_events_replacement, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("Comprehensive fullscreen fix applied successfully!")

if __name__ == "__main__":
    fix_fullscreen_mode()
