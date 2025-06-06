#!/usr/bin/env python3
import os
import sys
import re
import wave
import array
import math

def create_sound_files():
    """Create basic sound files for the game"""
    try:
        # Create sounds directory
        os.makedirs('sounds', exist_ok=True)
        
        # Function to create a simple sine wave sound
        def create_sine_wave(filename, frequency, duration, volume=0.5):
            sample_rate = 44100
            num_samples = int(duration * sample_rate)
            
            # Create sine wave data
            data = array.array('h')
            for i in range(num_samples):
                sample = int(volume * 32767.0 * 
                             math.sin(2 * math.pi * frequency * i / sample_rate))
                data.append(sample)
            
            # Write to WAV file
            with wave.open(f'sounds/{filename}', 'w') as f:
                f.setnchannels(1)  # Mono
                f.setsampwidth(2)  # 2 bytes per sample
                f.setframerate(sample_rate)
                f.writeframes(data.tobytes())
        
        # Create different engine sounds
        create_sine_wave('engine_idle.wav', 100, 1.0, 0.3)    # Low frequency for idle
        create_sine_wave('engine_low.wav', 150, 1.0, 0.4)     # Slightly higher for low speed
        create_sine_wave('engine_medium.wav', 200, 1.0, 0.5)  # Medium frequency
        create_sine_wave('engine_high.wav', 300, 1.0, 0.6)    # High frequency for high speed
        
        # Create effect sounds
        create_sine_wave('collision.wav', 80, 0.5, 0.7)       # Low frequency burst for collision
        create_sine_wave('powerup.wav', 440, 0.3, 0.5)        # High pitch for powerup
        create_sine_wave('coin.wav', 600, 0.2, 0.4)           # Short high pitch for coin
        
        print("Created sound files in 'sounds' directory")
        return True
    except Exception as e:
        print(f"Error creating sound files: {e}")
        return False

