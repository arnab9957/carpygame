#!/usr/bin/env python3
import os

def fix_apply_setting():
    """Fix the apply_setting methods to properly handle fullscreen mode"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the apply_setting methods
    for i, line in enumerate(lines):
        if "def apply_setting(self, option):" in line:
            # Find the fullscreen mode line
            for j in range(i, len(lines)):
                if "pygame.FULLSCREEN" in lines[j]:
                    # Replace with improved fullscreen flags
                    lines[j] = lines[j].replace("pygame.FULLSCREEN", "pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF")
                    break
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("apply_setting methods fixed successfully!")

if __name__ == "__main__":
    fix_apply_setting()
