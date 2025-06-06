#!/usr/bin/env python3
import os

def fix_garage_indentation():
    """Fix the indentation in the garage menu method"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the garage menu method
    garage_start = -1
    for i, line in enumerate(lines):
        if "def show_garage_menu(self, background_surface):" in line:
            garage_start = i
            break
    
    if garage_start == -1:
        print("Could not find garage menu method!")
        return
    
    # Fix indentation for all lines in the method
    i = garage_start + 1
    while i < len(lines):
        line = lines[i]
        if line.strip() and not line.startswith(" " * 8):  # If line is not properly indented
            if "def " in line:  # We've reached the next method
                break
            # Add proper indentation (8 spaces)
            lines[i] = " " * 8 + line.lstrip()
        i += 1
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("Garage menu indentation fixed successfully!")

if __name__ == "__main__":
    fix_garage_indentation()
