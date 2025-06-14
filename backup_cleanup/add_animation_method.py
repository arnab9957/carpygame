"""
This script adds the animate_option_toggle method to the SettingsMenu class in car_game.py.
Run this script to modify your car_game.py file.
"""

import re
import os

def add_animation_method():
    # Path to the car_game.py file
    file_path = '/mnt/c/Users/ARNAB/OneDrive/Desktop/Hacathon/carpygame/car_game.py'
    
    # Animation method to add
    animation_method = '''
    def animate_option_toggle(self, option, old_value, new_value):
        """Animate transitioning between option values"""
        # Animation parameters
        duration = 0.3  # seconds
        start_time = time.time()
        
        # Calculate the position of the value text
        option_index = list(self.settings.keys()).index(option)
        y_offset = self.screen_height * 0.35 + option_index * 60
        value_rect = pygame.Rect(
            self.screen_width // 2 + 20,
            y_offset - 15,
            100,
            30
        )
        
        # Create surfaces for old and new values
        old_surface = self.font_medium.render(old_value, True, WHITE)
        new_surface = self.font_medium.render(new_value, True, WHITE)
        
        # Store original screen content
        original_bg = self.screen.copy()
        
        # Animation loop
        clock = pygame.time.Clock()
        while True:
            current_time = time.time()
            progress = min(1.0, (current_time - start_time) / duration)
            
            # Restore background
            self.screen.blit(original_bg, (0, 0))
            
            if progress < 0.5:
                # First half: fade out old value and slide up
                alpha = int(255 * (1 - progress * 2))
                offset_y = int(-20 * progress * 2)
                
                # Create a temporary surface with alpha
                temp_surface = pygame.Surface(old_surface.get_size(), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))
                temp_surface.blit(old_surface, (0, 0))
                temp_surface.set_alpha(alpha)
                
                # Draw with offset
                self.screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
            else:
                # Second half: fade in new value and slide down
                alpha = int(255 * ((progress - 0.5) * 2))
                offset_y = int(20 * (1 - (progress - 0.5) * 2))
                
                # Create a temporary surface with alpha
                temp_surface = pygame.Surface(new_surface.get_size(), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))
                temp_surface.blit(new_surface, (0, 0))
                temp_surface.set_alpha(alpha)
                
                # Draw with offset
                self.screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
            
            pygame.display.flip()
            
            # Check if animation is complete
            if progress >= 1.0:
                break
            
            # Handle events during animation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Cap the frame rate
            clock.tick(60)
'''
    
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the SettingsMenu class
    settings_menu_pattern = r'class SettingsMenu:'
    match = re.search(settings_menu_pattern, content)
    
    if match:
        # Find the end of the __init__ method
        init_end_pattern = r'def __init__.*?self\.windowed_size = \(screen_width, screen_height\)'
        init_match = re.search(init_end_pattern, content, re.DOTALL)
        
        if init_match:
            # Insert the animation method after the __init__ method
            insert_position = init_match.end()
            new_content = content[:insert_position] + animation_method + content[insert_position:]
            
            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.write(new_content)
            
            print("Successfully added animate_option_toggle method to SettingsMenu class!")
        else:
            print("Could not find the end of the __init__ method in SettingsMenu class.")
    else:
        print("Could not find SettingsMenu class in car_game.py.")

if __name__ == "__main__":
    add_animation_method()
