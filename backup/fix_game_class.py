#!/usr/bin/env python3
import os
import sys
import re

def fix_game_class(file_path):
    """Fix the Game class definition in the file"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if the Game class is defined
        if "class Game:" not in content:
            print("Error: Game class not found in the file")
            
            # Try to find the class definition that might be broken
            class_def_pattern = r'class\s+\w+:'
            class_matches = re.findall(class_def_pattern, content)
            
            print(f"Found class definitions: {class_matches}")
            
            # Add the Game class definition
            game_class_def = """
class Game:
    def __init__(self):
        try:
            # Create a resizable window with error handling
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            pygame.display.set_caption("Car Racing Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont(None, 36)
            self.particle_system = ParticleSystem()
            self.highscore_manager = HighScoreManager()
            
            # Load engine sounds
            self.load_sounds()
            
            # Day-night cycle variables
            self.cycle_time = 0
            self.day_phase = 0  # 0 = day, 0.25 = sunset, 0.5 = night, 0.75 = sunrise
            self.stars = []
            self.generate_stars()
            
            self.reset_game()
        except Exception as e:
            print(f"Error initializing game: {e}")
            traceback.print_exc()
            pygame.quit()
            sys.exit(1)
"""
            
            # Find a good position to insert the Game class
            # Look for the last class definition before the main code
            last_class_pos = content.rfind("class ")
            if last_class_pos != -1:
                # Find the end of this class definition
                next_class_pos = content.find("class ", last_class_pos + 1)
                if next_class_pos == -1:
                    # This is the last class, insert Game class after it
                    # Find the end of the class by looking for the next def outside the class
                    class_end_pos = content.find("\ndef ", last_class_pos)
                    if class_end_pos == -1:
                        class_end_pos = len(content)
                    
                    # Insert the Game class
                    updated_content = content[:class_end_pos] + "\n" + game_class_def + content[class_end_pos:]
                else:
                    # Insert before the next class
                    updated_content = content[:next_class_pos] + game_class_def + content[next_class_pos:]
            else:
                # No classes found, add at the beginning
                updated_content = game_class_def + content
            
            # Write the updated content back to the file
            with open(file_path, 'w') as f:
                f.write(updated_content)
            
            print("Added Game class definition")
            return True
        
        return True
    
    except Exception as e:
        print(f"Error fixing Game class: {e}")
        return False

def main():
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        return
    
    print(f"Fixing Game class in {game_file}...")
    
    # Fix Game class
    if not fix_game_class(game_file):
        print("Failed to fix Game class")
        return
    
    print("Successfully fixed Game class!")

if __name__ == "__main__":
    main()
