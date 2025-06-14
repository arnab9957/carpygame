#!/usr/bin/env python3

import re

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    content = file.read()

# Find the show_menu method
menu_pattern = r'(def show_menu\(self\):.*?# Draw background\s+if has_background_image:.*?self\.screen\.blit\(overlay, \(0, 0\)\))'
menu_replacement = r'\1\n                \n                # Draw sparkles animation\n                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation\n                self.draw_sparkles(self.screen)'

# Apply the replacement
content = re.sub(menu_pattern, menu_replacement, content, flags=re.DOTALL)

# Find the main menu loop
loop_pattern = r'(# Main menu loop\s+running = True\s+clock = pygame\.time\.Clock\(\)\s+# Track the last selected option to detect changes\s+last_selected = -1\s+while running:.*?# Get mouse position\s+mouse_pos = pygame\.mouse\.get_pos\(\))'
loop_replacement = r'\1\n            \n            # Update sparkles\n            dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds\n            self.update_sparkles(dt)'

# Apply the replacement
content = re.sub(loop_pattern, loop_replacement, content, flags=re.DOTALL)

# Write the modified content back to the file
with open('car_game_advanced_new.py', 'w') as file:
    file.write(content)

print("Added sparkle animation to the main menu")
