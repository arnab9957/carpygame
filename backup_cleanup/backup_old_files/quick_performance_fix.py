#!/usr/bin/env python3
import re
import os
import sys

def apply_quick_fixes():
    """Apply quick performance fixes to car_game.py"""
    print("Applying quick performance fixes to car_game.py...")
    
    # Read the original file
    with open('car_game.py', 'r') as f:
        content = f.read()
    
    # Create backup if it doesn't exist
    if not os.path.exists('car_game.py.bak'):
        with open('car_game.py.bak', 'w') as f:
            f.write(content)
        print("Created backup at car_game.py.bak")
    
    # 1. Reduce particle effects
    content = content.replace("STAR_COUNT = 15", "STAR_COUNT = 5  # Reduced for performance")
    
    # 2. Limit particles
    content = content.replace("def add_particle(self, particle: Particle) -> None:",
                             "def add_particle(self, particle: Particle) -> None:\n        # Limit total particles for performance\n        if len(self.particles) >= 25:\n            return")
    
    # 3. Reduce object counts
    content = content.replace("if len(self.obstacles) < 3:", "if len(self.obstacles) < 2:  # Reduced for performance")
    content = content.replace("if len(self.other_cars) < 3:", "if len(self.other_cars) < 2:  # Reduced for performance")
    content = content.replace("if len(self.coins) < 10:", "if len(self.coins) < 6:  # Reduced for performance")
    
    # 4. Reduce spawn rates
    content = content.replace("if random.random() < 0.7:", "if random.random() < 0.3:  # Reduced for performance")
    
    # 5. Target lower FPS
    content = content.replace("self.clock.tick(60)", "self.clock.tick(30)  # Reduced for performance")
    
    # 6. Add background caching
    bg_cache = """
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
    
    # Find the draw_road method and add caching
    draw_road_pattern = r'def draw_road\(self\):\s+# Create gradient background for the road based on time of day'
    if re.search(draw_road_pattern, content):
        content = re.sub(draw_road_pattern, 
                        'def draw_road(self):\n' + bg_cache + '\n        # Create gradient background for the road based on time of day', 
                        content)
    
    # Write the optimized file
    with open('car_game_fixed.py', 'w') as f:
        f.write(content)
    
    print("Quick performance fixes applied!")
    print("Run the optimized game with: python3 car_game_fixed.py")

if __name__ == "__main__":
    apply_quick_fixes()
