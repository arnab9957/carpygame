"""
This script adds the draw_pulsating_highlight method to the SettingsMenu class.
Run this script to modify your car_game.py file.
"""

import re
import os

def add_pulsating_highlight():
    # Path to the car_game.py file
    file_path = '/mnt/c/Users/ARNAB/OneDrive/Desktop/Hacathon/carpygame/car_game.py'
    
    # Pulsating highlight method to add
    highlight_method = '''
    def draw_pulsating_highlight(self, rect, color, thickness=2):
        """Draw a pulsating highlight around the given rectangle"""
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5  # 0.0 to 1.0
        
        # Calculate pulsating size and alpha
        expand = int(pulse * 6)
        alpha = int(128 + pulse * 127)  # 128-255
        
        # Create a surface for the highlight
        highlight_rect = rect.inflate(expand, expand)
        highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        
        # Draw the highlight with alpha
        highlight_color = (*color, alpha)
        pygame.draw.rect(highlight_surface, highlight_color, (0, 0, highlight_rect.width, highlight_rect.height), thickness, border_radius=5)
        
        # Draw the highlight
        self.screen.blit(highlight_surface, highlight_rect.topleft)
'''
    
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the animate_option_toggle method
    animation_method_pattern = r'def animate_option_toggle.*?clock\.tick\(60\)'
    match = re.search(animation_method_pattern, content, re.DOTALL)
    
    if match:
        # Insert the highlight method after the animation method
        insert_position = match.end()
        new_content = content[:insert_position] + highlight_method + content[insert_position:]
        
        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(new_content)
        
        print("Successfully added draw_pulsating_highlight method to SettingsMenu class!")
    else:
        print("Could not find animate_option_toggle method in SettingsMenu class.")

if __name__ == "__main__":
    add_pulsating_highlight()
