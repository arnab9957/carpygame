"""
This file demonstrates how to implement the animations in car_game.py.
You can run this file directly to see the animations in action.
"""

import pygame
import random
import sys
import time
import math

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NEON_YELLOW = (255, 255, 0)
NEON_GREEN = (57, 255, 20)
ELECTRIC_PURPLE = (191, 64, 191)
SLEEK_SILVER = (204, 204, 204)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animation Demo")

# Particle class for visual effects
class Particle:
    def __init__(self, x, y, color, size, velocity, lifetime, alpha=255, shrink=True, gravity=0):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.initial_size = size
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alpha = alpha
        self.shrink = shrink
        self.gravity = gravity
        self.creation_time = time.time()

    def update(self, dt):
        # Scale velocity by delta time for frame-rate independence
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

        # Apply gravity
        if self.gravity > 0:
            self.velocity = (self.velocity[0], self.velocity[1] + self.gravity * dt)

        # Update lifetime
        self.lifetime -= dt

        # Update size if shrinking
        if self.shrink:
            self.size = self.initial_size * (self.lifetime / self.max_lifetime)

        # Update alpha (fade out)
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))

    def draw(self, screen):
        if self.lifetime <= 0:
            return

        try:
            # Create a surface with per-pixel alpha
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

            # Make sure alpha is within valid range
            alpha = max(0, min(255, self.alpha))

            # Make sure color values are valid
            r = max(0, min(255, self.color[0]))
            g = max(0, min(255, self.color[1]))
            b = max(0, min(255, self.color[2]))

            # Draw the particle with alpha
            pygame.draw.circle(
                particle_surface,
                (r, g, b, alpha),
                (self.size, self.size),
                self.size,
            )

            # Blit the particle surface onto the screen
            screen.blit(particle_surface, (self.x - self.size, self.y - self.size))
        except Exception as e:
            # Silently fail if there's an error drawing a particle
            pass

    def is_alive(self):
        return self.lifetime > 0

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.last_update_time = time.time()

    def add_particle(self, particle):
        # Limit total particles for performance
        if len(self.particles) >= 50:
            return
        self.particles.append(particle)

    def update(self, dt):
        # If dt is not provided or is zero, calculate it
        if dt <= 0:
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

        # Cap dt to avoid large jumps
        dt = min(dt, 0.1)

        # Update all particles
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def create_spark(self, x, y, count=10, intensity=1.0):
        """Create spark particles at the given position with adjustable intensity"""
        for _ in range(count):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150) * intensity
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            # Random color variations of yellow/orange
            color_choice = random.choice(
                [
                    (255, 255, 0),  # Yellow
                    (255, 200, 0),  # Gold
                    (255, 165, 0),  # Orange
                    (255, 140, 0),  # Dark Orange
                    (255, 255, 224),  # Light Yellow
                ]
            )

            # Create the particle with enhanced properties based on intensity
            particle = Particle(
                x=x + random.uniform(-5, 5) * intensity,
                y=y + random.uniform(-5, 5) * intensity,
                color=color_choice,
                size=random.uniform(1, 3) * intensity,
                velocity=velocity,
                lifetime=random.uniform(0.2, 0.8) * intensity,
                shrink=True,
                gravity=random.uniform(-10, 10) * intensity,
            )
            self.add_particle(particle)

# Create particle system
particle_system = ParticleSystem()

