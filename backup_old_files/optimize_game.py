#!/usr/bin/env python3
import os
import re
import sys

def optimize_game():
    """Apply performance optimizations to car_game.py"""
    print("Optimizing car_game.py for better performance...")
    
    # Read the original file
    with open('car_game.py', 'r') as f:
        content = f.read()
    
    # Create backup
    with open('car_game.py.bak', 'w') as f:
        f.write(content)
    print("Created backup at car_game.py.bak")
    
    # Apply optimizations
    
    # 1. Reduce particle count
    content = re.sub(r'STAR_COUNT = 15', 'STAR_COUNT = 8  # Reduced for performance', content)
    content = re.sub(r'count=15', 'count=8  # Reduced for performance', content)
    content = re.sub(r'count=10', 'count=5  # Reduced for performance', content)
    content = re.sub(r'count=20', 'count=10  # Reduced for performance', content)
    
    # 2. Add particle limits
    content = re.sub(r'def add_particle\(self, particle: Particle\) -> None:',
                    'def add_particle(self, particle: Particle) -> None:\n        # Limit total particles for performance\n        if len(self.particles) >= 30:  # Added particle limit\n            return', content)
    
    # 3. Reduce spawn rates
    content = re.sub(r'if random.random\(\) < 0.7:', 'if random.random() < 0.3:  # Reduced spawn chance', content)
    content = re.sub(r'if random.random\(\) < 0.3:', 'if random.random() < 0.15:  # Reduced spawn chance', content)
    
    # 4. Reduce maximum game objects
    content = re.sub(r'if len\(self.obstacles\) < 3:', 'if len(self.obstacles) < 2:  # Reduced max obstacles', content)
    content = re.sub(r'if len\(self.other_cars\) < 3:', 'if len(self.other_cars) < 2:  # Reduced max cars', content)
    content = re.sub(r'if len\(self.coins\) < 10:', 'if len(self.coins) < 8:  # Reduced max coins', content)
    
    # 5. Increase spawn intervals
    content = re.sub(r'random.uniform\(1.0, 3.0\)', 'random.uniform(2.0, 5.0)  # Increased interval', content)
    content = re.sub(r'random.uniform\(3.0, 6.0\)', 'random.uniform(4.0, 8.0)  # Increased interval', content)
    
    # 6. Add background caching
    bg_cache_code = """
        # Use cached background if available for better performance
        if not hasattr(self, 'cached_background') or not hasattr(self, 'cached_day_phase') or abs(self.cached_day_phase - self.day_phase) > 0.01:
            # Only recreate the background when the day phase changes significantly
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                # Get color for this y position
                color = self.get_sky_color(y)
                pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))
            
            # Cache the background and day phase
            self.cached_background = background
            self.cached_day_phase = self.day_phase
        else:
            # Use the cached background
            background = self.cached_background
    """
    
    content = content.replace("        # Create gradient background for the road based on time of day", 
                             "        # Create gradient background for the road based on time of day\n" + bg_cache_code)
    
    # 7. Reduce target FPS
    content = re.sub(r'self.clock.tick\(60\)', 'self.clock.tick(30)  # Reduced for better performance', content)
    
    # 8. Disable some visual effects conditionally
    content = re.sub(r'def draw_headlights\(self\):',
                    'def draw_headlights(self):\n        # Skip headlight effects for performance\n        return', content)
    
    # 9. Add performance settings at the top
    perf_settings = """
# Performance optimization settings
MAX_PARTICLES = 30  # Limit total particles
MAX_OBSTACLES = 2   # Limit obstacles
MAX_CARS = 2        # Limit other cars
MAX_COINS = 8       # Limit coins
MAX_SPARKLES = 30   # Limit menu sparkles
PARTICLE_SPAWN_CHANCE = 0.3  # Reduce particle spawn chance
ENABLE_BACKGROUND_CACHE = True  # Cache background gradients
ENABLE_HEADLIGHTS = False  # Disable headlight effects for performance
ENABLE_TIRE_TRACKS = False  # Disable tire track effects
TARGET_FPS = 30     # Target 30 FPS for better performance
"""
    
    # Find a good place to insert performance settings
    insert_pos = content.find("# Game settings")
    if insert_pos > 0:
        content = content[:insert_pos] + perf_settings + content[insert_pos:]
    
    # Write optimized file
    with open('car_game_optimized.py', 'w') as f:
        f.write(content)
    
    print("Optimized game saved to car_game_optimized.py")
    print("Run with: python3 car_game_optimized.py")

if __name__ == "__main__":
    optimize_game()
