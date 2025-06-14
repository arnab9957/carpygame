# Animation Implementation Guide for Car Racing Game

This guide explains how to implement the animation effects for toggling between different options in the car racing game.

## Overview

The animation code in `animation_updates.py` adds the following features:

1. **Option Toggle Animation** - Smooth transitions when changing settings
2. **Car Selection Animation** - Sliding effect when switching between cars in the garage
3. **Pulsating Highlight Effect** - Dynamic highlighting for selected menu items
4. **Menu Transition Effects** - Smooth transitions between different menus

## Implementation Steps

### 1. Update the SettingsMenu Class

Add the following methods to the `SettingsMenu` class in `car_game.py`:

- `animate_option_toggle(self, option, old_value, new_value)`
- `update_toggle_animation(self)`

Then modify these existing methods:
- `draw(self)`
- `apply_setting(self, option)`
- `handle_input(self)`

### 2. Update the Game Class for Car Selection Animation

Add this method to the `Game` class:
- `animate_car_switch(self, direction)`

### 3. Add Utility Animation Methods

Add these utility methods to the appropriate classes:
- `draw_pulsating_highlight(self, rect, color, thickness=2)`
- `transition_to_menu(self, menu_draw_function, direction="in", duration=0.5)`

## Implementation Details

### SettingsMenu Class Updates

1. Add toggle animation variables to the `__init__` method:
```python
# Toggle animation variables
self.toggle_animation = False
self.toggle_start_time = 0
self.toggle_duration = 0.3  # seconds
self.toggle_option = None
self.toggle_old_value = None
self.toggle_new_value = None
self.toggle_rect = None
```

2. Update the `handle_input` method to check for toggle animation:
```python
# At the beginning of the method
if hasattr(self, 'toggle_animation') and self.toggle_animation:
    self.update_toggle_animation()
    return None
```

3. Update the `draw` method to handle animation:
```python
# Check if toggle animation is active
if hasattr(self, 'toggle_animation') and self.toggle_animation:
    self.update_toggle_animation()
    return
```

### Garage Menu Updates

In the `show_garage_menu` method, update the car switching logic:

```python
# When switching to previous car
if event.key == pygame.K_LEFT:
    self.animate_car_switch(-1)
    # Play selection sound
    if sound_enabled and hasattr(self, "sound_menu_navigate"):
        self.sound_menu_navigate.play()

# When switching to next car
elif event.key == pygame.K_RIGHT:
    self.animate_car_switch(1)
    # Play selection sound
    if sound_enabled and hasattr(self, "sound_menu_navigate"):
        self.sound_menu_navigate.play()
```

## Testing

After implementing these changes:

1. Run the game and navigate to the Settings menu
2. Toggle options like Sound, Music, or Fullscreen to see the animation effects
3. Go to the Garage menu and switch between cars to see the sliding animation
4. Navigate between different menus to see the transition effects

## Troubleshooting

If you encounter issues:

1. Check that all required variables are properly initialized
2. Ensure the particle system is accessible from the animation methods
3. Verify that the animation timing works well on your system (adjust duration if needed)
4. Make sure event handling during animations doesn't interfere with the main game loop

## Performance Considerations

The animations are designed to be lightweight, but if you experience performance issues:

1. Reduce the number of particles created during animations
2. Simplify the animation effects
3. Adjust the animation duration to be shorter
4. Skip animations on lower-end systems
