#!/usr/bin/env python3
import os
import sys

def add_sound_integration_to_game(game_file_path):
    """Add sound integration to the game file"""
    try:
        # Read the game file
        with open(game_file_path, 'r') as f:
            content = f.readlines()
        
        # Add import for sound engine
        import_line = "import sound_engine\n"
        
        # Find the import section
        import_section_end = 0
        for i, line in enumerate(content):
            if line.startswith('import ') or line.startswith('from '):
                import_section_end = i + 1
        
        # Insert sound engine import
        content.insert(import_section_end, import_line)
        
        # Add sound initialization to the beginning of the game
        init_line = "# Initialize sound engine\nsound_engine.initialize()\n"
        
        # Find the main section
        main_section = 0
        for i, line in enumerate(content):
            if "if __name__ == "__main__":" in line:
                main_section = i + 1
                break
        
        # Insert sound initialization
        content.insert(main_section, init_line)
        
        # Add sound cleanup to the end of the game
        cleanup_line = "    sound_engine.cleanup()\n"
        
        # Find the exit section
        exit_section = 0
        for i, line in enumerate(content):
            if "pygame.quit()" in line:
                exit_section = i
                break
        
        # Insert sound cleanup
        content.insert(exit_section, cleanup_line)
        
        # Add sound updates to the update method
        update_line = "            # Update engine sounds\n            sound_engine.update_engine_sound(self.speed, self.player_car.is_boosting)\n"
        
        # Find the update method
        update_section = 0
        update_found = False
        for i, line in enumerate(content):
            if "def update(self):" in line:
                update_section = i
                update_found = True
                break
        
        if update_found:
            # Find a good place to insert the sound update
            for i in range(update_section, len(content)):
                if "self.update_mission_progress()" in content[i]:
                    content.insert(i, update_line)
                    break
        
        # Add sound effects for collisions
        collision_line = "                        sound_engine.play_collision()\n"
        
        # Find collision sections
        for i, line in enumerate(content):
            if "self.game_over = True" in line and "collision" in content[i-1].lower():
                content.insert(i, collision_line)
        
        # Add sound effects for power-ups
        powerup_line = "                    sound_engine.play_powerup()\n"
        
        # Find power-up sections
        for i, line in enumerate(content):
            if "# Apply power-up effect" in line:
                content.insert(i+1, powerup_line)
        
        # Add sound effects for coins
        coin_line = "                    sound_engine.play_coin()\n"
        
        # Find coin sections
        for i, line in enumerate(content):
            if "self.coins_collected += 1" in line:
                content.insert(i+1, coin_line)
        
        # Write the modified content back to the file
        with open(game_file_path, 'w') as f:
            f.writelines(content)
        
        print(f"Successfully added sound integration to {game_file_path}")
        return True
    except Exception as e:
        print(f"Error adding sound integration: {e}")
        return False

if __name__ == "__main__":
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        sys.exit(1)
    
    print(f"Adding sound integration to {game_file}...")
    
    if add_sound_integration_to_game(game_file):
        print("Successfully added sound integration!")
        print("The game will now have dynamic engine sounds based on the car's speed.")
        print("Sound effects have been added for collisions, power-ups, and coins.")
    else:
        print("Failed to add sound integration.")
        sys.exit(1)
