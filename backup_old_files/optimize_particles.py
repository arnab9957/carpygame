#!/usr/bin/env python3
import re

def optimize_particles():
    """Optimize the Particle class for better performance"""
    print("Optimizing particle system for better performance...")
    
    with open('car_game_optimized.py', 'r') as f:
        content = f.read()
    
    # Find the Particle class
    particle_class_match = re.search(r'class Particle:(.*?)class ParticleSystem:', content, re.DOTALL)
    if not particle_class_match:
        print("Could not find Particle class, skipping optimization")
        return
    
    particle_class = particle_class_match.group(1)
    
    # Optimize the draw method to skip small particles
    optimized_draw = """
    def draw(self, screen: pygame.Surface) -> None:
        if self.lifetime <= 0 or self.size < 1.0:  # Skip very small particles
            return

        try:
            # Skip alpha calculations for better performance
            if self.alpha < 30:  # Skip nearly invisible particles
                return
                
            # Create a surface with per-pixel alpha
            particle_surface = pygame.Surface(
                (int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA
            )

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
                (int(self.size), int(self.size)),
                int(self.size),
            )

            # Blit the particle surface onto the screen
            screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))
        except Exception as e:
            # Silently fail if there's an error drawing a particle
            pass
    """
    
    # Replace the draw method
    updated_particle_class = re.sub(r'def draw\(self, screen: pygame\.Surface\) -> None:(.*?)def is_alive', 
                                   lambda m: optimized_draw + '\n    def is_alive', 
                                   particle_class, flags=re.DOTALL)
    
    # Replace the particle class in the content
    updated_content = content.replace(particle_class, updated_particle_class)
    
    # Optimize ParticleSystem methods
    # 1. Optimize create_crash method to use fewer particles
    updated_content = re.sub(r'for _ in range\(20\):', 'for _ in range(10):  # Reduced particle count', updated_content)
    updated_content = re.sub(r'for _ in range\(25\):', 'for _ in range(12):  # Reduced particle count', updated_content)
    
    # 2. Optimize update method to batch process particles
    particle_system_update = """
    def update(self, dt: float) -> None:
        # If dt is not provided or is zero, calculate it
        if dt <= 0:
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

        # Cap dt to avoid large jumps
        dt = min(dt, 0.1)
        
        # Batch process particles - remove dead particles first
        self.particles = [p for p in self.particles if p.lifetime > 0]
        
        # Then update remaining particles
        for particle in self.particles:
            particle.update(dt)
    """
    
    updated_content = re.sub(r'def update\(self, dt: float\) -> None:(.*?)def draw', 
                            lambda m: particle_system_update + '\n    def draw', 
                            updated_content, flags=re.DOTALL)
    
    # Write the optimized file
    with open('car_game_optimized.py', 'w') as f:
        f.write(updated_content)
    
    print("Particle system optimized successfully")

if __name__ == "__main__":
    optimize_particles()
