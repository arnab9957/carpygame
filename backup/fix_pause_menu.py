#!/usr/bin/env python3

# This script fixes the pause menu in the car racing game

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    lines = file.readlines()

# Find the PauseMenu class
pause_menu_start = 0
for i, line in enumerate(lines):
    if line.strip() == "class PauseMenu:":
        pause_menu_start = i
        break

# Find the handle_input method in PauseMenu class
handle_input_start = 0
for i in range(pause_menu_start, len(lines)):
    if "def handle_input(self):" in lines[i]:
        handle_input_start = i
        break

# Replace the handle_input method with a fixed version
if handle_input_start > 0:
    # Find the end of the method
    handle_input_end = handle_input_start + 1
    indent_level = len(lines[handle_input_start]) - len(lines[handle_input_start].lstrip())
    
    while handle_input_end < len(lines):
        if lines[handle_input_end].strip() == "" or (len(lines[handle_input_end]) - len(lines[handle_input_end].lstrip()) <= indent_level and lines[handle_input_end].strip().startswith("def ")):
            break
        handle_input_end += 1
    
    # Create the fixed method
    fixed_method = """    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "RESUME"
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(
                        self.options
                    )
                    # Play menu navigation sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_navigate.play()
                        except:
                            pass
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(
                        self.options
                    )
                    # Play menu navigation sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_navigate.play()
                        except:
                            pass
                elif event.key == pygame.K_RETURN:
                    # Play menu selection sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_select.play()
                        except:
                            pass
                    return self.options[self.selected_option]
            # Handle mouse movement for hover effect
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                # Check if mouse is over any option
                for i, option in enumerate(self.options):
                    # Calculate option position
                    option_y = self.screen_height * 0.4 + i * self.screen_height * 0.08
                    option_rect = pygame.Rect(
                        self.screen_width // 2 - 100,  # Approximate width
                        option_y - 20,                 # Approximate height
                        200,                           # Width of clickable area
                        40                             # Height of clickable area
                    )
                    if option_rect.collidepoint(mouse_pos):
                        if self.selected_option != i:
                            self.selected_option = i
                            # Play menu navigation sound
                            if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                                try:
                                    sound_menu_navigate.play()
                                except:
                                    pass
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if any option was clicked
                    for i, option in enumerate(self.options):
                        # Calculate option position
                        option_y = self.screen_height * 0.4 + i * self.screen_height * 0.08
                        option_rect = pygame.Rect(
                            self.screen_width // 2 - 100,  # Approximate width
                            option_y - 20,                 # Approximate height
                            200,                           # Width of clickable area
                            40                             # Height of clickable area
                        )
                        if option_rect.collidepoint(mouse_pos):
                            # Play menu selection sound
                            if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                                try:
                                    sound_menu_select.play()
                                except:
                                    pass
                            return self.options[i]
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
                return "RESIZE"
        return None
"""
    
    # Replace the method
    lines[handle_input_start:handle_input_end] = fixed_method.splitlines(True)
    
    # Write the modified file
    with open('car_game_advanced_new.py', 'w') as file:
        file.writelines(lines)
    
    print("Fixed pause menu handle_input method")
else:
    print("Could not find handle_input method in PauseMenu class")
