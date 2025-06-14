"""
This script updates the mouse click handling in the SettingsMenu class to use the animation.
Run this script to modify your car_game.py file.
"""

import re
import os

def update_mouse_click_handling():
    # Path to the car_game.py file
    file_path = '/mnt/c/Users/ARNAB/OneDrive/Desktop/Hacathon/carpygame/car_game.py'
    
    # New mouse click handling code
    new_mouse_click_code = '''                                # Toggle the setting
                                option = list(self.settings.keys())[i]
                                values = self.settings[option]
                                old_value = values[self.current_values[option]]
                                self.current_values[option] = (self.current_values[option] + 1) % len(values)
                                new_value = values[self.current_values[option]]
                                
                                # Animate the option toggle
                                self.animate_option_toggle(option, old_value, new_value)
                                
                                # Apply the setting
                                result = self.apply_setting(option)
                                if result:
                                    return result'''
    
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the mouse click handling code
    mouse_click_pattern = r'# Toggle the setting.*?if result:\s+return result'
    match = re.search(mouse_click_pattern, content, re.DOTALL)
    
    if match:
        # Replace the mouse click handling code
        new_content = content[:match.start()] + new_mouse_click_code + content[match.end():]
        
        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(new_content)
        
        print("Successfully updated mouse click handling in SettingsMenu class!")
    else:
        print("Could not find mouse click handling code in SettingsMenu class.")

if __name__ == "__main__":
    update_mouse_click_handling()
