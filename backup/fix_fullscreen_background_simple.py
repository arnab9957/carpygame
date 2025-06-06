#!/usr/bin/env python3
import os

def fix_fullscreen_background():
    """Fix the background display when switching to fullscreen mode"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the SettingsMenu class
    settings_class_start = -1
    for i, line in enumerate(lines):
        if "class SettingsMenu:" in line:
            settings_class_start = i
            break
    
    if settings_class_start == -1:
        print("Could not find SettingsMenu class!")
        return
    
    # Find the apply_setting method
    apply_setting_start = -1
    for i in range(settings_class_start, len(lines)):
        if "def apply_setting(self, option):" in lines[i]:
            apply_setting_start = i
            break
    
    if apply_setting_start == -1:
        print("Could not find apply_setting method!")
        return
    
    # Find the font update section in fullscreen mode
    fullscreen_on_section = -1
    for i in range(apply_setting_start, len(lines)):
        if "# Update fonts for new screen size" in lines[i] and fullscreen_on_section == -1:
            fullscreen_on_section = i
    
    if fullscreen_on_section == -1:
        print("Could not find font update section in fullscreen mode!")
        return
    
    # Find the end of the font update section
    font_update_end = -1
    for i in range(fullscreen_on_section, len(lines)):
        if "print(f\"Switched to fullscreen mode:" in lines[i]:
            font_update_end = i
            break
    
    if font_update_end == -1:
        print("Could not find end of font update section!")
        return
    
    # Replace the font update section with updated code
    new_font_section = [
        "                # Update fonts for new screen size\n",
        "                self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n",
        "                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n",
        "                self.font_small = get_font(int(self.screen_height * 0.03))\n",
        "                \n",
        "                # Recreate background for new dimensions\n",
        "                self.create_background()\n",
        "                \n"
    ]
    
    # Replace the font update section
    lines[fullscreen_on_section:font_update_end] = new_font_section
    
    # Find the font update section in windowed mode
    windowed_mode_section = -1
    for i in range(font_update_end, len(lines)):
        if "# Update fonts for new screen size" in lines[i]:
            windowed_mode_section = i
            break
    
    if windowed_mode_section == -1:
        print("Could not find font update section in windowed mode!")
        return
    
    # Find the end of the windowed mode font update section
    windowed_font_end = -1
    for i in range(windowed_mode_section, len(lines)):
        if "print(f\"Switched to windowed mode:" in lines[i]:
            windowed_font_end = i
            break
    
    if windowed_font_end == -1:
        print("Could not find end of windowed mode font update section!")
        return
    
    # Replace the windowed mode font update section with updated code
    new_windowed_font_section = [
        "                # Update fonts for new screen size\n",
        "                self.font_large = get_font(int(self.screen_height * 0.06), bold=True)\n",
        "                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)\n",
        "                self.font_small = get_font(int(self.screen_height * 0.03))\n",
        "                \n",
        "                # Recreate background for new dimensions\n",
        "                self.create_background()\n",
        "                \n"
    ]
    
    # Replace the windowed mode font update section
    lines[windowed_mode_section:windowed_font_end] = new_windowed_font_section
    
    # Find the show_settings_menu method
    show_settings_start = -1
    for i, line in enumerate(lines):
        if "def show_settings_menu(self, background_surface):" in line:
            show_settings_start = i
            break
    
    if show_settings_start == -1:
        print("Could not find show_settings_menu method!")
        return
    
    # Find the FULLSCREEN_CHANGED section
    fullscreen_changed_section = -1
    for i in range(show_settings_start, len(lines)):
        if "elif result == \"RESIZE\" or result == \"FULLSCREEN_CHANGED\":" in lines[i]:
            fullscreen_changed_section = i
            break
    
    if fullscreen_changed_section == -1:
        print("Could not find FULLSCREEN_CHANGED section!")
        return
    
    # Find the end of the settings menu recreation section
    settings_menu_recreation_end = -1
    for i in range(fullscreen_changed_section, len(lines)):
        if "settings_menu = SettingsMenu(self.screen, screen_width, screen_height)" in lines[i]:
            settings_menu_recreation_end = i + 1
            break
    
    if settings_menu_recreation_end == -1:
        print("Could not find end of settings menu recreation section!")
        return
    
    # Add code to recreate the background surface
    background_recreation_code = [
        "\n",
        "                    # Recreate the background surface for the new resolution\n",
        "                    try:\n",
        "                        # Try to load the background image\n",
        "                        background_image = pygame.image.load(\"bgm.jpg\")\n",
        "                        # Scale the image to fit the new screen size\n",
        "                        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))\n",
        "                        # Create a new background surface\n",
        "                        background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))\n",
        "                        background_surface.blit(background_image, (0, 0))\n",
        "                        # Add semi-transparent overlay\n",
        "                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)\n",
        "                        overlay.fill((0, 0, 0, 120))\n",
        "                        background_surface.blit(overlay, (0, 0))\n",
        "                    except Exception as e:\n",
        "                        print(f\"Error recreating background after resolution change: {e}\")\n",
        "\n"
    ]
    
    # Insert the background recreation code
    for i, line in enumerate(background_recreation_code):
        lines.insert(settings_menu_recreation_end + i, line)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("Fullscreen background fix applied successfully!")

if __name__ == "__main__":
    fix_fullscreen_background()
