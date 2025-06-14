#!/usr/bin/env python3
import os

def add_garage_menu():
    """Add the garage menu implementation directly to the file"""
    
    # Path to the game file
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_advanced_new.py"
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove any existing broken garage menu implementation
    if "def show_garage_menu(self, background_surface):" in content:
        print("Removing existing broken garage menu implementation...")
        lines = content.split('\n')
        new_lines = []
        skip = False
        for line in lines:
            if "def show_garage_menu(self, background_surface):" in line:
                skip = True
            elif skip and line.startswith("    def "):
                skip = False
            
            if not skip:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
    
    # Find a good place to insert the garage menu method
    # Let's look for the show_game_mode_menu method
    insert_point = content.find("    def show_game_mode_menu(self):")
    
    if insert_point == -1:
        print("Could not find insertion point!")
        return
    
    # Create the garage menu method
    garage_menu_code = """    def show_garage_menu(self, background_surface):
        \"\"\"Show the garage menu for car selection and customization\"\"\"
        # Define colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        NEON_YELLOW = (255, 255, 0)
        ELECTRIC_PURPLE = (191, 64, 191)
        NEON_GREEN = (57, 255, 20)
        SLEEK_SILVER = (204, 204, 204)
        BRIGHT_RED = (255, 62, 65)
        
        # Get current screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Create fonts
        title_font = get_font(48, bold=True)
        menu_font = get_font(36)
        info_font = get_font(24)
        
        # Available cars with their stats
        cars = [
            {
                "name": "SPORTS CAR",
                "image": "car.png",  # Default car image
                "speed": 8,
                "acceleration": 9,
                "handling": 7,
                "color": (255, 0, 0),  # Red
                "description": "Fast and agile sports car with excellent acceleration."
            },
            {
                "name": "MUSCLE CAR",
                "image": "car2.png",  # Use existing car image or create a new one
                "speed": 9,
                "acceleration": 7,
                "handling": 6,
                "color": (0, 0, 255),  # Blue
                "description": "Powerful muscle car with high top speed."
            },
            {
                "name": "COMPACT CAR",
                "image": "car3.png",  # Use existing car image or create a new one
                "speed": 6,
                "acceleration": 6,
                "handling": 9,
                "color": (0, 255, 0),  # Green
                "description": "Nimble compact car with excellent handling."
            }
        ]
        
        # Current car index
        current_car = 0
        
        # Load car images or create colored rectangles as placeholders
        car_images = []
        for car in cars:
            try:
                # Try to load the car image
                img = pygame.image.load(car["image"])
                img = pygame.transform.scale(img, (200, 100))  # Scale to appropriate size
                car_images.append(img)
            except:
                # Create a colored rectangle as placeholder
                img = pygame.Surface((200, 100), pygame.SRCALPHA)
                img.fill(car["color"])
                # Add some details to make it look like a car
                pygame.draw.rect(img, (0, 0, 0), (0, 0, 200, 100), 2)  # Border
                pygame.draw.rect(img, (0, 0, 0), (50, 20, 100, 40), 2)  # Windows
                pygame.draw.circle(img, (0, 0, 0), (50, 80), 15)  # Wheel
                pygame.draw.circle(img, (0, 0, 0), (150, 80), 15)  # Wheel
                car_images.append(img)
        
        # Main garage menu loop
        clock = pygame.time.Clock()
        running = True
        
        # Create button rectangles
        back_button_rect = pygame.Rect(0, 0, 100, 40)
        back_button_rect.center = (screen_width // 4, screen_height - 100)
        
        select_button_rect = pygame.Rect(0, 0, 100, 40)
        select_button_rect.center = (3 * screen_width // 4, screen_height - 100)
        
        left_arrow_rect = pygame.Rect(0, 0, 40, 40)
        left_arrow_rect.center = (screen_width // 4, screen_height // 2 - 50)
        
        right_arrow_rect = pygame.Rect(0, 0, 40, 40)
        right_arrow_rect.center = (3 * screen_width // 4, screen_height // 2 - 50)
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Return to main menu
                        return
                    elif event.key == pygame.K_LEFT:
                        # Previous car
                        current_car = (current_car - 1) % len(cars)
                        # Play selection sound
                        if sound_enabled and hasattr(self, "sound_menu_navigate"):
                            self.sound_menu_navigate.play()
                    elif event.key == pygame.K_RIGHT:
                        # Next car
                        current_car = (current_car + 1) % len(cars)
                        # Play selection sound
                        if sound_enabled and hasattr(self, "sound_menu_navigate"):
                            self.sound_menu_navigate.play()
                    elif event.key == pygame.K_RETURN:
                        # Select this car
                        # Here you would set the player's car choice
                        # For now, just play a sound and return
                        if sound_enabled and hasattr(self, "sound_menu_select"):
                            self.sound_menu_select.play()
                        print(f"Selected car: {cars[current_car]['name']}")
                        # Store the selected car
                        self.selected_car = current_car
                        return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if back button was clicked
                        if back_button_rect.collidepoint(event.pos):
                            # Play selection sound
                            if sound_enabled and hasattr(self, "sound_menu_select"):
                                self.sound_menu_select.play()
                            return
                        # Check if select button was clicked
                        elif select_button_rect.collidepoint(event.pos):
                            # Play selection sound
                            if sound_enabled and hasattr(self, "sound_menu_select"):
                                self.sound_menu_select.play()
                            print(f"Selected car: {cars[current_car]['name']}")
                            # Store the selected car
                            self.selected_car = current_car
                            return
                        # Check if left arrow was clicked
                        elif left_arrow_rect.collidepoint(event.pos):
                            # Previous car
                            current_car = (current_car - 1) % len(cars)
                            # Play selection sound
                            if sound_enabled and hasattr(self, "sound_menu_navigate"):
                                self.sound_menu_navigate.play()
                        # Check if right arrow was clicked
                        elif right_arrow_rect.collidepoint(event.pos):
                            # Next car
                            current_car = (current_car + 1) % len(cars)
                            # Play selection sound
                            if sound_enabled and hasattr(self, "sound_menu_navigate"):
                                self.sound_menu_navigate.play()
            
            # Draw background
            self.screen.blit(background_surface, (0, 0))
            
            # Draw sparkles animation
            self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
            self.draw_sparkles(self.screen)
            
            # Draw title
            title_text = title_font.render("GARAGE", True, NEON_YELLOW)
            title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 6))
            self.screen.blit(title_text, title_rect)
            
            # Draw car image
            car_image_rect = car_images[current_car].get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            self.screen.blit(car_images[current_car], car_image_rect)
            
            # Draw car name
            car_name_text = menu_font.render(cars[current_car]["name"], True, ELECTRIC_PURPLE)
            car_name_rect = car_name_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            self.screen.blit(car_name_text, car_name_rect)
            
            # Draw car stats
            stats_y = screen_height // 2 + 100
            stats_spacing = 30
            
            # Speed stat
            speed_text = info_font.render(f"Speed: {cars[current_car]['speed']}/10", True, WHITE)
            speed_rect = speed_text.get_rect(center=(screen_width // 2, stats_y))
            self.screen.blit(speed_text, speed_rect)
            
            # Acceleration stat
            accel_text = info_font.render(f"Acceleration: {cars[current_car]['acceleration']}/10", True, WHITE)
            accel_rect = accel_text.get_rect(center=(screen_width // 2, stats_y + stats_spacing))
            self.screen.blit(accel_text, accel_rect)
            
            # Handling stat
            handling_text = info_font.render(f"Handling: {cars[current_car]['handling']}/10", True, WHITE)
            handling_rect = handling_text.get_rect(center=(screen_width // 2, stats_y + 2 * stats_spacing))
            self.screen.blit(handling_text, handling_rect)
            
            # Draw car description
            desc_text = info_font.render(cars[current_car]["description"], True, SLEEK_SILVER)
            desc_rect = desc_text.get_rect(center=(screen_width // 2, stats_y + 3 * stats_spacing))
            self.screen.blit(desc_text, desc_rect)
            
            # Draw navigation arrows
            arrow_y = screen_height // 2 - 50
            
            # Left arrow
            left_arrow_text = menu_font.render("<", True, NEON_GREEN)
            left_arrow_rect = left_arrow_text.get_rect(center=(screen_width // 4, arrow_y))
            self.screen.blit(left_arrow_text, left_arrow_rect)
            
            # Right arrow
            right_arrow_text = menu_font.render(">", True, NEON_GREEN)
            right_arrow_rect = right_arrow_text.get_rect(center=(3 * screen_width // 4, arrow_y))
            self.screen.blit(right_arrow_text, right_arrow_rect)
            
            # Draw buttons
            button_y = screen_height - 100
            
            # Back button
            back_text = menu_font.render("BACK", True, BRIGHT_RED)
            back_button_rect = back_text.get_rect(center=(screen_width // 4, button_y))
            self.screen.blit(back_text, back_button_rect)
            
            # Select button
            select_text = menu_font.render("SELECT", True, NEON_GREEN)
            select_button_rect = select_text.get_rect(center=(3 * screen_width // 4, button_y))
            self.screen.blit(select_text, select_button_rect)
            
            # Draw car selection indicators
            indicator_y = screen_height - 50
            for i in range(len(cars)):
                if i == current_car:
                    # Current car indicator
                    pygame.draw.circle(self.screen, NEON_YELLOW, 
                                      (screen_width // 2 - (len(cars) - 1) * 15 + i * 30, indicator_y), 8)
                else:
                    # Other car indicator
                    pygame.draw.circle(self.screen, SLEEK_SILVER, 
                                      (screen_width // 2 - (len(cars) - 1) * 15 + i * 30, indicator_y), 5)
            
            # Update display
            pygame.display.flip()
            clock.tick(60)

"""
    
    # Insert the garage menu method
    updated_content = content[:insert_point] + garage_menu_code + content[insert_point:]
    
    # Write the updated content back to the file
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print("Garage menu added successfully!")

if __name__ == "__main__":
    add_garage_menu()
