#!/usr/bin/env python3
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
        """Load sound effects"""
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
        """Create dummy sound objects when sound files are missing"""
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
        """Update engine sound based on current speed"""
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
        """Play collision sound"""
        if self.sound_enabled:
            self.collision_sound.play()
    
    def play_powerup(self):
        """Play powerup sound"""
        if self.sound_enabled:
            self.powerup_sound.play()
    
    def play_coin(self):
        """Play coin sound"""
        if self.sound_enabled:
            self.coin_sound.play()
    
    def cleanup(self):
        """Stop all sounds and clean up"""
        if self.sound_enabled:
            pygame.mixer.stop()

# Create a global instance
sound_engine = None

def initialize():
    """Initialize the sound engine"""
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
    """Update engine sound based on speed"""
    global sound_engine
    if sound_engine:
        sound_engine.update_engine_sound(speed, is_boosting)

def play_collision():
    """Play collision sound"""
    global sound_engine
    if sound_engine:
        sound_engine.play_collision()

def play_powerup():
    """Play powerup sound"""
    global sound_engine
    if sound_engine:
        sound_engine.play_powerup()

def play_coin():
    """Play coin sound"""
    global sound_engine
    if sound_engine:
        sound_engine.play_coin()

def cleanup():
    """Clean up sound engine"""
    global sound_engine
    if sound_engine:
        sound_engine.cleanup()
