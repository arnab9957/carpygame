"""
This script updates the RIGHT key handling in the SettingsMenu class to use the animation.
Run this script to modify your car_game.py file.
"""

import re
import os

def update_right_key_handling():
    # Path to the car_game.py file
    file_path = '/mnt/c/Users/ARNAB/OneDrive/Desktop/Hacathon/carpygame/car_game.py'
    
    # New RIGHT key handling code
    new_right_key_code = '''                elif event.key == pygame.K_RIGHT:
                    if self.selected_option < len(self.settings):
                        option = list(self.settings.keys())[self.selected_option]
                        values = self.settings[option]
                        old_value = values[self.current_values[option]]
                        self.current_values[option] = (self.current_values[option] + 1) % len(values)
                        new_value = values[self.current_values[option]]
                        
                        # Play menu navigation sound
                        if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                            try:
                                sound_menu_navigate.play()
                            except:
                                pass
                        
                        # Animate the option toggle
                        self.animate_option_toggle(option, old_value, new_value)
                        
                        # Apply the setting
                        result = self.apply_setting(option)
                        if result:
                            return result'''
    
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the RIGHT key handling code
    right_key_pattern = r'elif event\.key == pygame\.K_RIGHT:.*?if result:\s+return result'
    match = re.search(right_key_pattern, content, re.DOTALL)
    
    if match:
        # Replace the RIGHT key handling code
        new_content = content[:match.start()] + new_right_key_code + content[match.end():]
        
        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(new_content)
        
        print("Successfully updated RIGHT key handling in SettingsMenu class!")
    else:
        print("Could not find RIGHT key handling code in SettingsMenu class.")

if __name__ == "__main__":
    update_right_key_handling()
