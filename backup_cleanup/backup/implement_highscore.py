#!/usr/bin/env python3
import os
import sys
import re

def update_highscore_manager(file_path):
    """Update the HighScoreManager class in the game file"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Load the new HighScoreManager implementation
        with open('fixed_highscore.py', 'r') as f:
            new_highscore_manager = f.read()
        
        # Extract just the HighScoreManager class
        highscore_class_match = re.search(r'class HighScoreManager:.*?def _get_mode_key\(self.*?\).*?return "endless".*?# Default', 
                                         new_highscore_manager, re.DOTALL)
        
        if not highscore_class_match:
            print("Error: Could not find HighScoreManager class in the new implementation")
            return False
        
        new_highscore_class = highscore_class_match.group(0)
        
        # Find the existing HighScoreManager class in the game file
        highscore_pattern = r'class HighScoreManager:.*?def _get_mode_key\(self.*?\).*?return "endless".*?# Default'
        
        # Replace the old implementation with the new one
        updated_content = re.sub(highscore_pattern, new_highscore_class, content, flags=re.DOTALL)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        print("Successfully updated HighScoreManager class")
        return True
    
    except Exception as e:
        print(f"Error updating HighScoreManager: {e}")
        return False

def add_game_over_screen(file_path):
    """Add the game over screen implementation to the game file"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Load the game over screen implementation
        with open('game_over_screen.py', 'r') as f:
            game_over_screen = f.read()
        
        # Extract the show_game_over function
        show_game_over_match = re.search(r'def show_game_over\(.*?\):.*?waiting = False', 
                                        game_over_screen, re.DOTALL)
        
        if not show_game_over_match:
            print("Error: Could not find show_game_over function")
            return False
        
        show_game_over_func = show_game_over_match.group(0)
        
        # Extract the get_player_name function
        get_player_name_match = re.search(r'def get_player_name\(.*?\):.*?return text', 
                                         game_over_screen, re.DOTALL)
        
        if not get_player_name_match:
            print("Error: Could not find get_player_name function")
            return False
        
        get_player_name_func = get_player_name_match.group(0)
        
        # Extract the show_highscores function
        show_highscores_match = re.search(r'def show_highscores\(.*?\):.*?clock\.tick\(30\)', 
                                         game_over_screen, re.DOTALL)
        
        if not show_highscores_match:
            print("Error: Could not find show_highscores function")
            return False
        
        show_highscores_func = show_highscores_match.group(0)
        
        # Convert these functions to methods of the Game class
        show_game_over_method = "    def show_game_over(self):\n        \"\"\"Show game over screen and handle high score if applicable\"\"\"\n" + \
                               show_game_over_func.replace("def show_game_over(screen, clock, score, distance_traveled, coins_collected, game_mode, highscore_manager):", "").replace(
                                   "screen", "self.screen").replace(
                                   "clock", "self.clock").replace(
                                   "score", "self.score").replace(
                                   "distance_traveled", "self.distance_traveled").replace(
                                   "coins_collected", "self.coins_collected").replace(
                                   "game_mode", "self.game_mode").replace(
                                   "highscore_manager", "self.highscore_manager").replace(
                                   "get_player_name(", "self.get_player_name(").replace(
                                   "show_highscores(", "self.show_highscores(")
        
        get_player_name_method = "    def get_player_name(self):\n        \"\"\"Get player name for high score\"\"\"\n" + \
                                get_player_name_func.replace("def get_player_name(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT):", "").replace(
                                    "screen", "self.screen").replace(
                                    "clock", "self.clock").replace(
                                    "SCREEN_WIDTH", "SCREEN_WIDTH").replace(
                                    "SCREEN_HEIGHT", "SCREEN_HEIGHT")
        
        show_highscores_method = "    def show_highscores(self, player_name=None):\n        \"\"\"Show the high scores screen\"\"\"\n" + \
                                show_highscores_func.replace("def show_highscores(screen, clock, game_mode, highscore_manager, player_name=None):", "").replace(
                                    "screen", "self.screen").replace(
                                    "clock", "self.clock").replace(
                                    "game_mode", "self.game_mode").replace(
                                    "highscore_manager", "self.highscore_manager")
        
        # Find a good place to insert these methods (before the run method)
        run_method_pattern = r'    def run\(self\):'
        run_method_match = re.search(run_method_pattern, content)
        
        if not run_method_match:
            print("Error: Could not find run method in the game file")
            return False
        
        insert_position = run_method_match.start()
        
        # Insert the new methods
        updated_content = content[:insert_position] + \
                         show_game_over_method + "\n\n" + \
                         get_player_name_method + "\n\n" + \
                         show_highscores_method + "\n\n" + \
                         content[insert_position:]
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        print("Successfully added game over screen methods")
        return True
    
    except Exception as e:
        print(f"Error adding game over screen: {e}")
        return False

def update_run_method(file_path):
    """Update the run method to show the game over screen"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the run method
        run_method_pattern = r'    def run\(self\):.*?while running:.*?if not self.game_over and running:.*?else:.*?in_menu = True'
        run_method_match = re.search(run_method_pattern, content, re.DOTALL)
        
        if not run_method_match:
            print("Error: Could not find the relevant part of the run method")
            return False
        
        old_run_code = run_method_match.group(0)
        
        # Replace with updated code that shows game over screen
        new_run_code = old_run_code.replace(
            "else:\n                        in_menu = True",
            "else:\n                        # Show game over screen if game is over\n                        if self.game_over:\n                            self.show_game_over()\n                        in_menu = True"
        )
        
        # Update the content
        updated_content = content.replace(old_run_code, new_run_code)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        print("Successfully updated run method")
        return True
    
    except Exception as e:
        print(f"Error updating run method: {e}")
        return False

def main():
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        return
    
    print(f"Updating high score system in {game_file}...")
    
    # Update the HighScoreManager class
    if not update_highscore_manager(game_file):
        print("Failed to update HighScoreManager class")
        return
    
    # Add game over screen methods
    if not add_game_over_screen(game_file):
        print("Failed to add game over screen methods")
        return
    
    # Update the run method
    if not update_run_method(game_file):
        print("Failed to update run method")
        return
    
    print("Successfully updated the high score system!")
    print("Now only scores that beat the current highest score will be recorded.")

if __name__ == "__main__":
    main()
