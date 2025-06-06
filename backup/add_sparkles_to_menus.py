#!/usr/bin/env python3
import os
import re

def add_sparkles_to_menus():
    """Add sparkle animations to all menu screens"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to find background drawing sections without sparkles
    pattern = r'(# Draw background.*?if has_background_image:.*?# Add a semi-transparent overlay.*?self\.screen\.blit\(overlay, \(0, 0\)\))(.*?)(\s+else:\s+# Use the gradient background)'
    
    # Replacement with sparkles added
    replacement = r'\1\n                \n                # Draw sparkles animation\n                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation\n                self.draw_sparkles(self.screen)\2\3'
    
    # Apply the replacement
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print("Sparkle animations added to all menu screens successfully!")

if __name__ == "__main__":
    add_sparkles_to_menus()
