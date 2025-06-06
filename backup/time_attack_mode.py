#!/usr/bin/env python3
"""
Time Attack Mode Implementation for Car Racing Game
"""

# Time Attack mission types
TIME_ATTACK_SURVIVE = 0
TIME_ATTACK_AVOID_OBSTACLES = 1
TIME_ATTACK_MAINTAIN_SPEED = 2
TIME_ATTACK_COLLECT_ITEMS = 3
TIME_ATTACK_PASS_CARS = 4
TIME_ATTACK_REACH_SCORE = 5

# Time Attack constants
TIME_ATTACK_INITIAL_TIME = 60  # Initial time in seconds
TIME_ATTACK_BONUS_TIME = 5     # Bonus time from power-ups
TIME_ATTACK_WARNING_TIME = 10  # Time when warning effects start

# Add these functions to the Game class

def reset_game_time_attack(self):
    """Reset game state for Time Attack mode"""
    # Set game mode
    self.game_mode = GAME_MODE_TIME_ATTACK
    
    # Initialize Time Attack specific variables
    self.time_remaining = TIME_ATTACK_INITIAL_TIME
    self.time_attack_mission_type = random.randint(0, 5)  # Random Time Attack mission
    self.time_attack_target = 0
    self.time_attack_progress = 0
    self.time_attack_speed_timer = 0  # For speed maintenance mission
    self.time_attack_passed_cars = 0  # For passing cars mission
    self.time_attack_avoided_obstacles = 0  # For avoiding obstacles mission
    
    # Set the first mission
    self.set_time_attack_mission()
    
    # Reset other game variables
    self.score = 0
    self.speed = 5
    self.obstacles = []
    self.powerups = []
    self.coins = []
    self.combo_count = 0
    self.combo_timer = 0
    self.score_multiplier = 1
    self.distance_traveled = 0
    self.start_time = time.time()
    self.powerups_used = 0
    self.game_over = False
    self.game_has_been_played = True

def set_time_attack_mission(self):
    """Set up a random Time Attack mission"""
    self.time_attack_mission_type = random.randint(0, 5)
    
    if self.time_attack_mission_type == TIME_ATTACK_SURVIVE:
        # Survive for X seconds without crashing
        self.time_attack_target = random.randint(20, 40)
        self.time_attack_progress = 0
        
    elif self.time_attack_mission_type == TIME_ATTACK_AVOID_OBSTACLES:
        # Avoid Y obstacles before time runs out
        self.time_attack_target = random.randint(10, 20)
        self.time_attack_avoided_obstacles = 0
        
    elif self.time_attack_mission_type == TIME_ATTACK_MAINTAIN_SPEED:
        # Reach a certain speed and maintain it for Z seconds
        self.time_attack_target = random.randint(5, 10)  # seconds to maintain speed
        self.time_attack_speed_timer = 0
        
    elif self.time_attack_mission_type == TIME_ATTACK_COLLECT_ITEMS:
        # Collect N power-ups or coins within the time limit
        self.time_attack_target = random.randint(10, 20)
        self.time_attack_progress = 0
        
    elif self.time_attack_mission_type == TIME_ATTACK_PASS_CARS:
        # Pass M non-player cars in 30 seconds
        self.time_attack_target = random.randint(10, 20)
        self.time_attack_passed_cars = 0
        
    elif self.time_attack_mission_type == TIME_ATTACK_REACH_SCORE:
        # Reach X score before the clock hits zero
        self.time_attack_target = random.randint(500, 1000)
        # Progress will be tracked by the score itself

def get_time_attack_mission_text(self):
    """Get the text description of the current Time Attack mission"""
    if self.time_attack_mission_type == TIME_ATTACK_SURVIVE:
        return f"Survive for {self.time_attack_target}s without crashing: {int(self.time_attack_progress)}s"
        
    elif self.time_attack_mission_type == TIME_ATTACK_AVOID_OBSTACLES:
        return f"Avoid {self.time_attack_target} obstacles: {self.time_attack_avoided_obstacles}/{self.time_attack_target}"
        
    elif self.time_attack_mission_type == TIME_ATTACK_MAINTAIN_SPEED:
        target_speed = 200  # km/h
        return f"Maintain {target_speed}+ km/h for {self.time_attack_target}s: {int(self.time_attack_speed_timer)}s"
        
    elif self.time_attack_mission_type == TIME_ATTACK_COLLECT_ITEMS:
        return f"Collect {self.time_attack_target} coins: {self.time_attack_progress}/{self.time_attack_target}"
        
    elif self.time_attack_mission_type == TIME_ATTACK_PASS_CARS:
        return f"Pass {self.time_attack_target} cars: {self.time_attack_passed_cars}/{self.time_attack_target}"
        
    elif self.time_attack_mission_type == TIME_ATTACK_REACH_SCORE:
        return f"Reach {self.time_attack_target} points: {self.score}/{self.time_attack_target}"
        
    return "Unknown mission"

