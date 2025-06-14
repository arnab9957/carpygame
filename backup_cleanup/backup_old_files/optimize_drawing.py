#!/usr/bin/env python3
import re

def optimize_drawing():
    """Optimize the drawing methods for better performance"""
    print("Optimizing drawing methods for better performance...")
    
    with open('car_game_optimized.py', 'r') as f:
        content = f.read()
    
    # Optimize draw_road method
    draw_road_match = re.search(r'def draw_road\(self\):(.*?)def draw\(self\):', content, re.DOTALL)
    if not draw_road_match:
        print("Could not find draw_road method, skipping optimization")
        return
    
    draw_road = draw_road_match.group(1)
    
    # Optimize star drawing to only draw a subset of stars
    optimized_stars = """
        # Draw stars if it's night time (between 0.5 and 1.0)
        if 0.4 < self.day_phase < 0.9:
            # Calculate star visibility (0 at day, 1 at full night)
            star_visibility = 0
            if 0.4 < self.day_phase < 0.5:
                star_visibility = (self.day_phase - 0.4) * 10  # Fade in
            elif 0.5 <= self.day_phase < 0.75:
                star_visibility = 1.0  # Full visibility
            elif 0.75 <= self.day_phase < 0.9:
                star_visibility = (0.9 - self.day_phase) * 6.67  # Fade out

            # Only draw a subset of stars for better performance
            current_time = pygame.time.get_ticks() / 1000
            for i, star in enumerate(self.stars):
                # Only draw every other star to improve performance
                if i % 2 == 0:
                    # Calculate twinkle effect
                    twinkle = (
                        math.sin(
                            current_time * star["twinkle_speed"] + star["twinkle_offset"]
                        )
                        + 1
                    ) / 2
                    brightness = (
                        star["brightness"] * (0.7 + 0.3 * twinkle) * star_visibility
                    )

                # Draw star with appropriate brightness
                color = (
                    int(255 * brightness),
                    int(255 * brightness),
                    int(255 * brightness),
                )
                pygame.draw.circle(
                    self.screen, color, (star["x"], star["y"]), star["size"]
                )
    """
    
    # Replace the star drawing code
    updated_draw_road = re.sub(r'# Draw stars if it\'s night time.*?pygame\.draw\.circle\(\s*self\.screen, color, \(star\["x"\], star\["y"\]\), star\["size"\]\s*\)', 
                              optimized_stars, draw_road, flags=re.DOTALL)
    
    # Optimize lane markings drawing
    optimized_lane_markings = """
        # Draw lane markings with metallic effect - only draw every other frame for performance
        if pygame.time.get_ticks() % 2 == 0:
            for i in range(7):  # Changed from 5 to 7 for 6 lanes
                x = i * LANE_WIDTH
                pygame.draw.line(
                    self.screen, METALLIC_SILVER, (x, 0), (x, SCREEN_HEIGHT), 3
                )

            # Draw dashed lines in the middle of lanes with neon effect - simplified
            for i in range(1, 6):  # Changed from 1-4 to 1-6 for 6 lanes
                x = i * LANE_WIDTH
                for y in range(0, SCREEN_HEIGHT, 80):  # Increased spacing from 40 to 80
                    pygame.draw.line(self.screen, WHITE, (x, y), (x, y + 20), 2)
        """
    
    # Replace the lane markings code
    updated_draw_road = re.sub(r'# Draw lane markings with metallic effect.*?pygame\.draw\.line\(self\.screen, WHITE, \(x, y\), \(x, y \+ 20\), 2\)', 
                              optimized_lane_markings, updated_draw_road, flags=re.DOTALL)
    
    # Update the draw_road method in the content
    updated_content = content.replace(draw_road, updated_draw_road)
    
    # Optimize the draw method to skip some visual effects
    draw_match = re.search(r'def draw\(self\):(.*?)def update\(self\):', updated_content, re.DOTALL)
    if draw_match:
        draw_method = draw_match.group(1)
        
        # Skip some visual effects when there are many objects on screen
        performance_check = """
            # Skip some visual effects when there are many objects for better performance
            skip_effects = len(self.obstacles) + len(self.other_cars) + len(self.powerups) + len(self.coins) > 10
        """
        
        # Add performance check at the beginning of the draw method
        updated_draw = draw_method.replace("try:", "try:\n" + performance_check)
        
        # Skip some effects conditionally
        updated_draw = updated_draw.replace("# Apply slow motion effect if active", 
                                          "# Apply slow motion effect if active and not skipping effects\n            if not skip_effects:")
        
        # Update the draw method in the content
        updated_content = updated_content.replace(draw_method, updated_draw)
    
    # Write the optimized file
    with open('car_game_optimized.py', 'w') as f:
        f.write(updated_content)
    
    print("Drawing methods optimized successfully")

if __name__ == "__main__":
    optimize_drawing()
