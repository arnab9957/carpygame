#!/usr/bin/env python3
import os
import sys

def fix_indentation(file_path):
    """Fix indentation issues in the game file"""
    try:
        # Read the game file
        with open(file_path, 'r') as f:
            content = f.readlines()
        
        # Find and fix indentation issues
        fixed_content = []
        in_finally_block = False
        
        for line in content:
            # Check if we're entering a finally block
            if "finally:" in line:
                in_finally_block = True
                fixed_content.append(line)
                continue
            
            # Check if we're in a finally block and need to fix indentation
            if in_finally_block and "sound_engine.cleanup()" in line:
                # Fix indentation to match the finally block
                fixed_line = line.lstrip()  # Remove leading whitespace
                fixed_line = "        " + fixed_line  # Add correct indentation
                fixed_content.append(fixed_line)
            else:
                fixed_content.append(line)
        
        # Write the fixed content back to the file
        with open(file_path, 'w') as f:
            f.writelines(fixed_content)
        
        print(f"Successfully fixed indentation issues in {file_path}")
        return True
    except Exception as e:
        print(f"Error fixing indentation: {e}")
        return False

if __name__ == "__main__":
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        sys.exit(1)
    
    print(f"Fixing indentation issues in {game_file}...")
    
    if fix_indentation(game_file):
        print("Successfully fixed indentation issues!")
        print("You can now run the game with engine sounds.")
    else:
        print("Failed to fix indentation issues.")
        sys.exit(1)