# Font setup
pygame.font.init()
font_large = pygame.font.SysFont("Arial", 36, bold=True)
font_medium = pygame.font.SysFont("Arial", 24, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

# Demo settings
settings = {
    "FULLSCREEN": ["OFF", "ON"],
    "SOUND": ["OFF", "ON"],
    "MUSIC": ["OFF", "ON"],
    "DIFFICULTY": ["EASY", "NORMAL", "HARD"],
}

current_values = {
    "FULLSCREEN": 0,
    "SOUND": 1,
    "MUSIC": 1,
    "DIFFICULTY": 1,
}

selected_option = 0

# Car images for garage demo
car_colors = [
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (128, 0, 128)   # Purple
]

car_images = []
for color in car_colors:
    # Create a car image
    car_img = pygame.Surface((100, 60), pygame.SRCALPHA)
    # Car body
    pygame.draw.rect(car_img, color, [10, 10, 80, 40], 0, 10)
    # Windows
    pygame.draw.rect(car_img, (100, 200, 255), [20, 15, 60, 15], 0, 5)
    # Wheels
    pygame.draw.circle(car_img, BLACK, (25, 50), 10)
    pygame.draw.circle(car_img, BLACK, (75, 50), 10)
    car_images.append(car_img)

current_car = 0

def animate_option_toggle(option, old_value, new_value):
    """Animate transitioning between option values"""
    # Animation parameters
    duration = 0.3  # seconds
    start_time = time.time()
    
    # Calculate the position of the value text
    option_index = list(settings.keys()).index(option)
    y_offset = 150 + option_index * 60
    value_rect = pygame.Rect(
        SCREEN_WIDTH // 2 + 20,
        y_offset - 15,
        100,
        30
    )
    
    # Create surfaces for old and new values
    old_surface = font_medium.render(old_value, True, WHITE)
    new_surface = font_medium.render(new_value, True, WHITE)
    
    # Store original screen content
    original_bg = screen.copy()
    
    # Animation loop
    clock = pygame.time.Clock()
    while True:
        current_time = time.time()
        progress = min(1.0, (current_time - start_time) / duration)
        
        # Restore background
        screen.blit(original_bg, (0, 0))
        
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
            screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
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
            screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
        
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
                
                # Add to particle system
                particle_system.add_particle(particle)
        
        # Update and draw particles
        particle_system.update(1/60)
        particle_system.draw(screen)
        
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

def animate_car_switch(old_car_index, new_car_index):
    """Animate switching between cars in the garage"""
    # Animation parameters
    duration = 0.3  # seconds
    start_time = time.time()
    
    # Determine direction (1 for next, -1 for previous)
    direction = 1 if (new_car_index > old_car_index or 
                      (old_car_index == len(car_images)-1 and new_car_index == 0)) else -1
    
    # Store original screen content
    original_bg = screen.copy()
    
    # Animation loop
    clock = pygame.time.Clock()
    while True:
        current_time = time.time()
        progress = min(1.0, (current_time - start_time) / duration)
        
        # Restore background
        screen.blit(original_bg, (0, 0))
        
        # Calculate slide offset
        if direction > 0:  # Next car
            offset_x = int((1.0 - progress) * SCREEN_WIDTH)
        else:  # Previous car
            offset_x = int((progress - 1.0) * SCREEN_WIDTH)
        
        # Draw old car sliding out
        old_car_image = car_images[old_car_index]
        old_car_rect = old_car_image.get_rect(
            center=(SCREEN_WIDTH // 2 - offset_x, SCREEN_HEIGHT // 2)
        )
        screen.blit(old_car_image, old_car_rect)
        
        # Draw new car sliding in
        new_car_image = car_images[new_car_index]
        new_car_rect = new_car_image.get_rect(
            center=(SCREEN_WIDTH // 2 + (direction * SCREEN_WIDTH) - offset_x, SCREEN_HEIGHT // 2)
        )
        screen.blit(new_car_image, new_car_rect)
        
        # Add some particle effects
        if random.random() < 0.3:
            particle_system.create_spark(
                SCREEN_WIDTH // 2 + random.uniform(-100, 100),
                SCREEN_HEIGHT // 2 + random.uniform(-50, 50),
                count=3,
                intensity=0.7
            )
        
        # Update and draw particles
        particle_system.update(1/60)
        particle_system.draw(screen)
        
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

def draw_pulsating_highlight(rect, color, thickness=2):
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
    screen.blit(highlight_surface, highlight_rect.topleft)

def transition_to_menu(menu_draw_function, direction="in", duration=0.5):
    """
    Perform a smooth transition to a menu
    
    Parameters:
    - menu_draw_function: Function that draws the menu
    - direction: "in" for appearing, "out" for disappearing
    - duration: Animation duration in seconds
    """
    start_time = time.time()
    
    # Store original screen content
    original_bg = screen.copy()
    
    # Create a surface for the menu
    menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    
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
        screen.blit(original_bg, (0, 0))
        
        # Scale and position the menu
        scaled_width = int(SCREEN_WIDTH * scale)
        scaled_height = int(SCREEN_HEIGHT * scale)
        scaled_menu = pygame.transform.smoothscale(menu_surface, (scaled_width, scaled_height))
        scaled_menu.set_alpha(alpha)
        
        # Center the scaled menu
        pos_x = (SCREEN_WIDTH - scaled_width) // 2
        pos_y = (SCREEN_HEIGHT - scaled_height) // 2 + offset_y
        
        # Draw the menu
        screen.blit(scaled_menu, (pos_x, pos_y))
        
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

def draw_settings_menu(surface):
    """Draw the settings menu to a surface"""
    # Fill with background color
    surface.fill(BLACK)
    
    # Draw title
    title_text = font_large.render("SETTINGS", True, NEON_YELLOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    surface.blit(title_text, title_rect)
    
    # Draw options
    y_offset = 150
    for i, (option, values) in enumerate(settings.items()):
        # Draw option name
        if i == selected_option:
            color = ELECTRIC_PURPLE
            option_text = font_medium.render(f"> {option} <", True, color)
        else:
            color = WHITE
            option_text = font_medium.render(option, True, color)
        
        option_rect = option_text.get_rect(midright=(SCREEN_WIDTH // 2 - 20, y_offset))
        surface.blit(option_text, option_rect)
        
        # Draw current value
        current_value = values[current_values[option]]
        value_text = font_medium.render(current_value, True, NEON_GREEN)
        value_rect = value_text.get_rect(midleft=(SCREEN_WIDTH // 2 + 20, y_offset))
        surface.blit(value_text, value_rect)
        
        y_offset += 60
    
    # Draw back button
    back_text = font_medium.render("BACK", True, RED)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    surface.blit(back_text, back_rect)

def draw_garage_menu(surface):
    """Draw the garage menu to a surface"""
    # Fill with background color
    surface.fill(BLACK)
    
    # Draw title
    title_text = font_large.render("GARAGE", True, NEON_YELLOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    surface.blit(title_text, title_rect)
    
    # Draw car
    car_image = car_images[current_car]
    car_rect = car_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(car_image, car_rect)
    
    # Draw car name
    car_names = ["RED RACER", "BLUE BOLT", "GREEN MACHINE", "YELLOW FLASH", "PURPLE PHANTOM"]
    car_name_text = font_medium.render(car_names[current_car], True, ELECTRIC_PURPLE)
    car_name_rect = car_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    surface.blit(car_name_text, car_name_rect)
    
    # Draw navigation arrows
    left_arrow = font_large.render("<", True, NEON_GREEN)
    left_rect = left_arrow.get_rect(center=(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    surface.blit(left_arrow, left_rect)
    
    right_arrow = font_large.render(">", True, NEON_GREEN)
    right_rect = right_arrow.get_rect(center=(3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
    surface.blit(right_arrow, right_rect)
    
    # Draw back button
    back_text = font_medium.render("BACK", True, RED)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    surface.blit(back_text, back_rect)

# Main demo loop
def main():
    global selected_option, current_car
    
    clock = pygame.time.Clock()
    running = True
    
    # Demo state
    current_demo = "settings"  # "settings" or "garage"
    
    # Start with a transition
    transition_to_menu(draw_settings_menu, "in")
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if current_demo == "settings":
                    if event.key == pygame.K_UP:
                        selected_option = max(0, selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        selected_option = min(len(settings), selected_option + 1)
                    elif event.key == pygame.K_LEFT:
                        if selected_option < len(settings):
                            option = list(settings.keys())[selected_option]
                            values = settings[option]
                            old_value = values[current_values[option]]
                            current_values[option] = (current_values[option] - 1) % len(values)
                            new_value = values[current_values[option]]
                            animate_option_toggle(option, old_value, new_value)
                    elif event.key == pygame.K_RIGHT:
                        if selected_option < len(settings):
                            option = list(settings.keys())[selected_option]
                            values = settings[option]
                            old_value = values[current_values[option]]
                            current_values[option] = (current_values[option] + 1) % len(values)
                            new_value = values[current_values[option]]
                            animate_option_toggle(option, old_value, new_value)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == len(settings):  # Back button
                            # Switch to garage demo
                            current_demo = "garage"
                            transition_to_menu(draw_garage_menu, "in")
                
                elif current_demo == "garage":
                    if event.key == pygame.K_LEFT:
                        old_car = current_car
                        current_car = (current_car - 1) % len(car_images)
                        animate_car_switch(old_car, current_car)
                    elif event.key == pygame.K_RIGHT:
                        old_car = current_car
                        current_car = (current_car + 1) % len(car_images)
                        animate_car_switch(old_car, current_car)
                    elif event.key == pygame.K_RETURN:
                        # Switch back to settings demo
                        current_demo = "settings"
                        transition_to_menu(draw_settings_menu, "in")
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw current demo
        if current_demo == "settings":
            draw_settings_menu(screen)
            
            # Draw pulsating highlight around selected option
            if selected_option < len(settings):
                option = list(settings.keys())[selected_option]
                option_index = list(settings.keys()).index(option)
                y_offset = 150 + option_index * 60
                option_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y_offset - 20, 300, 40)
                draw_pulsating_highlight(option_rect, ELECTRIC_PURPLE)
            else:
                # Highlight back button
                back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 120, 100, 40)
                draw_pulsating_highlight(back_rect, RED)
                
        elif current_demo == "garage":
            draw_garage_menu(screen)
            
            # Draw pulsating highlight around car
            car_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 40, 120, 80)
            draw_pulsating_highlight(car_rect, car_colors[current_car])
        
        # Update and draw particles
        particle_system.update(1/60)
        particle_system.draw(screen)
        
        # Draw instructions
        if current_demo == "settings":
            instructions = "Arrow keys: Navigate | Enter: Select | ESC: Exit"
        else:
            instructions = "Left/Right: Change car | Enter: Back to settings | ESC: Exit"
        
        instructions_text = font_small.render(instructions, True, SLEEK_SILVER)
        instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instructions_text, instructions_rect)
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
