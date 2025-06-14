"""
Update the SettingsMenu class in car_game.py with animation features.

This file contains the code changes needed to add animations to the SettingsMenu class.
Follow the instructions below to implement these changes.
"""

# Step 1: Add the animate_option_toggle method to the SettingsMenu class
"""
def animate_option_toggle(self, option, old_value, new_value):
    # Animation parameters
    duration = 0.3  # seconds
    start_time = time.time()
    
    # Calculate the position of the value text
    option_index = list(self.settings.keys()).index(option)
    y_offset = self.screen_height * 0.35 + option_index * 60
    value_rect = pygame.Rect(
        self.screen_width // 2 + 20,
        y_offset - 15,
        100,
        30
    )
    
    # Create surfaces for old and new values
    old_surface = self.font_medium.render(old_value, True, WHITE)
    new_surface = self.font_medium.render(new_value, True, WHITE)
    
    # Store original screen content
    original_bg = self.screen.copy()
    
    # Animation loop
    clock = pygame.time.Clock()
    while True:
        current_time = time.time()
        progress = min(1.0, (current_time - start_time) / duration)
        
        # Restore background
        self.screen.blit(original_bg, (0, 0))
        
        if progress < 0.5:
            # First half: fade out old value and slide up
            alpha = int(255 * (1 - progress * 2))
            offset_y = int(-20 * progress * 2)
            
            # Create a temporary surface with alpha
            temp_surface = pygame.Surface(old_surface.get_size(), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 0))
            temp_surface.blit(old_surface, (0, 0))
            temp_surface.set_alpha(alpha)
            
            # Draw with offset
            self.screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
        else:
            # Second half: fade in new value and slide down
            alpha = int(255 * ((progress - 0.5) * 2))
            offset_y = int(20 * (1 - (progress - 0.5) * 2))
            
            # Create a temporary surface with alpha
            temp_surface = pygame.Surface(new_surface.get_size(), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 0))
            temp_surface.blit(new_surface, (0, 0))
            temp_surface.set_alpha(alpha)
            
            # Draw with offset
            self.screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
        
        pygame.display.flip()
        
        # Check if animation is complete
        if progress >= 1.0:
            break
        
        # Handle events during animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Cap the frame rate
        clock.tick(60)
"""

# Step 2: Update the handle_input method in the SettingsMenu class
"""
# Find the LEFT key handling code and replace it with:
elif event.key == pygame.K_LEFT:
    if self.selected_option < len(self.settings):
        option = list(self.settings.keys())[self.selected_option]
        values = self.settings[option]
        old_value = values[self.current_values[option]]
        self.current_values[option] = (self.current_values[option] - 1) % len(values)
        new_value = values[self.current_values[option]]
        
        # Play menu navigation sound
        if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
            try:
                sound_menu_navigate.play()
            except:
                pass
        
        # Animate the option toggle
        self.animate_option_toggle(option, old_value, new_value)
        
        # Apply the setting
        result = self.apply_setting(option)
        if result:
            return result

# Find the RIGHT key handling code and replace it with:
elif event.key == pygame.K_RIGHT:
    if self.selected_option < len(self.settings):
        option = list(self.settings.keys())[self.selected_option]
        values = self.settings[option]
        old_value = values[self.current_values[option]]
        self.current_values[option] = (self.current_values[option] + 1) % len(values)
        new_value = values[self.current_values[option]]
        
        # Play menu navigation sound
        if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
            try:
                sound_menu_navigate.play()
            except:
                pass
        
        # Animate the option toggle
        self.animate_option_toggle(option, old_value, new_value)
        
        # Apply the setting
        result = self.apply_setting(option)
        if result:
            return result

# Find the mouse click handling code for options and replace it with:
# Inside the mouse click handling for options:
# Toggle the setting
option = list(self.settings.keys())[i]
values = self.settings[option]
old_value = values[self.current_values[option]]
self.current_values[option] = (self.current_values[option] + 1) % len(values)
new_value = values[self.current_values[option]]

# Animate the option toggle
self.animate_option_toggle(option, old_value, new_value)

# Apply the setting
result = self.apply_setting(option)
if result:
    return result
"""

# Step 3: Add the draw_pulsating_highlight method to the SettingsMenu class
"""
def draw_pulsating_highlight(self, rect, color, thickness=2):
    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5  # 0.0 to 1.0
    
    # Calculate pulsating size and alpha
    expand = int(pulse * 6)
    alpha = int(128 + pulse * 127)  # 128-255
    
    # Create a surface for the highlight
    highlight_rect = rect.inflate(expand, expand)
    highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
    
    # Draw the highlight with alpha
    highlight_color = (*color, alpha)
    pygame.draw.rect(highlight_surface, highlight_color, (0, 0, highlight_rect.width, highlight_rect.height), thickness, border_radius=5)
    
    # Draw the highlight
    self.screen.blit(highlight_surface, highlight_rect.topleft)
"""

# Step 4: Update the draw_to_surface method to use the pulsating highlight
"""
# Find where the options are drawn and add this code after drawing each option:
if i == self.selected_option:
    # Draw pulsating highlight around selected option
    option_rect = pygame.Rect(
        self.screen_width // 2 - 150,  # Adjust as needed
        y_offset - 20,
        300,  # Adjust as needed
        40    # Adjust as needed
    )
    self.draw_pulsating_highlight(option_rect, ELECTRIC_PURPLE)
"""

print("To implement these changes:")
print("1. Add the animate_option_toggle method to the SettingsMenu class")
print("2. Update the handle_input method to call the animation when changing settings")
print("3. Add the draw_pulsating_highlight method to the SettingsMenu class")
print("4. Update the draw_to_surface method to use the pulsating highlight")
print("\nThese changes will add smooth animations when toggling between different options in the settings menu.")
