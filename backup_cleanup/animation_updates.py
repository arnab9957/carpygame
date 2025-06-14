"""
Animation updates for car_game.py

This file contains the animation-related code to be added to the car_game.py file.
Copy and paste these methods into the appropriate classes in car_game.py.
"""

# Add these methods to the SettingsMenu class

def animate_option_toggle(self, option, old_value, new_value):
    """
    Animate transitioning between option values
    
    Parameters:
    - option: The option being changed
    - old_value: Previous option value text
    - new_value: New option value text
    """
    # Store animation parameters
    self.toggle_animation = True
    self.toggle_start_time = time.time()
    self.toggle_option = option
    self.toggle_duration = 0.3  # seconds
    
    # Calculate the position of the value text
    option_index = list(self.settings.keys()).index(option)
    y_offset = self.screen_height * 0.35 + option_index * 60
    self.toggle_rect = pygame.Rect(
        self.screen_width // 2 + 20 - 50,  # Centered on the value
        y_offset - 15,
        100,
        30
    )
    
    # Create surfaces for old and new values
    self.old_surface = self.font_medium.render(old_value, True, WHITE)
    self.new_surface = self.font_medium.render(new_value, True, WHITE)
    
    # Store original screen content
    self.toggle_bg = self.screen.copy()

def update_toggle_animation(self):
    """Update the toggle animation if active"""
    if not self.toggle_animation:
        return False
        
    current_time = time.time()
    progress = min(1.0, (current_time - self.toggle_start_time) / self.toggle_duration)
    
    # Restore background
    self.screen.blit(self.toggle_bg, (0, 0))
    
    if progress < 0.5:
        # First half: fade out old value and slide up
        alpha = int(255 * (1 - progress * 2))
        offset_y = int(-20 * progress * 2)
        
        # Create a temporary surface with alpha
        temp_surface = pygame.Surface(self.old_surface.get_size(), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))
        temp_surface.blit(self.old_surface, (0, 0))
        temp_surface.set_alpha(alpha)
        
        # Draw with offset
        self.screen.blit(temp_surface, (self.toggle_rect.x, self.toggle_rect.y + offset_y))
    else:
        # Second half: fade in new value and slide down
        alpha = int(255 * ((progress - 0.5) * 2))
        offset_y = int(20 * (1 - (progress - 0.5) * 2))
        
        # Create a temporary surface with alpha
        temp_surface = pygame.Surface(self.new_surface.get_size(), pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))
        temp_surface.blit(self.new_surface, (0, 0))
        temp_surface.set_alpha(alpha)
        
        # Draw with offset
        self.screen.blit(temp_surface, (self.toggle_rect.x, self.toggle_rect.y + offset_y))
    
    # Add some particle effects
    if random.random() < 0.3:
        # Create sparkle effect around the toggled option
        for _ in range(2):
            sparkle_x = self.toggle_rect.centerx + random.uniform(-self.toggle_rect.width/2, self.toggle_rect.width/2)
            sparkle_y = self.toggle_rect.centery + random.uniform(-self.toggle_rect.height/2, self.toggle_rect.height/2)
            
            # Get color based on the option
            if self.toggle_option == "FULLSCREEN":
                color = NEON_YELLOW
            elif self.toggle_option == "SOUND":
                color = NEON_GREEN
            elif self.toggle_option == "MUSIC":
                color = ELECTRIC_PURPLE
            else:
                color = SLEEK_SILVER
            
            # Create a particle
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
            
            # Add to global particle system
            Game.particle_system.add_particle(particle)
    
    pygame.display.flip()
    
    # Check if animation is complete
    if progress >= 1.0:
        self.toggle_animation = False
        return False
        
    return True

# Update the draw method in SettingsMenu class to include animation
def draw(self):
    # Check if toggle animation is active
    if hasattr(self, 'toggle_animation') and self.toggle_animation:
        self.update_toggle_animation()
        return
        
    # Draw to the main screen
    self.draw_to_surface(self.screen)
    pygame.display.flip()

