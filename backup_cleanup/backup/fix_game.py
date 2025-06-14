#!/usr/bin/env python3
"""
Script to fix the car_game_advanced_new_optimized.py file
"""
import re
import sys
import os

def fix_game(filename):
    print(f"Fixing {filename}...")
    
    # Read the file
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix the create_crash method syntax error
    content = re.sub(
        r'self\.create_spark\(x, y, count=15\s+# Reduced for performance, intensity=1\.5\)',
        'self.create_spark(x, y, count=15, intensity=1.5)  # Reduced for performance',
        content
    )
    
    # Fix the create_smoke method syntax error
    content = re.sub(
        r'self\.create_smoke\(x, y, count=5\s+# Reduced for performance\)',
        'self.create_smoke(x, y, count=5)  # Reduced for performance',
        content
    )
    
    # Fix the background gradient indentation error in show_game_mode_menu
    pattern = r'# Create background with gradient as fallback\s+# Calculate gradient color'
    replacement = '# Create background with gradient as fallback\n            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))\n            for y in range(SCREEN_HEIGHT):\n                # Calculate gradient color'
    content = re.sub(pattern, replacement, content)
    
    # Write the fixed content back to a new file
    fixed_filename = filename.replace('.py', '_fixed.py')
    with open(fixed_filename, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Fixed file saved as {fixed_filename}")
    return fixed_filename

if __name__ == "__main__":
    if len(sys.argv) > 1:
        fix_game(sys.argv[1])
    else:
        fix_game("car_game_advanced_new_optimized.py")
