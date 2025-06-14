#!/usr/bin/env python3
import os
import sys
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

def main():
    print("Creating sound files for the car racing game...")
    
    if create_sound_files():
        print("Successfully created the following sound files in the 'sounds' directory:")
        print("- engine_idle.wav")
        print("- engine_low.wav")
        print("- engine_medium.wav")
        print("- engine_high.wav")
        print("- collision.wav")
        print("- powerup.wav")
        print("- coin.wav")
        print("\nYou can now use these sound files with the car racing game.")
        
        # Create the sound engine module
        with open('sound_engine.py', 'w') as f:
            f.write("""#!/usr/bin/env python3
import pygame
import os
import sys

class SoundEngine:
    def __init__(self):
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except:
            print("Warning: Could not initialize sound mixer")
            self.sound_enabled = False
        
        # Load sounds
        self.load_sounds()
        
        # Current speed
        self.speed = 0
        self.max_speed = 15
        self.is_boosting = False
    
    def load_sounds(self):
        \"\"\"Load sound effects\"\"\"
        if not self.sound_enabled:
            self._create_dummy_sounds()
            return
            
        try:
            # Check if sound files exist
            required_sounds = ['engine_idle.wav', 'engine_low.wav', 'engine_medium.wav', 
                              'engine_high.wav', 'collision.wav', 'powerup.wav', 'coin.wav']
            
            missing_files = False
            for sound_file in required_sounds:
                if not os.path.exists(f'sounds/{sound_file}'):
                    print(f"Warning: Sound file 'sounds/{sound_file}' not found.")
                    missing_files = True
            
            if missing_files:
                print("Some sound files are missing. Using dummy sounds.")
                self._create_dummy_sounds()
                return
            
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
            self._create_dummy_sounds()
    
    def _create_dummy_sounds(self):
        \"\"\"Create dummy sound objects when sound files are missing\"\"\"
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
        print("Using dummy sounds (no audio)")
    
    def update_engine_sound(self, speed, is_boosting=False):
        \"\"\"Update engine sound based on current speed\"\"\"
        if not self.sound_enabled:
            return
            
        try:
            self.speed = speed
            self.is_boosting = is_boosting
            
            # Calculate speed ratio (0 to 1)
            speed_ratio = min(self.speed / self.max_speed, 1.0)
            
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
            if self.is_boosting:
                # Increase high engine sound for boost effect
                self.engine_high_sound.set_volume(min(0.8, self.engine_high_sound.get_volume() + 0.2))
        except Exception as e:
            print(f"Error updating engine sound: {e}")
    
    def play_collision(self):
        \"\"\"Play collision sound\"\"\"
        if self.sound_enabled:
            self.collision_sound.play()
    
    def play_powerup(self):
        \"\"\"Play powerup sound\"\"\"
        if self.sound_enabled:
            self.powerup_sound.play()
    
    def play_coin(self):
        \"\"\"Play coin sound\"\"\"
        if self.sound_enabled:
            self.coin_sound.play()
    
    def cleanup(self):
        \"\"\"Stop all sounds and clean up\"\"\"
        if self.sound_enabled:
            pygame.mixer.stop()

# Create a global instance
sound_engine = None

def initialize():
    \"\"\"Initialize the sound engine\"\"\"
    global sound_engine
    if sound_engine is None:
        try:
            pygame.init()
            sound_engine = SoundEngine()
            return True
        except Exception as e:
            print(f"Error initializing sound engine: {e}")
            return False
    return True

def update_engine_sound(speed, is_boosting=False):
    \"\"\"Update engine sound based on speed\"\"\"
    global sound_engine
    if sound_engine:
        sound_engine.update_engine_sound(speed, is_boosting)

def play_collision():
    \"\"\"Play collision sound\"\"\"
    global sound_engine
    if sound_engine:
        sound_engine.play_collision()

def play_powerup():
    \"\"\"Play powerup sound\"\"\"
    global sound_engine
    if sound_engine:
        sound_engine.play_powerup()

def play_coin():
    \"\"\"Play coin sound\"\"\"
    global sound_engine
    if sound_engine:
        sound_engine.play_coin()

def cleanup():
    \"\"\"Clean up sound engine\"\"\"
    global sound_engine
    if sound_engine:
        sound_engine.cleanup()
""")
        
        # Create the game integration file
        with open('game_sound_integration.py', 'w') as f:
            f.write("""#!/usr/bin/env python3
import os
import sys

def add_sound_integration_to_game(game_file_path):
    \"\"\"Add sound integration to the game file\"\"\"
    try:
        # Read the game file
        with open(game_file_path, 'r') as f:
            content = f.readlines()
        
        # Add import for sound engine
        import_line = "import sound_engine\\n"
        
        # Find the import section
        import_section_end = 0
        for i, line in enumerate(content):
            if line.startswith('import ') or line.startswith('from '):
                import_section_end = i + 1
        
        # Insert sound engine import
        content.insert(import_section_end, import_line)
        
        # Add sound initialization to the beginning of the game
        init_line = "# Initialize sound engine\\nsound_engine.initialize()\\n"
        
        # Find the main section
        main_section = 0
        for i, line in enumerate(content):
            if "if __name__ == \"__main__\":" in line:
                main_section = i + 1
                break
        
        # Insert sound initialization
        content.insert(main_section, init_line)
        
        # Add sound cleanup to the end of the game
        cleanup_line = "    sound_engine.cleanup()\\n"
        
        # Find the exit section
        exit_section = 0
        for i, line in enumerate(content):
            if "pygame.quit()" in line:
                exit_section = i
                break
        
        # Insert sound cleanup
        content.insert(exit_section, cleanup_line)
        
        # Add sound updates to the update method
        update_line = "            # Update engine sounds\\n            sound_engine.update_engine_sound(self.speed, self.player_car.is_boosting)\\n"
        
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
        collision_line = "                        sound_engine.play_collision()\\n"
        
        # Find collision sections
        for i, line in enumerate(content):
            if "self.game_over = True" in line and "collision" in content[i-1].lower():
                content.insert(i, collision_line)
        
        # Add sound effects for power-ups
        powerup_line = "                    sound_engine.play_powerup()\\n"
        
        # Find power-up sections
        for i, line in enumerate(content):
            if "# Apply power-up effect" in line:
                content.insert(i+1, powerup_line)
        
        # Add sound effects for coins
        coin_line = "                    sound_engine.play_coin()\\n"
        
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
""")
        
        print("\nCreated sound engine module (sound_engine.py) and integration script (game_sound_integration.py).")
        print("To integrate sounds into your game, run:")
        print("  python3 game_sound_integration.py")
    else:
        print("Failed to create sound files.")

if __name__ == "__main__":
    main()
