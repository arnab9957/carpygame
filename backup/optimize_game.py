#!/usr/bin/env python3
"""
Performance optimizer for car_game_advanced_new.py
This script makes targeted changes to reduce lag in the game.
"""

import sys

def optimize_game(filename):
    print(f"Optimizing {filename}...")
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    optimized_lines = []
    
    # Track if we're in specific sections to modify
    in_particle_system = False
    in_draw_road = False
    draw_road_modified = False
    
    for line in lines:
        # 1. Reduce STAR_COUNT
        if "STAR_COUNT = " in line and "#" not in line.split("STAR_COUNT")[0]:
            line = "STAR_COUNT = 15  # Reduced for performance\n"
        
        # 2. Lower target FPS
        if "self.clock.tick(60)" in line:
            line = line.replace("self.clock.tick(60)", "self.clock.tick(30)  # Reduced for better performance")
        
        # 3. Reduce maximum number of obstacles
        if "if len(self.obstacles) < " in line:
            line = line.replace("if len(self.obstacles) < 3", "if len(self.obstacles) < 2  # Reduced for performance")
        
        # 4. Reduce maximum number of cars
        if "if len(self.other_cars) < " in line:
            line = line.replace("if len(self.other_cars) < 3", "if len(self.other_cars) < 2  # Reduced for performance")
        
        # 5. Increase spawn intervals
        if "if current_time - self.last_obstacle_time > random.uniform(2.0, 5.0)" in line:
            line = line.replace("random.uniform(2.0, 5.0)", "random.uniform(3.0, 6.0)  # Increased interval for performance")
        
        if "if current_time - self.last_car_time > random.uniform(3.0, 7.0)" in line:
            line = line.replace("random.uniform(3.0, 7.0)", "random.uniform(4.0, 8.0)  # Increased interval for performance")
        
        # 6. Track if we're in the ParticleSystem class
        if "class ParticleSystem:" in line:
            in_particle_system = True
        
        # 7. Modify add_particle method to limit particles
        if in_particle_system and "def add_particle(self, particle: Particle)" in line:
            optimized_lines.append(line)
            # Add particle limit code
            optimized_lines.append("        # Limit total particles for performance\n")
            optimized_lines.append("        if len(self.particles) >= 50:\n")
            optimized_lines.append("            return\n")
            continue
        
        # 8. Track if we're in draw_road method
        if "def draw_road(self):" in line:
            in_draw_road = True
            draw_road_modified = False
        
        # 9. Add background caching to draw_road method
        if in_draw_road and "# Create gradient background for the road based on time of day" in line and not draw_road_modified:
            optimized_lines.append(line)
            optimized_lines.append("        # Use cached background if available for better performance\n")
            optimized_lines.append("        if not hasattr(self, 'cached_background') or not hasattr(self, 'cached_day_phase') or abs(self.cached_day_phase - self.day_phase) > 0.01:\n")
            optimized_lines.append("            # Only recreate the background when the day phase changes significantly\n")
            optimized_lines.append("            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))\n")
            optimized_lines.append("            for y in range(SCREEN_HEIGHT):\n")
            optimized_lines.append("                # Get color for this y position\n")
            optimized_lines.append("                color = self.get_sky_color(y)\n")
            optimized_lines.append("                pygame.draw.line(background, color, (0, y), (SCREEN_WIDTH, y))\n")
            optimized_lines.append("            \n")
            optimized_lines.append("            # Cache the background and day phase\n")
            optimized_lines.append("            self.cached_background = background\n")
            optimized_lines.append("            self.cached_day_phase = self.day_phase\n")
            optimized_lines.append("        else:\n")
            optimized_lines.append("            # Use the cached background\n")
            optimized_lines.append("            background = self.cached_background\n")
            draw_road_modified = True
            
            # Skip the next few lines that create the background
            continue
        
        # Skip the original background creation code if we've already added our optimized version
        if in_draw_road and draw_road_modified and ("background = pygame.Surface" in line or 
                                                  "for y in range(SCREEN_HEIGHT)" in line or
                                                  "color = self.get_sky_color" in line or
                                                  "pygame.draw.line(background, color" in line):
            continue
        
        # 10. Reduce particle effects in create_crash
        if "self.create_spark(x, y, count=50," in line:
            line = line.replace("count=50", "count=15  # Reduced for performance")
        
        if "self.create_smoke(x, y, count=15)" in line:
            line = line.replace("count=15", "count=5  # Reduced for performance")
        
        # Add the line to our optimized version
        optimized_lines.append(line)
    
    # Write optimized content back to file
    optimized_filename = filename.replace('.py', '_optimized.py')
    with open(optimized_filename, 'w') as file:
        file.writelines(optimized_lines)
    
    print(f"Optimization complete! Optimized file saved as {optimized_filename}")
    print("Run the optimized version with: python3 " + optimized_filename)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        optimize_game(sys.argv[1])
    else:
        optimize_game("car_game_advanced_new.py")
