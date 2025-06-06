#!/usr/bin/env python3

import re

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    content = file.read()

# Pattern for name input background
name_input_pattern = r'(def show_name_input.*?# Draw background\n\s+)(self\.screen\.blit\(background, \(0, 0\)\))'
name_input_replacement = r'\1if has_background_image:\n                # Use the loaded image as background\n                self.screen.blit(background_image, (0, 0))\n                \n                # Add a semi-transparent overlay to make text more readable\n                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)\n                overlay.fill((0, 0, 0, 120))  # Semi-transparent black\n                self.screen.blit(overlay, (0, 0))\n            else:\n                # Use the gradient background\n                self.screen.blit(background, (0, 0))'

# Pattern for high scores background
highscores_pattern = r'(def show_highscores.*?# Draw background\n\s+)(self\.screen\.blit\(background, \(0, 0\)\))'
highscores_replacement = r'\1if has_background_image:\n                # Use the loaded image as background\n                self.screen.blit(background_image, (0, 0))\n                \n                # Add a semi-transparent overlay to make text more readable\n                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)\n                overlay.fill((0, 0, 0, 120))  # Semi-transparent black\n                self.screen.blit(overlay, (0, 0))\n            else:\n                # Use the gradient background\n                self.screen.blit(background, (0, 0))'

# Apply the replacements
content = re.sub(name_input_pattern, name_input_replacement, content, flags=re.DOTALL)
content = re.sub(highscores_pattern, highscores_replacement, content, flags=re.DOTALL)

# Write the modified content back to the file
with open('car_game_advanced_new.py', 'w') as file:
    file.write(content)

print("Background image code added to name input and high scores screens")
