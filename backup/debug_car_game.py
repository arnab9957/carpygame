#!/usr/bin/env python3
import traceback
import sys

try:
    print("Attempting to import car_game_advanced_new...")
    import car_game_advanced_new
    print("Import successful!")
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
