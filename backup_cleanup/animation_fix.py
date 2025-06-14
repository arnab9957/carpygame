"""
Direct animation fixes for car_game.py

This file contains ready-to-use code snippets that can be directly added to your car_game.py file.
"""

# ===== STEP 1: Add these imports if not already present =====
import time
import math

# ===== STEP 2: Add these methods to the SettingsMenu class =====

"""
Add these methods to the SettingsMenu class in car_game.py
"""

def animate_option_toggle(self, option, old_value, new_value):
    """Animate transitioning between option values"""
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
        
        # Add some particle effects
        if random.random() < 0.3:
            # Create sparkle effect around the toggled option
            for _ in range(2):
                sparkle_x = value_rect.centerx + random.uniform(-value_rect.width/2, value_rect.width/2)
                sparkle_y = value_rect.centery + random.uniform(-value_rect.height/2, value_rect.height/2)
                
                # Get color based on the option
                if option == "FULLSCREEN":
                    color = NEON_YELLOW
                elif option == "SOUND":
                    color = NEON_GREEN
                elif option == "MUSIC":
                    color = ELECTRIC_PURPLE
                else:
                    color = SLEEK_SILVER
                
                # Create particles directly
                particle = Particle(
                    x=sparkle_x,
                    y=sparkle_y,
                    color=color,
                    size=random.uniform(1, 3),
                    velocity=(random.uniform(-30, 30), random.uniform(-30, 30)),
                    lifetime=random.uniform(0.3, 0.6),
                    shrink=True,
                    gravity=0
                )
                
                # Add to particle system if available
                try:
                    if hasattr(pygame.display.get_surface(), "_game"):
                        game = pygame.display.get_surface()._game
                        if hasattr(game, "particle_system"):
                            game.particle_system.add_particle(particle)
                except:
                    pass  # Silently fail if particle system is not accessible
        
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

# ===== STEP 3: Update the handle_input method in SettingsMenu class =====

"""
Replace the handle_input method in SettingsMenu class with this version
"""

