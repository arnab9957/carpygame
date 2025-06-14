# Animation Implementation Steps

Follow these steps to add animations to your car racing game:

## Step 1: Add the Option Toggle Animation

1. Open your `car_game.py` file
2. Find the `SettingsMenu` class
3. Add the `animate_option_toggle` method from `simple_toggle_animation.py`
4. Update the `handle_input` method to call the animation when changing settings

### Changes to `handle_input` method:

For the LEFT key:
```python
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
```

Make similar changes for the RIGHT key and mouse click handling.

## Step 2: Add Pulsating Highlight Effect

Add this method to the `SettingsMenu` class:

```python
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
```

Then update the `draw_to_surface` method to use it for the selected option.

## Step 3: Add Car Selection Animation

Add this method to the `Game` class:

```python
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
```

Then update the car switching code in the `show_garage_menu` method.

## Testing

After implementing each step, test the animations by:

1. Running the game
2. Going to the settings menu and changing options
3. Going to the garage menu and switching between cars

If you encounter any issues, check the console for error messages.
