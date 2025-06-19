import pygame
import math
import random
import time

class MenuAnimations:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.title_bounce_time = 0.0
        self.background_pulse_time = 0.0
        
    def generate_particles(self, count=30):
        """Generate floating particles for menu background"""
        self.particles = []
        for _ in range(count):
            particle = {
                'x': random.randint(0, self.screen.get_width()),
                'y': random.randint(0, self.screen.get_height()),
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-30, 30),
                'size': random.randint(1, 4),
                'color': random.choice([(255, 255, 0), (128, 0, 255), (0, 255, 0), (192, 192, 192)]),
                'alpha': random.randint(100, 255),
                'pulse_speed': random.uniform(2, 5),
                'pulse_offset': random.uniform(0, 6.28)
            }
            self.particles.append(particle)
    
    def update_particles(self, dt):
        """Update particle positions and properties"""
        for particle in self.particles:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            
            # Wrap around screen edges
            if particle['x'] < -10:
                particle['x'] = self.screen.get_width() + 10
            elif particle['x'] > self.screen.get_width() + 10:
                particle['x'] = -10
            if particle['y'] < -10:
                particle['y'] = self.screen.get_height() + 10
            elif particle['y'] > self.screen.get_height() + 10:
                particle['y'] = -10
            
            # Update pulsing alpha
            particle['pulse_offset'] += particle['pulse_speed'] * dt
            pulse_factor = (math.sin(particle['pulse_offset']) + 1) / 2
            particle['current_alpha'] = int(particle['alpha'] * (0.3 + 0.7 * pulse_factor))
    
    def draw_particles(self):
        """Draw animated particles"""
        for particle in self.particles:
            color = (*particle['color'], particle['current_alpha'])
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
            self.screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def update_timers(self, dt):
        """Update animation timers"""
        self.title_bounce_time += dt
        self.background_pulse_time += dt
    
    def draw_animated_title(self, title_text, base_rect):
        """Draw title with bounce animation and glow effect"""
        # Calculate bounce offset
        bounce_offset = math.sin(self.title_bounce_time * 2.0) * 10.0
        animated_rect = base_rect.copy()
        animated_rect.y += int(bounce_offset)
        
        # Add glow effect that changes color
        glow_colors = [(255, 255, 0), (128, 0, 255), (0, 255, 0)]
        glow_color = glow_colors[int(self.title_bounce_time) % len(glow_colors)]
        
        # Draw glow layers
        for i in range(3, 0, -1):
            glow_alpha = int(80 * (4 - i) / 3)
            glow_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
            glow_surface.fill((*glow_color, glow_alpha))
            glow_rect = animated_rect.copy()
            glow_rect.x += i * 2
            glow_rect.y += i * 2
            self.screen.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_ADD)
        
        # Draw main title
        self.screen.blit(title_text, animated_rect)
        return animated_rect
    
    def draw_animated_menu_item(self, text_surface, base_rect, is_hovered=False, slide_progress=1.0):
        """Draw menu item with slide-in animation and hover effects"""
        # Calculate slide offset
        slide_offset = int((1.0 - slide_progress) * 200)  # Slide in from right
        animated_rect = base_rect.copy()
        animated_rect.x += slide_offset
        
        # Add hover glow effect
        if is_hovered:
            # Create pulsing glow
            pulse = (math.sin(self.background_pulse_time * 4) + 1) * 0.5
            glow_intensity = int(100 + 50 * pulse)
            
            # Draw glow background
            glow_surface = pygame.Surface((animated_rect.width + 20, animated_rect.height + 10), pygame.SRCALPHA)
            glow_surface.fill((255, 255, 0, glow_intensity))
            glow_rect = glow_surface.get_rect(center=animated_rect.center)
            self.screen.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_ADD)
        
        # Draw the text
        self.screen.blit(text_surface, animated_rect)
        return animated_rect
    
    def draw_background_effects(self, base_surface=None):
        """Draw animated background effects"""
        if base_surface:
            self.screen.blit(base_surface, (0, 0))
        
        # Add pulsing overlay
        pulse_intensity = (math.sin(self.background_pulse_time * 1.5) + 1) * 0.5
        overlay_alpha = int(20 + 30 * pulse_intensity)
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 50, overlay_alpha))  # Blue tint
        self.screen.blit(overlay, (0, 0))
