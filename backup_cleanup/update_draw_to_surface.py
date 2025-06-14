"""
This script updates the draw_to_surface method in the SettingsMenu class to use the pulsating highlight.
Run this script to modify your car_game.py file.
"""

import re
import os

def update_draw_to_surface():
    # Path to the car_game.py file
    file_path = '/mnt/c/Users/ARNAB/OneDrive/Desktop/Hacathon/carpygame/car_game.py'
    
    # Code to add for highlighting selected option
    highlight_code = '''
            # Draw pulsating highlight around selected option if it's not the back button
            if i == self.selected_option and i < len(self.settings):
                option_rect = pygame.Rect(
                    self.screen_width // 2 - 150,
                    y_offset - 20,
                    300,
                    40
                )
                self.draw_pulsating_highlight(option_rect, ELECTRIC_PURPLE)
'''
    
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find where to insert the highlight code
    insert_pattern = r'if i == self.selected_option:.*?option_text = self.font_medium.render\(f"> \{option\} <", True, color\)'
    match = re.search(insert_pattern, content, re.DOTALL)
    
    if match:
        # Insert the highlight code before the existing code
        insert_position = match.start()
        new_content = content[:insert_position] + highlight_code + content[insert_position:]
        
        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(new_content)
        
        print("Successfully updated draw_to_surface method in SettingsMenu class!")
    else:
        print("Could not find the appropriate insertion point in draw_to_surface method.")

if __name__ == "__main__":
    update_draw_to_surface()
