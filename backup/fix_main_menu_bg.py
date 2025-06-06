#!/usr/bin/env python3
import os

def fix_main_menu_bg():
    """Fix the background size in the main menu"""
    
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
    
    # Find the "Draw background" section
    draw_bg_start = -1
    for i in range(show_menu_start, len(lines)):
        if "# Draw background" in lines[i]:
            draw_bg_start = i
            break
    
    if draw_bg_start == -1:
        print("Could not find 'Draw background' section!")
        return
    
    # Find the end of the background drawing section
    draw_bg_end = -1
    for i in range(draw_bg_start, len(lines)):
        if "# Draw title with glow effect" in lines[i]:
            draw_bg_end = i
            break
    
    if draw_bg_end == -1:
        print("Could not find end of background drawing section!")
        return
    
    # Create the updated background drawing code
    updated_bg_code = [
        "            # Draw background\n",
        "            if has_background_image:\n",
        "                # Use the loaded image as background\n",
        "                # Get current screen dimensions to ensure proper scaling\n",
        "                current_width = self.screen.get_width()\n",
        "                current_height = self.screen.get_height()\n",
        "                \n",
        "                # Check if the background image needs to be rescaled\n",
        "                if background_image.get_width() != current_width or background_image.get_height() != current_height:\n",
        "                    background_image = pygame.transform.scale(background_image, (current_width, current_height))\n",
        "                    print(f\"Background image rescaled to {current_width}x{current_height}\")\n",
        "                \n",
        "                self.screen.blit(background_image, (0, 0))\n",
        "                \n",
        "                # Add a semi-transparent overlay to make text more readable\n",
        "                overlay = pygame.Surface((current_width, current_height), pygame.SRCALPHA)\n",
        "                overlay.fill((0, 0, 0, 120))  # Semi-transparent black\n",
        "                self.screen.blit(overlay, (0, 0))\n",
        "                \n",
        "                # Draw sparkles animation\n",
        "                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation\n",
        "                self.draw_sparkles(self.screen)\n",
        "            else:\n",
        "                # Use the gradient background\n",
        "                self.screen.blit(background, (0, 0))\n",
        "\n"
    ]
    
    # Replace the background drawing section
    lines[draw_bg_start:draw_bg_end] = updated_bg_code
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("Main menu background size fix applied successfully!")

if __name__ == "__main__":
    fix_main_menu_bg()
