"""
This script runs all the update scripts to add animations to the car_game.py file.
"""

import os
import sys
import importlib.util

def run_script(script_path):
    """Run a Python script by path"""
    print(f"Running {script_path}...")
    
    # Load the script as a module
    spec = importlib.util.spec_from_file_location("module.name", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Find the main function and run it
    if hasattr(module, "__main__"):
        getattr(module, "__main__")()
    else:
        # Try to find a function that matches the script name
        script_name = os.path.basename(script_path).replace(".py", "")
        if hasattr(module, script_name):
            getattr(module, script_name)()
        else:
            print(f"Could not find main function in {script_path}")

def main():
    # Directory containing the scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List of scripts to run in order
    scripts = [
        "add_animation_method.py",
        "update_left_key.py",
        "update_right_key.py",
        "update_mouse_click.py",
        "add_pulsating_highlight.py",
        "update_draw_to_surface.py"
    ]
    
    # Run each script
    for script in scripts:
        script_path = os.path.join(script_dir, script)
        if os.path.exists(script_path):
            run_script(script_path)
        else:
            print(f"Script {script_path} not found")
    
    print("\nAll updates completed! The car_game.py file has been modified with animations.")
    print("Run the game to see the animations in action:")
    print("python car_game.py")

if __name__ == "__main__":
    main()
