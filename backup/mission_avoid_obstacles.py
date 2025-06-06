#!/usr/bin/env python3
"""
Implementation of the "Avoid 25 obstacles in one run without missing more than 2" mission
for the Car Racing Game.

This file contains the code to add a new mission type to the game that challenges
players to avoid a specific number of obstacles with limited misses allowed.
"""

# Add this constant to the mission types section in car_game_final.py
# MISSION_AVOID_OBSTACLES_PRECISE = 4

def update_mission_constants(file_path):
    """Update the mission constants in the game file"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the mission types section
    mission_types_section = "# Mission types\nMISSION_COLLECT_COINS = 0\nMISSION_DISTANCE = 1\nMISSION_AVOID_CRASHES = 2\nMISSION_USE_POWERUPS = 3\n"
    
    # Add the new mission type
    new_mission_types_section = mission_types_section + "MISSION_AVOID_OBSTACLES_PRECISE = 4\n"
    
    # Replace the section in the content
    updated_content = content.replace(mission_types_section, new_mission_types_section)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated mission constants in {file_path}")

def update_set_mission_method(file_path):
    """Update the set_mission method to include the new mission type"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the set_mission method
    set_mission_method = """    def set_mission(self):
        if self.mission_type == MISSION_COLLECT_COINS:
            self.mission_target = random.randint(10, 30)
            self.mission_description = f"Collect {self.mission_target} coins"
        elif self.mission_type == MISSION_DISTANCE:
            self.mission_target = random.randint(1000, 3000)
            self.mission_description = f"Travel {self.mission_target}m"
        elif self.mission_type == MISSION_AVOID_CRASHES:
            self.mission_target = random.randint(30, 60)
            self.mission_description = f"Survive {self.mission_target} seconds"
        elif self.mission_type == MISSION_USE_POWERUPS:
            self.mission_target = random.randint(3, 8)
            self.mission_description = f"Use {self.mission_target} power-ups"
"""
    
    # Add the new mission type to the method
    new_set_mission_method = """    def set_mission(self):
        if self.mission_type == MISSION_COLLECT_COINS:
            self.mission_target = random.randint(10, 30)
            self.mission_description = f"Collect {self.mission_target} coins"
        elif self.mission_type == MISSION_DISTANCE:
            self.mission_target = random.randint(1000, 3000)
            self.mission_description = f"Travel {self.mission_target}m"
        elif self.mission_type == MISSION_AVOID_CRASHES:
            self.mission_target = random.randint(30, 60)
            self.mission_description = f"Survive {self.mission_target} seconds"
        elif self.mission_type == MISSION_USE_POWERUPS:
            self.mission_target = random.randint(3, 8)
            self.mission_description = f"Use {self.mission_target} power-ups"
        elif self.mission_type == MISSION_AVOID_OBSTACLES_PRECISE:
            self.mission_target = 25  # Need to avoid 25 obstacles
            self.mission_failures = 0  # Obstacles missed (max 2 allowed)
            self.mission_description = f"Avoid 25 obstacles without missing more than 2"
"""
    
    # Replace the method in the content
    updated_content = content.replace(set_mission_method, new_set_mission_method)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated set_mission method in {file_path}")

def update_update_mission_progress_method(file_path):
    """Update the update_mission_progress method to handle the new mission type"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the update_mission_progress method
    update_mission_progress_method = """    def update_mission_progress(self):
        if self.game_mode != GAME_MODE_MISSIONS:
            return

        if self.mission_type == MISSION_COLLECT_COINS:
            self.mission_progress = self.coins_collected
        elif self.mission_type == MISSION_DISTANCE:
            self.mission_progress = int(self.distance_traveled)
        elif self.mission_type == MISSION_AVOID_CRASHES:
            self.mission_progress = int(time.time() - self.start_time)
        elif self.mission_type == MISSION_USE_POWERUPS:
            self.mission_progress = self.powerups_used

        # Check if mission is complete
        if self.mission_progress >= self.mission_target:
            self.score += 100  # Bonus for completing mission
            self.mission_type = (self.mission_type + 1) % 4
            self.set_mission()
            self.mission_progress = 0
"""
    
    # Add the new mission type to the method
    new_update_mission_progress_method = """    def update_mission_progress(self):
        if self.game_mode != GAME_MODE_MISSIONS:
            return

        if self.mission_type == MISSION_COLLECT_COINS:
            self.mission_progress = self.coins_collected
        elif self.mission_type == MISSION_DISTANCE:
            self.mission_progress = int(self.distance_traveled)
        elif self.mission_type == MISSION_AVOID_CRASHES:
            self.mission_progress = int(time.time() - self.start_time)
        elif self.mission_type == MISSION_USE_POWERUPS:
            self.mission_progress = self.powerups_used
        elif self.mission_type == MISSION_AVOID_OBSTACLES_PRECISE:
            # Progress is tracked separately when obstacles are avoided
            pass

        # Check if mission is complete
        if self.mission_progress >= self.mission_target:
            self.score += 100  # Bonus for completing mission
            self.mission_type = (self.mission_type + 1) % 5  # Updated to include new mission type
            self.set_mission()
            self.mission_progress = 0
