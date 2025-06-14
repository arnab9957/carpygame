#!/usr/bin/env python3
import os
import re

def fix_garage_menu():
    """Move the show_garage_menu method to the Game class"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the show_garage_menu method at the end of the file
    garage_menu_pattern = r'def show_garage_menu\(self, background_surface\):.*?clock\.tick\(60\)'
    garage_menu_match = re.search(garage_menu_pattern, content, re.DOTALL)
    
    if not garage_menu_match:
        print("Could not find show_garage_menu method!")
        return
    
    # Extract the method
    garage_menu_method = garage_menu_match.group(0)
    
    # Remove the method from the end of the file
    content = content.replace(garage_menu_method, '')
    
    # Find a good place to insert the method in the Game class
    # Let's look for the show_game_mode_menu method
    game_mode_menu_pattern = r'def show_game_mode_menu\(self\):'
    game_mode_menu_match = re.search(game_mode_menu_pattern, content)
    
    if not game_mode_menu_match:
        print("Could not find show_game_mode_menu method!")
        return
    
    # Insert the garage menu method before the game mode menu method
    insert_position = game_mode_menu_match.start()
    content = content[:insert_position] + "    " + garage_menu_method + "\n\n    " + content[insert_position:]
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("Garage menu method moved to Game class successfully!")

if __name__ == "__main__":
    fix_garage_menu()
