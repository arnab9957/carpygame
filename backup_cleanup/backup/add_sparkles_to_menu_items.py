#!/usr/bin/env python3
import os

def add_sparkles_to_menu_items():
    """Add sparkle effects to menu items"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the show_menu method
    show_menu_start = -1
    for i, line in enumerate(lines):
        if "def show_menu(self):" in line:
            show_menu_start = i
            break
    
    if show_menu_start == -1:
        print("Could not find show_menu method!")
        return
    
    # Find the menu button drawing section
    menu_buttons_start = -1
    for i in range(show_menu_start, len(lines)):
        if "# Draw menu buttons" in lines[i]:
            menu_buttons_start = i
            break
    
    if menu_buttons_start == -1:
        print("Could not find menu buttons section!")
        return
    
    # Find the end of the menu button drawing section
    menu_buttons_end = -1
    for i in range(menu_buttons_start, len(lines)):
        if "self.screen.blit(option_text, option_rect)" in lines[i]:
            menu_buttons_end = i + 1
            break
    
    if menu_buttons_end == -1:
        print("Could not find end of menu buttons section!")
        return
    
    # Create the sparkle effect code for menu items
    sparkle_effect_code = [
        "                # Add sparkle effect around menu items\n",
        "                if is_hovering:\n",
        "                    # Create sparkles around the button when hovering\n",
        "                    for _ in range(2):  # Add 2 sparkles per frame when hovering\n",
        "                        # Calculate random position around the button\n",
        "                        sparkle_x = button_rect.x + random.randint(-10, button_rect.width + 10)\n",
        "                        sparkle_y = button_rect.y + random.randint(-10, button_rect.height + 10)\n",
        "                        \n",
        "                        # Add sparkle with color matching the button\n",
        "                        self.sparkles.append({\n",
        "                            \"x\": sparkle_x,\n",
        "                            \"y\": sparkle_y,\n",
        "                            \"size\": random.uniform(1, 3),\n",
        "                            \"color\": hover_color,\n",
        "                            \"brightness\": random.uniform(0.5, 1.0),\n",
        "                            \"twinkle_speed\": random.uniform(3, 8),\n",
        "                            \"twinkle_offset\": random.uniform(0, 2 * math.pi),\n",
        "                        })\n",
        "\n"
    ]
    
    # Insert the sparkle effect code
    for i, line in enumerate(sparkle_effect_code):
        lines.insert(menu_buttons_end + i, line)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("Sparkle effects added to menu items successfully!")

if __name__ == "__main__":
    add_sparkles_to_menu_items()