# Update the apply_setting method in SettingsMenu class
def apply_setting(self, option):
    """Apply the setting change with animation"""
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS, sound_enabled, music_enabled
    
    # Get the old and new values for animation
    old_value = self.settings[option][self.current_values[option]]
    
    # Now apply the actual setting change
    if option == "FULLSCREEN":
        if self.current_values[option] == 1:  # ON
            # Save current window size before going fullscreen
            self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Get the display info for proper fullscreen resolution
            info = pygame.display.Info()
            SCREEN_WIDTH = info.current_w
            SCREEN_HEIGHT = info.current_h
            
            # Set fullscreen mode
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 
                pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            )
            
            # Update menu dimensions
            self.screen_width = SCREEN_WIDTH
            self.screen_height = SCREEN_HEIGHT
            
            # Update scale factors
            SCALE_X = SCREEN_WIDTH / BASE_WIDTH
            SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
            
            # Recalculate lane positions
            LANE_WIDTH = SCREEN_WIDTH // 6
            LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
            
            # Update fonts for new screen size
            self.font_large = get_font(int(self.screen_height * 0.06), bold=True)
            self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)
            self.font_small = get_font(int(self.screen_height * 0.03))
            
            # Recreate background for new dimensions
            self.create_background()
            
            print(f"Switched to fullscreen mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
            return "FULLSCREEN_CHANGED"
        else:  # OFF
            # Restore previous window size
            if hasattr(self, 'windowed_size'):
                window_width, window_height = self.windowed_size
            else:
                # Default size if no previous size is stored
                window_width, window_height = 1280, 720
            
            # Update global variables
            SCREEN_WIDTH = window_width
            SCREEN_HEIGHT = window_height
            
            # Set windowed mode
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 
                pygame.RESIZABLE
            )
            
            # Update menu dimensions
            self.screen_width = SCREEN_WIDTH
            self.screen_height = SCREEN_HEIGHT
            
            # Update scale factors
            SCALE_X = SCREEN_WIDTH / BASE_WIDTH
            SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
            
            # Recalculate lane positions
            LANE_WIDTH = SCREEN_WIDTH // 6
            LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
            
            # Update fonts for new screen size
            self.font_large = get_font(int(self.screen_height * 0.06), bold=True)
            self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)
            self.font_small = get_font(int(self.screen_height * 0.03))
            
            # Recreate background for new dimensions
            self.create_background()
            
            print(f"Switched to windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
            return "FULLSCREEN_CHANGED"
    elif option == "SOUND":
        # Toggle sound
        sound_enabled = bool(self.current_values[option])
        print(f"Sound {'enabled' if sound_enabled else 'disabled'}")
        return None
    elif option == "MUSIC":
        # Toggle music
        music_enabled = bool(self.current_values[option])
        print(f"Music {'enabled' if music_enabled else 'disabled'}")
        return None

    # Other settings would be applied here
    print(f"Setting {option} changed to {self.settings[option][self.current_values[option]]}")
    return None

# Update the handle_input method in SettingsMenu class
def handle_input(self):
    # If toggle animation is active, wait for it to complete
    if hasattr(self, 'toggle_animation') and self.toggle_animation:
        self.update_toggle_animation()
        return None
        
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
                    
                    # Start animation
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
                    
                    # Start animation
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
                            
                            # Start animation
                            self.animate_option_toggle(option, old_value, new_value)
                            
                            # Apply the setting
                            result = self.apply_setting(option)
                            if result:
                                return result
        if event.type == pygame.VIDEORESIZE:
            self.resize(event.w, event.h)
            return "RESIZE"
    return None

# Add these methods to the Game class for car selection animation in the garage menu

def animate_car_switch(self, direction):
    """
    Animate switching between cars in the garage
    
    Parameters:
    - direction: 1 for next car, -1 for previous car
    """
    old_car = self.current_car
    new_car = (self.current_car + direction) % len(self.cars)
    
    # Animation parameters
    duration = 0.3
    start_time = time.time()
    
    # Store original screen content
    original_bg = self.screen.copy()
    
    # Animation loop
    while True:
        current_time = time.time()
        progress = min(1.0, (current_time - start_time) / duration)
        
        # Restore background
        self.screen.blit(original_bg, (0, 0))
        
        # Calculate slide offset
        if direction > 0:  # Next car
            offset_x = int((1.0 - progress) * self.screen_width)
        else:  # Previous car
            offset_x = int((progress - 1.0) * self.screen_width)
        
        # Draw old car sliding out
        old_car_image = self.car_images[old_car]
        old_car_rect = old_car_image.get_rect(center=(self.screen_width // 2 - offset_x, self.screen_height // 2 - 50))
        self.screen.blit(old_car_image, old_car_rect)
        
        # Draw new car sliding in
        new_car_image = self.car_images[new_car]
        new_car_rect = new_car_image.get_rect(center=(self.screen_width // 2 + (direction * self.screen_width) - offset_x, self.screen_height // 2 - 50))
        self.screen.blit(new_car_image, new_car_rect)
        
        # Add some particle effects
        if random.random() < 0.3:
            self.particle_system.create_spark(
                self.screen_width // 2 + random.uniform(-100, 100),
                self.screen_height // 2 - 50 + random.uniform(-50, 50),
                count=3,
                intensity=0.7
            )
        
        pygame.display.flip()
        
        # Check if animation is complete
        if progress >= 1.0:
            self.current_car = new_car
            break
        
        # Handle events during animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Add this method to create a pulsating highlight effect for selected menu items
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

# Add this method for smooth menu transitions
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
    menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
    # Draw the menu to the surface
    menu_draw_function(menu_surface)
    
    # Animation loop
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
        scaled_width = int(SCREEN_WIDTH * scale)
        scaled_height = int(SCREEN_HEIGHT * scale)
        scaled_menu = pygame.transform.smoothscale(menu_surface, (scaled_width, scaled_height))
        scaled_menu.set_alpha(alpha)
        
        # Center the scaled menu
        pos_x = (SCREEN_WIDTH - scaled_width) // 2
        pos_y = (SCREEN_HEIGHT - scaled_height) // 2 + offset_y
        
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
