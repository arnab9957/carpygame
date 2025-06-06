#!/usr/bin/env python3

# Read the file
with open('car_game_advanced_new.py', 'r') as file:
    content = file.readlines()

# Find the Game class definition
game_class_start = 0
for i, line in enumerate(content):
    if line.strip() == "class Game:":
        game_class_start = i
        break

# Find a good place to insert the sparkle methods - after the generate_stars method
insert_position = 0
for i in range(game_class_start, len(content)):
    if "def generate_stars" in content[i]:
        # Find the end of this method
        for j in range(i, len(content)):
            if content[j].strip() == "":
                insert_position = j
                break
        break

if insert_position > 0:
    # Define the sparkle methods with proper indentation
    sparkle_methods = """    def generate_sparkles(self, count):
        \"\"\"Generate sparkles for menu background animation\"\"\"
        self.sparkles = []
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.uniform(1, 3)
            brightness = random.uniform(0.5, 1.0)
            twinkle_speed = random.uniform(2.0, 5.0)  # Faster than stars
            color_choice = random.choice([
                (255, 255, 255),  # White
                (255, 255, 200),  # Warm white
                (200, 255, 255),  # Cool white
                (255, 215, 0),    # Gold
                (255, 255, 0),    # Yellow
            ])
            self.sparkles.append({
                "x": x,
                "y": y,
                "size": size,
                "brightness": brightness,
                "twinkle_speed": twinkle_speed,
                "twinkle_offset": random.uniform(0, 2 * math.pi),
                "color": color_choice,
                "direction": random.uniform(0, 2 * math.pi),
                "speed": random.uniform(0.2, 1.0)
            })
    
    def update_sparkles(self, dt):
        \"\"\"Update sparkle positions and properties\"\"\"
        for sparkle in self.sparkles:
            # Move sparkle in its direction
            sparkle["x"] += math.cos(sparkle["direction"]) * sparkle["speed"]
            sparkle["y"] += math.sin(sparkle["direction"]) * sparkle["speed"]
            
            # Wrap around screen edges
            if sparkle["x"] < 0:
                sparkle["x"] = SCREEN_WIDTH
            elif sparkle["x"] > SCREEN_WIDTH:
                sparkle["x"] = 0
            if sparkle["y"] < 0:
                sparkle["y"] = SCREEN_HEIGHT
            elif sparkle["y"] > SCREEN_HEIGHT:
                sparkle["y"] = 0
                
            # Occasionally change direction
            if random.random() < 0.01:
                sparkle["direction"] = random.uniform(0, 2 * math.pi)
                
            # Occasionally change speed
            if random.random() < 0.01:
                sparkle["speed"] = random.uniform(0.2, 1.0)
    
    def draw_sparkles(self, surface):
        \"\"\"Draw sparkles on the given surface\"\"\"
        current_time = pygame.time.get_ticks() / 1000
        for sparkle in self.sparkles:
            # Calculate twinkle effect
            twinkle = (math.sin(current_time * sparkle["twinkle_speed"] + sparkle["twinkle_offset"]) + 1) / 2
            brightness = sparkle["brightness"] * (0.3 + 0.7 * twinkle)
            
            # Calculate color with brightness
            color = tuple(int(c * brightness) for c in sparkle["color"])
            
            # Draw sparkle with glow effect
            for offset in range(3, 0, -1):
                glow_size = sparkle["size"] + offset * twinkle
                glow_alpha = int(255 * (1 - offset/3) * brightness)
                glow_color = (*color, glow_alpha)
                
                # Create a surface for the glow
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    glow_surface,
                    glow_color,
                    (glow_size, glow_size),
                    glow_size
                )
                surface.blit(
                    glow_surface,
                    (sparkle["x"] - glow_size, sparkle["y"] - glow_size)
                )
            
            # Draw the main sparkle
            pygame.draw.circle(
                surface,
                color,
                (int(sparkle["x"]), int(sparkle["y"])),
                sparkle["size"] * twinkle
            )

"""
    
    # Insert the sparkle methods
    content.insert(insert_position + 1, sparkle_methods)
    
    # Remove the old sparkle methods if they exist
    new_content = []
    skip_mode = False
    for line in content:
        if line.strip() == "def generate_sparkles(self, count):":
            skip_mode = True
        elif skip_mode and line.strip() == "":
            skip_mode = False
            continue
        
        if not skip_mode:
            new_content.append(line)
    
    # Write the modified content back to the file
    with open('car_game_advanced_new.py', 'w') as file:
        file.writelines(new_content)
    
    print("Fixed sparkle methods placement")
else:
    print("Could not find a suitable position to insert sparkle methods")