"""
    
    # Replace the method in the content
    updated_content = content.replace(update_mission_progress_method, new_update_mission_progress_method)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated update_mission_progress method in {file_path}")

def add_obstacle_tracking_methods(file_path):
    """Add methods to track obstacles for the new mission type"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find a good insertion point - after the update_mission_progress method
    insertion_point = """    def handle_events(self):
        try:
            global SCREEN_WIDTH, SCREEN_HEIGHT, LANE_WIDTH, LANE_POSITIONS"""
    
    # New methods to add
    new_methods = """    def track_avoided_obstacle(self, obstacle):
        # Track when an obstacle is successfully avoided for the precise avoidance mission
        if self.game_mode != GAME_MODE_MISSIONS or self.mission_type != MISSION_AVOID_OBSTACLES_PRECISE:
            return
            
        # Mark the obstacle as counted to avoid counting it multiple times
        if not obstacle.get("counted", False):
            obstacle["counted"] = True
            self.mission_progress += 1
            
            # Check if mission is complete
            if self.mission_progress >= self.mission_target:
                self.score += 100  # Bonus for completing mission
                self.mission_type = (self.mission_type + 1) % 5
                self.set_mission()
                self.mission_progress = 0
                
                # Show mission complete prompt
                if hasattr(self, "prompt_system"):
                    self.prompt_system.show_prompt("mission_complete")
    
    def track_obstacle_collision(self):
        # Track when the player collides with an obstacle for the precise avoidance mission
        if self.game_mode != GAME_MODE_MISSIONS or self.mission_type != MISSION_AVOID_OBSTACLES_PRECISE:
            return
            
        # Increment failure counter
        self.mission_failures += 1
        
        # Check if mission failed (more than 2 misses)
        if self.mission_failures > 2:
            # Mission failed - set a new mission
            self.mission_type = (self.mission_type + 1) % 5
            self.set_mission()
            self.mission_progress = 0
            
            # Show mission failed prompt
            if hasattr(self, "prompt_system"):
                self.prompt_system.show_prompt("mission_failed")

    def handle_events(self):
        try:
            global SCREEN_WIDTH, SCREEN_HEIGHT, LANE_WIDTH, LANE_POSITIONS"""
    
    # Insert the new methods
    updated_content = content.replace(insertion_point, new_methods)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Added obstacle tracking methods to {file_path}")