def handle_input(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "EXIT"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "BACK"
            elif event.key == pygame.K_UP:
                self.selected_option = max(0, self.selected_option - 1)
                # Play menu navigation sound
                if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                    try:
                        sound_menu_navigate.play()
                    except:
                        pass
            elif event.key == pygame.K_DOWN:
                self.selected_option = min(len(self.settings), self.selected_option + 1)
                # Play menu navigation sound
                if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                    try:
                        sound_menu_navigate.play()
                    except:
                        pass
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
            elif event.key == pygame.K_RETURN:
                # Play menu selection sound
                if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                    try:
                        sound_menu_select.play()
                    except:
                        pass
                
                # If back button is selected
                if self.selected_option == len(self.settings):
                    return "BACK"
                else:
                    # Apply the selected setting
                    option = list(self.settings.keys())[self.selected_option]
                    result = self.apply_setting(option)
                    if result:
                        return result
        # Handle mouse movement for hover effect
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Check if mouse is over any option
            for i, button_rect in enumerate(self.button_rects):
                if button_rect.collidepoint(mouse_pos):
                    new_selection = i if i < len(self.settings) else len(self.settings)
                    if self.selected_option != new_selection:
                        self.selected_option = new_selection
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
                for i, button_rect in enumerate(self.button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        # Play menu selection sound
                        if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                            try:
                                sound_menu_select.play()
                            except:
                                pass
                        
                        # If it's the back button
                        if i == len(self.settings):
                            return "BACK"
                        else:
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
        if event.type == pygame.VIDEORESIZE:
            self.resize(event.w, event.h)
            return "RESIZE"
    return None

# ===== STEP 4: Add car selection animation to the Game class =====

"""
Add this method to the Game class
"""

def animate_car_switch(self, old_car_index, new_car_index, car_images):
    """Animate switching between cars in the garage"""
    # Animation parameters
    duration = 0.3  # seconds
    start_time = time.time()
    
    # Determine direction (1 for next, -1 for previous)
    direction = 1 if (new_car_index > old_car_index or 
                      (old_car_index == len(car_images)-1 and new_car_index == 0)) else -1
    
    # Store original screen content
    original_bg = self.screen.copy()
    
    # Animation loop
    clock = pygame.time.Clock()
    while True:
        current_time = time.time()
        progress = min(1.0, (current_time - start_time) / duration)
        
        # Restore background
        self.screen.blit(original_bg, (0, 0))
        
        # Calculate slide offset
        if direction > 0:  # Next car
            offset_x = int((1.0 - progress) * self.screen.get_width())
        else:  # Previous car
            offset_x = int((progress - 1.0) * self.screen.get_width())
        
        # Draw old car sliding out
        old_car_image = car_images[old_car_index]
        old_car_rect = old_car_image.get_rect(
            center=(self.screen.get_width() // 2 - offset_x, 
                   self.screen.get_height() // 2 - 50)
        )
        self.screen.blit(old_car_image, old_car_rect)
        
        # Draw new car sliding in
        new_car_image = car_images[new_car_index]
        new_car_rect = new_car_image.get_rect(
            center=(self.screen.get_width() // 2 + (direction * self.screen.get_width()) - offset_x, 
                   self.screen.get_height() // 2 - 50)
        )
        self.screen.blit(new_car_image, new_car_rect)
        
        # Add some particle effects
        if random.random() < 0.3:
            self.particle_system.create_spark(
                self.screen.get_width() // 2 + random.uniform(-100, 100),
                self.screen.get_height() // 2 - 50 + random.uniform(-50, 50),
                count=3,
                intensity=0.7
            )
        
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

# ===== STEP 5: Add pulsating highlight effect =====

"""
Add this method to the Game class or any menu class that needs it
"""

def draw_pulsating_highlight(self, rect, color, thickness=2):
    """Draw a pulsating highlight around the given rectangle"""
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

# ===== STEP 6: Update the show_garage_menu method to use car animation =====

"""
In the show_garage_menu method, find the code that handles car switching and update it:
"""

# Example of how to update the car switching code in show_garage_menu:
"""
# When handling left key press:
elif event.key == pygame.K_LEFT:
    # Store old car index
    old_car = current_car
    # Update car index
    current_car = (current_car - 1) % len(cars)
    # Play selection sound
    if sound_enabled and hasattr(self, "sound_menu_navigate"):
        self.sound_menu_navigate.play()
    # Animate car switch
    self.animate_car_switch(old_car, current_car, car_images)

# When handling right key press:
elif event.key == pygame.K_RIGHT:
    # Store old car index
    old_car = current_car
    # Update car index
    current_car = (current_car + 1) % len(cars)
    # Play selection sound
    if sound_enabled and hasattr(self, "sound_menu_navigate"):
        self.sound_menu_navigate.play()
    # Animate car switch
    self.animate_car_switch(old_car, current_car, car_images)
"""

# ===== STEP 7: Add menu transition effect =====

"""
Add this method to the Game class
"""

def transition_to_menu(self, menu_draw_function, direction="in", duration=0.5):
    """
    Perform a smooth transition to a menu
    
    Parameters:
    - menu_draw_function: Function that draws the menu
    - direction: "in" for appearing, "out" for disappearing
    - duration: Animation duration in seconds
    """
    start_time = time.time()
    
    # Store original screen content
    original_bg = self.screen.copy()
    
    # Create a surface for the menu
    menu_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
    
    # Draw the menu to the surface
    menu_draw_function(menu_surface)
    
    # Animation loop
    clock = pygame.time.Clock()
    while True:
        current_time = time.time()
        progress = min(1.0, (current_time - start_time) / duration)
        
        # Calculate animation parameters
        if direction == "in":
            alpha = int(255 * progress)
            scale = 0.9 + 0.1 * progress
            offset_y = int((1.0 - progress) * 50)
        else:  # out
            alpha = int(255 * (1.0 - progress))
            scale = 1.0 - 0.1 * progress
            offset_y = int(progress * 50)
        
        # Draw original background
        self.screen.blit(original_bg, (0, 0))
        
        # Scale and position the menu
        scaled_width = int(self.screen.get_width() * scale)
        scaled_height = int(self.screen.get_height() * scale)
        scaled_menu = pygame.transform.smoothscale(menu_surface, (scaled_width, scaled_height))
        scaled_menu.set_alpha(alpha)
        
        # Center the scaled menu
        pos_x = (self.screen.get_width() - scaled_width) // 2
        pos_y = (self.screen.get_height() - scaled_height) // 2 + offset_y
        
        # Draw the menu
        self.screen.blit(scaled_menu, (pos_x, pos_y))
        
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