def update_time_attack_mission(self, dt):
    """Update the progress of the current Time Attack mission"""
    if self.time_attack_mission_type == TIME_ATTACK_SURVIVE:
        # Update survival time
        self.time_attack_progress += dt
        
        # Check if mission is complete
        if self.time_attack_progress >= self.time_attack_target:
            self.complete_time_attack_mission()
            
    elif self.time_attack_mission_type == TIME_ATTACK_MAINTAIN_SPEED:
        # Check if speed is above threshold
        speed_value = int(self.speed * 10)
        if self.player_car.has_boost:
            speed_value = int(self.speed * BOOST_MULTIPLIER * 10)
            
        if speed_value >= 200:  # 200 km/h threshold
            self.time_attack_speed_timer += dt
        else:
            self.time_attack_speed_timer = 0  # Reset if speed drops
            
        # Check if mission is complete
        if self.time_attack_speed_timer >= self.time_attack_target:
            self.complete_time_attack_mission()
            
    elif self.time_attack_mission_type == TIME_ATTACK_REACH_SCORE:
        # Check if score target is reached
        if self.score >= self.time_attack_target:
            self.complete_time_attack_mission()
            
def complete_time_attack_mission(self):
    """Handle completion of a Time Attack mission"""
    # Add bonus time
    self.time_remaining += TIME_ATTACK_BONUS_TIME
    
    # Play success sound
    if sound_enabled and hasattr(self, "sound_powerup"):
        self.sound_powerup.play()
        
    # Add score bonus
    self.score += 100
    
    # Set a new mission
    self.set_time_attack_mission()
    
def create_time_bonus_powerup(self):
    """Create a time bonus power-up for Time Attack mode"""
    # Only create if in Time Attack mode
    if self.game_mode != GAME_MODE_TIME_ATTACK:
        return
        
    # Random chance to create a time bonus
    if random.random() < 0.05:  # 5% chance
        lane = random.randint(0, 5)
        x = LANE_POSITIONS[lane]
        y = -POWERUP_HEIGHT
        
        # Create a special time bonus powerup
        powerup = {
            "type": "time_bonus",
            "x": x,
            "y": y,
            "width": POWERUP_WIDTH,
            "height": POWERUP_HEIGHT,
            "lane": lane,
            "collected": False,
            "color": (255, 215, 0),  # Gold color
            "text": "+5s",
        }
        
        self.powerups.append(powerup)

def update_time_attack(self, dt):
    """Update Time Attack mode specific logic"""
    # Update time remaining
    self.time_remaining -= dt
    
    # Check if time is up
    if self.time_remaining <= 0:
        self.game_over = True
        self.game_has_been_played = True
        # Play game over sound
        if sound_enabled and hasattr(self, "sound_game_over"):
            self.sound_game_over.play()
        return
    
    # Update current mission
    self.update_time_attack_mission(dt)
    
    # Increase difficulty as time decreases
    difficulty_factor = 1.0 + max(0, (TIME_ATTACK_INITIAL_TIME - self.time_remaining) / TIME_ATTACK_INITIAL_TIME)
    
    # Adjust obstacle generation rate based on difficulty
    self.obstacle_rate = 0.02 * difficulty_factor
    
    # Adjust speed based on difficulty
    self.speed = min(self.speed + SPEED_INCREMENT * difficulty_factor, 30)
    
    # Create time bonus powerups occasionally
    self.create_time_bonus_powerup()
    
    # Handle obstacle avoidance tracking for that mission type
    if self.time_attack_mission_type == TIME_ATTACK_AVOID_OBSTACLES:
        # Count obstacles that have passed the player without collision
        for obstacle in self.obstacles[:]:
            if obstacle["y"] > SCREEN_HEIGHT and not obstacle.get("counted", False):
                self.time_attack_avoided_obstacles += 1
                obstacle["counted"] = True
                
                # Check if mission is complete
                if self.time_attack_avoided_obstacles >= self.time_attack_target:
                    self.complete_time_attack_mission()
    
    # Handle car passing tracking for that mission type
    if self.time_attack_mission_type == TIME_ATTACK_PASS_CARS:
        # Count cars that have been passed
        for obstacle in self.obstacles[:]:
            if obstacle["y"] > self.player_car.y and not obstacle.get("passed", False):
                self.time_attack_passed_cars += 1
                obstacle["passed"] = True
                
                # Check if mission is complete
                if self.time_attack_passed_cars >= self.time_attack_target:
                    self.complete_time_attack_mission()