def update_obstacle_handling(file_path):
    """Update the obstacle handling code to track avoidances and collisions"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the obstacle update code
    obstacle_update_code = """            # Move and check obstacles
            for obstacle in self.obstacles[:]:
                obstacle["y"] += self.speed * speed_factor
                
                if obstacle["y"] > SCREEN_HEIGHT:
                    self.obstacles.remove(obstacle)
                elif self.player_car.collides_with_obstacle(obstacle) and not self.player_car.has_shield:
                    # Collision with obstacle
                    self.game_over = True
                    self.game_has_been_played = True  # Mark that a game has been played
                    
                    # Play crash sound
                    if sound_enabled and hasattr(self, "sound_crash"):
                        self.sound_crash.play()
                        
                    # Create explosion effect
                    self.particle_system.create_explosion(self.player_car.x, self.player_car.y)
                    
                    # Start crash animation
                    self.crash_animation_timer = 1.0  # 1 second animation
                    self.crash_animation_start_time = time.time()
                    
                    return"""
    
    # Updated code to track obstacle avoidance and collisions
    new_obstacle_update_code = """            # Move and check obstacles
            for obstacle in self.obstacles[:]:
                obstacle["y"] += self.speed * speed_factor
                
                if obstacle["y"] > SCREEN_HEIGHT:
                    # Obstacle passed without collision - track for precise avoidance mission
                    self.track_avoided_obstacle(obstacle)
                    self.obstacles.remove(obstacle)
                elif self.player_car.collides_with_obstacle(obstacle) and not self.player_car.has_shield:
                    # Collision with obstacle
                    # Track for precise avoidance mission
                    self.track_obstacle_collision()
                    
                    self.game_over = True
                    self.game_has_been_played = True  # Mark that a game has been played
                    
                    # Play crash sound
                    if sound_enabled and hasattr(self, "sound_crash"):
                        self.sound_crash.play()
                        
                    # Create explosion effect
                    self.particle_system.create_explosion(self.player_car.x, self.player_car.y)
                    
                    # Start crash animation
                    self.crash_animation_timer = 1.0  # 1 second animation
                    self.crash_animation_start_time = time.time()
                    
                    return"""
    
    # Replace the code
    updated_content = content.replace(obstacle_update_code, new_obstacle_update_code)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated obstacle handling in {file_path}")

def update_mission_display(file_path):
    """Update the mission display to show failures for the precise avoidance mission"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the mission display code
    mission_display_code = """                # Draw mission progress
                mission_text = score_font.render(
                    f"{self.mission_description}: {self.mission_progress}/{self.mission_target}",
                    True,
                    ELECTRIC_PURPLE,
                )
                mission_shadow = score_font.render(
                    f"{self.mission_description}: {self.mission_progress}/{self.mission_target}",
                    True,
                    (
                        ELECTRIC_PURPLE[0] // 3,
                        ELECTRIC_PURPLE[1] // 3,
                        ELECTRIC_PURPLE[2] // 3,
                    ),
                )
                self.screen.blit(mission_shadow, (SCREEN_WIDTH // 2 - 202, 52))
                self.screen.blit(mission_text, (SCREEN_WIDTH // 2 - 200, 50))"""
    
    # Updated code to show failures for precise avoidance mission
    new_mission_display_code = """                # Draw mission progress
                if self.mission_type == MISSION_AVOID_OBSTACLES_PRECISE:
                    mission_text = score_font.render(
                        f"{self.mission_description}: {self.mission_progress}/{self.mission_target} (Misses: {self.mission_failures}/2)",
                        True,
                        ELECTRIC_PURPLE,
                    )
                    mission_shadow = score_font.render(
                        f"{self.mission_description}: {self.mission_progress}/{self.mission_target} (Misses: {self.mission_failures}/2)",
                        True,
                        (
                            ELECTRIC_PURPLE[0] // 3,
                            ELECTRIC_PURPLE[1] // 3,
                            ELECTRIC_PURPLE[2] // 3,
                        ),
                    )
                else:
                    mission_text = score_font.render(
                        f"{self.mission_description}: {self.mission_progress}/{self.mission_target}",
                        True,
                        ELECTRIC_PURPLE,
                    )
                    mission_shadow = score_font.render(
                        f"{self.mission_description}: {self.mission_progress}/{self.mission_target}",
                        True,
                        (
                            ELECTRIC_PURPLE[0] // 3,
                            ELECTRIC_PURPLE[1] // 3,
                            ELECTRIC_PURPLE[2] // 3,
                        ),
                    )
                self.screen.blit(mission_shadow, (SCREEN_WIDTH // 2 - 202, 52))
                self.screen.blit(mission_text, (SCREEN_WIDTH // 2 - 200, 50))"""
    
    # Replace the code
    updated_content = content.replace(mission_display_code, new_mission_display_code)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated mission display in {file_path}")

def add_mission_failed_prompt(file_path):
    """Add a mission failed prompt to the prompt system"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the prompt definitions
    prompt_definitions = """            "mission_complete": {
                "text": "Mission complete! Get ready for the next challenge.",
                "duration": 3.0,
                "shown": False,
            },"""
    
    # Add the mission failed prompt
    new_prompt_definitions = """            "mission_complete": {
                "text": "Mission complete! Get ready for the next challenge.",
                "duration": 3.0,
                "shown": False,
            },
            "mission_failed": {
                "text": "Mission failed! Too many obstacles hit. Try a new mission.",
                "duration": 3.0,
                "shown": False,
            },"""
    
    # Replace the code
    updated_content = content.replace(prompt_definitions, new_prompt_definitions)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Added mission failed prompt to {file_path}")

def update_reset_game_method(file_path):
    """Update the reset_game method to initialize mission_failures"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the reset_game method
    reset_game_code = """        self.mission_type = random.randint(
            0, 3
        )  # Keep this as is - it's for mission types, not lanes
        self.mission_target = 0
        self.mission_progress = 0
        self.set_mission()"""
    
    # Updated code to initialize mission_failures
    new_reset_game_code = """        self.mission_type = random.randint(
            0, 4
        )  # Updated to include the new mission type
        self.mission_target = 0
        self.mission_progress = 0
        self.mission_failures = 0  # Initialize failures counter for precise avoidance mission
        self.set_mission()"""
    
    # Replace the code
    updated_content = content.replace(reset_game_code, new_reset_game_code)
    
    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated reset_game method in {file_path}")

if __name__ == "__main__":
    file_path = "/mnt/c/Users/ARNAB/Desktop/AWS_Q_CLI/car_game_final.py"
    
    # Make all the necessary updates
    update_mission_constants(file_path)
    update_set_mission_method(file_path)
    update_update_mission_progress_method(file_path)
    add_obstacle_tracking_methods(file_path)
    update_obstacle_handling(file_path)
    update_mission_display(file_path)
    add_mission_failed_prompt(file_path)
    update_reset_game_method(file_path)
    
    print("All updates completed successfully!")
    print("The 'Avoid 25 obstacles in one run without missing more than 2' mission has been added to the game.")
