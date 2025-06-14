"""
Simple animation fix for car_game.py

This file contains a minimal implementation of the option toggle animation
that can be directly added to your SettingsMenu class in car_game.py.
"""

def animate_option_toggle(self, option, old_value, new_value):
    """
    Animate transitioning between option values
    
    Parameters:
    - option: The option being changed
    - old_value: Previous option value text
    - new_value: New option value text
    """
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

# To use this animation in your SettingsMenu class:
# 1. Add the animate_option_toggle method to your SettingsMenu class
# 2. Update your handle_input method to call animate_option_toggle when changing settings
# 3. Example usage:
"""
# Example of how to call the animation in handle_input:
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
"""
