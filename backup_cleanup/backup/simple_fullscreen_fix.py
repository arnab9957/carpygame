#!/usr/bin/env python3

def fix_fullscreen():
    """Apply a simple fix to the fullscreen mode"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Update the show_settings_menu method to properly handle fullscreen changes
    old_settings_menu = """    def show_settings_menu(self, background_surface):
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
                    
                    # Recreate settings menu with new dimensions
                    settings_menu = SettingsMenu(self.screen, screen_width, screen_height)"""
    
    new_settings_menu = """    def show_settings_menu(self, background_surface):
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
                    settings_menu = SettingsMenu(self.screen, screen_width, screen_height)"""
    
    # Fix 2: Update the windowed_size in apply_setting method
    old_windowed_size = "self.windowed_size = (self.screen_width, self.screen_height)"
    new_windowed_size = "self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)"
    
    # Apply the fixes
    content = content.replace(old_settings_menu, new_settings_menu)
    content = content.replace(old_windowed_size, new_windowed_size)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("Simple fullscreen fix applied successfully!")

if __name__ == "__main__":
    fix_fullscreen()
