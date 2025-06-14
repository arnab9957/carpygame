#!/usr/bin/env python3
import os
import sys
import re

def fix_syntax_error(file_path):
    """Fix the syntax error in the game file"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the problematic code in __init__ method
        init_pattern = r'def __init__\(self\):.*?try:.*?self\.reset_game\(\)'
        init_match = re.search(init_pattern, content, re.DOTALL)
        
        if not init_match:
            print("Error: Could not find __init__ method with try block")
            return False
        
        old_init = init_match.group(0)
        
        # Check if there's a try block without except
        if "try:" in old_init and "except" not in old_init:
            # Add except block
            fixed_init = old_init.replace(
                "self.reset_game()",
                "self.reset_game()\n        except Exception as e:\n            print(f\"Error in __init__: {e}\")\n            traceback.print_exc()"
            )
            
            content = content.replace(old_init, fixed_init)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("Successfully fixed syntax error in __init__ method")
        return True
    
    except Exception as e:
        print(f"Error fixing syntax error: {e}")
        return False

def main():
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        return
    
    print(f"Fixing syntax error in {game_file}...")
    
    if not fix_syntax_error(game_file):
        print("Failed to fix syntax error")
        return
    
    print("Successfully fixed syntax error!")
    print("You can now run the game with engine sounds.")

if __name__ == "__main__":
    main()