def modify_game_file(file_path):
    """Modify the game file to add sound functionality"""
    try:
        # Read the file content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # 1. Add pygame mixer initialization
        pygame_init_pattern = r'# Initialize pygame\npygame\.init\(\)'
        pygame_init_replacement = """# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound effects"""
        
        content = content.replace(pygame_init_pattern, pygame_init_replacement)
        
        # 2. Add sound loading to Game.__init__
        game_init_pattern = r'def __init__\(self\):.*?self\.reset_game\(\)'
        game_init_match = re.search(game_init_pattern, content, re.DOTALL)
        
        if not game_init_match:
            print("Error: Could not find Game.__init__ method")
            return False
        
        old_init = game_init_match.group(0)
        new_init = old_init.replace(
            "self.reset_game()",
            """# Load engine sounds
        self.load_sounds()
        
        self.reset_game()"""
        )
        
        content = content.replace(old_init, new_init)
        
        # 3. Add load_sounds method after reset_game method
        reset_game_pattern = r'def reset_game\(self\):.*?self\.set_mission\(\)'
        reset_game_match = re.search(reset_game_pattern, content, re.DOTALL)
        
        if not reset_game_match:
            print("Error: Could not find reset_game method")
            return False
        
        old_reset = reset_game_match.group(0)
        
        load_sounds_method = """
    def load_sounds(self):
        \"\"\"Load sound effects for the game\"\"\"
        try:
            # Engine sounds at different speeds
            self.engine_idle_sound = pygame.mixer.Sound('sounds/engine_idle.wav')
            self.engine_low_sound = pygame.mixer.Sound('sounds/engine_low.wav')
            self.engine_medium_sound = pygame.mixer.Sound('sounds/engine_medium.wav')
            self.engine_high_sound = pygame.mixer.Sound('sounds/engine_high.wav')
            
            # Set initial volumes
            self.engine_idle_sound.set_volume(0.3)
            self.engine_low_sound.set_volume(0.0)
            self.engine_medium_sound.set_volume(0.0)
            self.engine_high_sound.set_volume(0.0)
            
            # Start playing engine sounds in loops
            self.engine_idle_sound.play(-1)  # -1 means loop indefinitely
            self.engine_low_sound.play(-1)
            self.engine_medium_sound.play(-1)
            self.engine_high_sound.play(-1)
            
            # Other game sounds
            self.collision_sound = pygame.mixer.Sound('sounds/collision.wav')
            self.powerup_sound = pygame.mixer.Sound('sounds/powerup.wav')
            self.coin_sound = pygame.mixer.Sound('sounds/coin.wav')
            
            print("Game sounds loaded successfully")
        except Exception as e:
            print(f"Error loading sounds: {e}")
            print("Continuing without sound effects")
            # Create dummy sound objects to prevent errors
            class DummySound:
                def play(self, *args): pass
                def stop(self): pass
                def set_volume(self, vol): pass
            
            self.engine_idle_sound = DummySound()
            self.engine_low_sound = DummySound()
            self.engine_medium_sound = DummySound()
            self.engine_high_sound = DummySound()
            self.collision_sound = DummySound()
            self.powerup_sound = DummySound()
            self.coin_sound = DummySound()
    
    def update_engine_sound(self):
        \"\"\"Update engine sound based on current speed\"\"\"
        try:
            # Calculate speed ratio (0 to 1)
            max_speed = 15  # Maximum speed value
            speed_ratio = min(self.speed / max_speed, 1.0)
            
            # Set volumes based on speed
            if speed_ratio < 0.2:  # Idle or very slow
                self.engine_idle_sound.set_volume(0.3 - speed_ratio)
                self.engine_low_sound.set_volume(speed_ratio * 2)
                self.engine_medium_sound.set_volume(0.0)
                self.engine_high_sound.set_volume(0.0)
            elif speed_ratio < 0.5:  # Low to medium speed
                self.engine_idle_sound.set_volume(0.0)
                self.engine_low_sound.set_volume(0.4 - (speed_ratio - 0.2) * 2)
                self.engine_medium_sound.set_volume((speed_ratio - 0.2) * 2)
                self.engine_high_sound.set_volume(0.0)
            else:  # High speed
                self.engine_idle_sound.set_volume(0.0)
                self.engine_low_sound.set_volume(0.0)
                self.engine_medium_sound.set_volume(0.4 - (speed_ratio - 0.5) * 0.8)
                self.engine_high_sound.set_volume((speed_ratio - 0.5) * 0.8)
                
            # Add boost effect if boosting
            if self.player_car.is_boosting:
                # Increase high engine sound for boost effect
                self.engine_high_sound.set_volume(min(0.8, self.engine_high_sound.get_volume() + 0.2))
        except Exception as e:
            print(f"Error updating engine sound: {e}")"""
        
        content = content.replace(old_reset, old_reset + load_sounds_method)
        
        # 4. Add engine sound update call to the update method
        update_pattern = r'def update\(self\):.*?# Update mission progress\s+self\.update_mission_progress\(\)'
        update_match = re.search(update_pattern, content, re.DOTALL)
        
        if not update_match:
            print("Error: Could not find the update method")
            return False
        
        old_update = update_match.group(0)
        update_insertion_point = old_update.find("# Update mission progress")
        
        new_update = old_update[:update_insertion_point] + "            # Update engine sounds based on speed\n            self.update_engine_sound()\n\n            " + old_update[update_insertion_point:]
        
        content = content.replace(old_update, new_update)
        
        # 5. Add collision sound
        collision_pattern = r'# Create crash effect\n                        self\.particle_system\.create_crash\(self\.player_car\.x, self\.player_car\.y\)\n                        self\.game_over = True'
        collision_with_sound = """# Create crash effect
                        self.particle_system.create_crash(self.player_car.x, self.player_car.y)
                        # Play collision sound
                        self.collision_sound.play()
                        self.game_over = True"""
        
        content = content.replace(collision_pattern, collision_with_sound)
        
        # 6. Add powerup sound
        powerup_pattern = r'# Apply power-up effect\n                    if powerup\.type == \'boost\':'
        powerup_with_sound = """# Play powerup sound
                    self.powerup_sound.play()
                    
                    # Apply power-up effect
                    if powerup.type == 'boost':"""
        
        content = content.replace(powerup_pattern, powerup_with_sound)
        
        # 7. Add coin sound
        coin_pattern = r'coin\.collect\(\)\n                    self\.coins\.remove\(coin\)\n                    self\.coins_collected \+= 1'
        coin_with_sound = """coin.collect()
                    self.coins.remove(coin)
                    self.coins_collected += 1
                    # Play coin sound
                    self.coin_sound.play()"""
        
        content = content.replace(coin_pattern, coin_with_sound)
        
        # 8. Add cleanup in the run method's finally block
        run_finally_pattern = r'finally:\n            pygame\.quit\(\)\n            sys\.exit\(\)'
        run_finally_with_cleanup = """finally:
            # Stop all sounds
            try:
                pygame.mixer.stop()
            except:
                pass
            pygame.quit()
            sys.exit()"""
        
        content = content.replace(run_finally_pattern, run_finally_with_cleanup)
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("Successfully modified game file to add sound functionality")
        return True
    
    except Exception as e:
        print(f"Error modifying game file: {e}")
        return False

def main():
    game_file = '/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py'
    
    if not os.path.exists(game_file):
        print(f"Error: Game file not found at {game_file}")
        return
    
    print("Creating sound files...")
    if not create_sound_files():
        print("Failed to create sound files")
        return
    
    print(f"Implementing engine sounds in {game_file}...")
    if not modify_game_file(game_file):
        print("Failed to implement engine sounds")
        return
    
    print("Successfully implemented engine sounds that vary with speed!")
    print("The game will now have dynamic engine sounds based on the car's speed.")
    print("Sound effects have been added for collisions, power-ups, and coins.")

if __name__ == "__main__":
    main()