def draw_time_attack_ui(self):
    """Draw Time Attack mode specific UI elements"""
    # Draw time remaining
    time_text = self.font_medium.render(
        f"TIME: {int(self.time_remaining)}s", True, BRIGHT_RED
    )
    time_shadow = self.font_medium.render(
        f"TIME: {int(self.time_remaining)}s",
        True,
        (BRIGHT_RED[0] // 3, BRIGHT_RED[1] // 3, BRIGHT_RED[2] // 3),
    )
    self.screen.blit(time_shadow, (SCREEN_WIDTH - 152, 52))
    self.screen.blit(time_text, (SCREEN_WIDTH - 150, 50))
    
    # Draw current mission
    mission_text = self.font_small.render(
        self.get_time_attack_mission_text(), True, ELECTRIC_PURPLE
    )
    mission_shadow = self.font_small.render(
        self.get_time_attack_mission_text(),
        True,
        (ELECTRIC_PURPLE[0] // 3, ELECTRIC_PURPLE[1] // 3, ELECTRIC_PURPLE[2] // 3),
    )
    self.screen.blit(mission_shadow, (SCREEN_WIDTH // 2 - 202, 52))
    self.screen.blit(mission_text, (SCREEN_WIDTH // 2 - 200, 50))
    
    # Add flashing border when time is low
    if self.time_remaining <= TIME_ATTACK_WARNING_TIME:
        # Calculate flash intensity (pulsating effect)
        flash_intensity = abs(math.sin(time.time() * 5)) * 255
        border_color = (255, 0, 0, flash_intensity)
        
        # Create a surface for the border
        border = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw border lines
        border_width = 5
        pygame.draw.rect(border, border_color, (0, 0, SCREEN_WIDTH, border_width))  # Top
        pygame.draw.rect(border, border_color, (0, 0, border_width, SCREEN_HEIGHT))  # Left
        pygame.draw.rect(border, border_color, (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width))  # Bottom
        pygame.draw.rect(border, border_color, (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT))  # Right
        
        # Blit the border to the screen
        self.screen.blit(border, (0, 0))

def handle_powerup_collection_time_attack(self, powerup):
    """Handle collection of powerups in Time Attack mode"""
    if powerup["type"] == "time_bonus":
        # Add time to the clock
        self.time_remaining += TIME_ATTACK_BONUS_TIME
        
        # Play powerup sound
        if sound_enabled and hasattr(self, "sound_powerup"):
            self.sound_powerup.play()
            
        # Show floating text
        self.particle_system.create_floating_text(
            powerup["x"], powerup["y"], f"+{TIME_ATTACK_BONUS_TIME}s", (255, 215, 0)
        )
        
        # Track for collect items mission
        if self.time_attack_mission_type == TIME_ATTACK_COLLECT_ITEMS:
            self.time_attack_progress += 1
            
            # Check if mission is complete
            if self.time_attack_progress >= self.time_attack_target:
                self.complete_time_attack_mission()
    else:
        # Handle regular powerups
        # Track for collect items mission if it's that type
        if self.time_attack_mission_type == TIME_ATTACK_COLLECT_ITEMS:
            self.time_attack_progress += 1
            
            # Check if mission is complete
            if self.time_attack_progress >= self.time_attack_target:
                self.complete_time_attack_mission()

# Modifications to existing functions:

def update_game(self, dt):
    """Main game update function"""
    # ... existing code ...
    
    # Add Time Attack specific updates
    if self.game_mode == GAME_MODE_TIME_ATTACK:
        self.update_time_attack(dt)
    
    # ... rest of existing code ...

def draw_game(self):
    """Main game drawing function"""
    # ... existing code ...
    
    # Add Time Attack specific UI
    if self.game_mode == GAME_MODE_TIME_ATTACK:
        self.draw_time_attack_ui()
    
    # ... rest of existing code ...

def handle_coin_collection(self, coin):
    """Handle coin collection"""
    # ... existing code ...
    
    # Track for collect items mission in Time Attack mode
    if self.game_mode == GAME_MODE_TIME_ATTACK and self.time_attack_mission_type == TIME_ATTACK_COLLECT_ITEMS:
        self.time_attack_progress += 1
        
        # Check if mission is complete
        if self.time_attack_progress >= self.time_attack_target:
            self.complete_time_attack_mission()
    
    # ... rest of existing code ...
