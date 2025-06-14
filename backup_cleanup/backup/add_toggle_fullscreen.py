#!/usr/bin/env python3
import os

def add_toggle_fullscreen():
    """Add a toggle_fullscreen method to the Game class"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the Game class
    game_class_start = -1
    for i, line in enumerate(lines):
        if "class Game:" in line:
            game_class_start = i
            break
    
    if game_class_start == -1:
        print("Could not find Game class!")
        return
    
    # Find a good place to insert the toggle_fullscreen method
    # Let's look for the handle_resize method
    handle_resize_end = -1
    for i in range(game_class_start, len(lines)):
        if "def handle_resize" in lines[i]:
            # Find the end of this method
            for j in range(i, len(lines)):
                if j + 1 < len(lines) and lines[j + 1].startswith("    def "):
                    handle_resize_end = j + 1
                    break
            break
    
    if handle_resize_end == -1:
        print("Could not find a good place to insert toggle_fullscreen method!")
        return
    
    # Create the toggle_fullscreen method
    toggle_fullscreen_method = """    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
        
        # Check current display mode
        current_flags = pygame.display.get_surface().get_flags()
        is_fullscreen = bool(current_flags & pygame.FULLSCREEN)
        
        if is_fullscreen:
            # Switch to windowed mode
            if hasattr(self, "windowed_size"):
                window_width, window_height = self.windowed_size
            else:
                # Default size if no previous size is stored
                window_width, window_height = 1280, 720
            
            # Update global variables
            SCREEN_WIDTH = window_width
            SCREEN_HEIGHT = window_height
            
            # Set windowed mode
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 
                pygame.RESIZABLE
            )
        else:
            # Save current window size before going fullscreen
            self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Get the display info for proper fullscreen resolution
            info = pygame.display.Info()
            SCREEN_WIDTH = info.current_w
            SCREEN_HEIGHT = info.current_h
            
            # Set fullscreen mode with proper flags
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 
                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
        
        # Update scale factors
        SCALE_X = SCREEN_WIDTH / BASE_WIDTH
        SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
        
        # Recalculate lane positions
        LANE_WIDTH = SCREEN_WIDTH // 6
        LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
        
        # Update player position if it exists
        if hasattr(self, "player_car"):
            self.player_car.x = LANE_POSITIONS[self.player_car.lane]
            self.player_car.y = SCREEN_HEIGHT - scale_value(150)
        
        # Update fonts
        self.font = get_font(scale_value(36))
        self.font_large = get_font(scale_value(48), bold=True)
        self.font_medium = get_font(scale_value(36), bold=True)
        self.font_small = get_font(scale_value(24))
        
        # Regenerate stars for new screen size
        self.generate_stars()
        
        # Regenerate sparkles for new screen size
        if hasattr(self, "generate_sparkles"):
            self.generate_sparkles(100)
        
        # Force a redraw of the screen to apply changes
        pygame.display.flip()
        
        return is_fullscreen

"""
    
    # Insert the toggle_fullscreen method
    lines.insert(handle_resize_end, toggle_fullscreen_method)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("toggle_fullscreen method added successfully!")

if __name__ == "__main__":
    add_toggle_fullscreen()
