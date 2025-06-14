#!/usr/bin/env python3

import re

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    content = file.read()

# Pattern for game over in collision with obstacles
pattern1 = r'(self\.game_over = True\n\s+# Start crash animation timer\n\s+self\.crash_animation_timer = time\.time\(\))'
replacement1 = r'self.game_over = True\n                        self.game_has_been_played = True  # Mark that a game has been played\n                        # Start crash animation timer\n                        self.crash_animation_timer = time.time()'

# Pattern for game over in time attack mode
pattern2 = r'(self\.game_over = True\n\s+# Play game over sound)'
replacement2 = r'self.game_over = True\n                    self.game_has_been_played = True  # Mark that a game has been played\n                    # Play game over sound'

# Apply the replacements
content = re.sub(pattern1, replacement1, content)
content = re.sub(pattern2, replacement2, content)

# Update the game over text condition to check for game_has_been_played
pattern3 = r'if self\.game_over and hasattr\(self, \'score\'\) and self\.score > 0:'
replacement3 = r'if self.game_over and hasattr(self, \'game_has_been_played\') and self.game_has_been_played:'

content = re.sub(pattern3, replacement3, content)

# Write the modified content back to the file
with open('car_game_advanced_new.py', 'w') as file:
    file.write(content)

print("Added game_has_been_played flag to all game over instances")
