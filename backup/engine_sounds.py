#!/usr/bin/env python3
import os
import sys
import wave
import array
import math

def create_dummy_sound_files():
    """Create basic dummy sound files for testing"""
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
        
        print("Created dummy sound files in 'sounds' directory")
        return True
    except Exception as e:
        print(f"Error creating dummy sound files: {e}")
        return False

def main():
    print("Creating dummy sound files for the car racing game...")
    
    if create_dummy_sound_files():
        print("Successfully created the following sound files in the 'sounds' directory:")
        print("- engine_idle.wav")
        print("- engine_low.wav")
        print("- engine_medium.wav")
        print("- engine_high.wav")
        print("- collision.wav")
        print("- powerup.wav")
        print("- coin.wav")
        print("\nYou can now use these sound files with the car racing game.")
        print("To use your own sound files, replace these files with your own WAV files.")
    else:
        print("Failed to create sound files.")

if __name__ == "__main__":
    main()
