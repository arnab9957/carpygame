#!/usr/bin/env python3
import os

def fix_menu_item_sparkles():
    """Fix the sparkle effect for menu items"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the menu item sparkle code
    menu_item_sparkle_start = -1
    for i, line in enumerate(lines):
        if "# Add sparkle effect around menu items" in line:
            menu_item_sparkle_start = i
            break
    
    if menu_item_sparkle_start == -1:
        print("Could not find menu item sparkle code!")
        return
    
    # Find the sparkle creation section in menu items
    menu_sparkle_creation_start = -1
    for i in range(menu_item_sparkle_start, len(lines)):
        if "self.sparkles.append({" in lines[i]:
            menu_sparkle_creation_start = i
            break
    
    if menu_sparkle_creation_start == -1:
        print("Could not find menu sparkle creation section!")
        return
    
    # Find the end of the menu sparkle creation section
    menu_sparkle_creation_end = -1
    for i in range(menu_sparkle_creation_start, len(lines)):
        if "})" in lines[i]:
            menu_sparkle_creation_end = i + 1
            break
    
    if menu_sparkle_creation_end == -1:
        print("Could not find end of menu sparkle creation section!")
        return
    
    # Create the updated menu sparkle creation code
    updated_menu_sparkle_code = [
        "                        self.sparkles.append({\n",
        "                            \"x\": sparkle_x,\n",
        "                            \"y\": sparkle_y,\n",
        "                            \"direction\": random.uniform(0, 2 * math.pi),\n",
        "                            \"speed\": random.uniform(0.2, 1.0),\n",
        "                            \"color\": hover_color,\n",
        "                            \"size\": random.uniform(1, 3),\n",
        "                            \"brightness\": random.uniform(0.5, 1.0),\n",
        "                            \"twinkle_speed\": random.uniform(3, 8),\n",
        "                            \"twinkle_offset\": random.uniform(0, 2 * math.pi),\n",
        "                        })\n"
    ]
    
    # Replace the menu sparkle creation section
    lines[menu_sparkle_creation_start:menu_sparkle_creation_end] = updated_menu_sparkle_code
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("Menu item sparkle code fixed successfully!")

if __name__ == "__main__":
    fix_menu_item_sparkles()
