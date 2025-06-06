#!/usr/bin/env python3
import traceback
import sys

try:
    print("Attempting to run car_game_advanced_new...")
    import car_game_advanced_new
    
    # Create and run the game
    print("Creating game instance...")
    game = car_game_advanced_new.Game()
    print("Running game...")
    game.run()
    print("Game exited normally")
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
