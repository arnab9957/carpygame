import pygame
import random
import math
import time
from typing import List, Dict, Any, Optional, Tuple

# This file contains the Race Mode implementation for the car racing game

class RaceOpponent:
    """AI-controlled opponent for race mode"""
    def __init__(self, lane, position=0, difficulty=1, lane_positions=None, car_width=60, car_height=120):
        self.lane = lane
        self.lane_positions = lane_positions
        self.x = self.lane_positions[lane]
        self.y = 0  # Will be calculated based on relative position
        self.width = car_width
        self.height = car_height
        self.position = position  # Race position (distance traveled)
        self.speed = 5 * (0.8 + difficulty * 0.1)  # Speed based on difficulty
        self.color = random.choice([
            (255, 0, 0),    # Red
            (0, 0, 255),    # Blue
            (0, 255, 0),    # Green
            (255, 255, 0),  # Yellow
            (128, 0, 128)   # Purple
        ])
        self.difficulty = difficulty  # 1-5, affects AI behavior
        self.lane_change_cooldown = 0
        self.target_lane = lane
        self.is_car = True  # Flag to identify as a car for collision detection
        self.finished = False
        self.finish_time = 0
        self.name = f"Racer {lane+1}"
        
    def draw(self, screen, player_position, screen_height):
        # Calculate relative position based on player's position
        relative_position = self.position - player_position
        
        # Convert relative position to screen coordinates
        screen_y = screen_height - 150 - relative_position
        
        # Only draw if on screen
        if -self.height < screen_y < screen_height + self.height:
            # Car body
            pygame.draw.rect(
                screen,
                self.color,
                [
                    self.x - self.width // 2,
                    screen_y - self.height // 2,
                    self.width,
                    self.height,
                ],
                0,
                10,
            )

            # Add metallic effect with gradient
            highlight_color = (
                min(self.color[0] + 40, 255),
                min(self.color[1] + 40, 255),
                min(self.color[2] + 40, 255),
            )
            pygame.draw.rect(
                screen,
                highlight_color,
                [
                    self.x - self.width // 2,
                    screen_y - self.height // 2,
                    self.width // 2,
                    self.height,
                ],
                0,
                10,
            )

            # Windshield
            windshield_width = int(self.width * 0.8)
            windshield_height = int(self.height * 0.3)
            windshield_x = self.x - windshield_width // 2
            windshield_y = screen_y - self.height // 2 + int(self.height * 0.15)
            pygame.draw.rect(
                screen,
                (100, 200, 255),
                [windshield_x, windshield_y, windshield_width, windshield_height],
                0,
                5,
            )

            # Roof
            roof_width = int(self.width * 0.8)
            roof_height = int(self.height * 0.2)
            roof_x = self.x - roof_width // 2
            roof_y = screen_y - self.height // 2 + int(self.height * 0.15) + windshield_height
            pygame.draw.rect(
                screen, self.color, [roof_x, roof_y, roof_width, roof_height], 0, 5
            )

            # Wheels
            wheel_width = int(self.width * 0.25)
            wheel_height = int(self.height * 0.15)

            # Front left wheel
            pygame.draw.rect(
                screen,
                (15, 15, 15),  # MATTE_BLACK
                [
                    self.x - self.width // 2 - 3,
                    screen_y - self.height // 4,
                    wheel_width,
                    wheel_height,
                ],
                0,
                3,
            )

            # Front right wheel
            pygame.draw.rect(
                screen,
                (15, 15, 15),  # MATTE_BLACK
                [
                    self.x + self.width // 2 - wheel_width + 3,
                    screen_y - self.height // 4,
                    wheel_width,
                    wheel_height,
                ],
                0,
                3,
            )

            # Rear left wheel
            pygame.draw.rect(
                screen,
                (15, 15, 15),  # MATTE_BLACK
                [
                    self.x - self.width // 2 - 3,
                    screen_y + self.height // 4 - wheel_height,
                    wheel_width,
                    wheel_height,
                ],
                0,
                3,
            )

            # Rear right wheel
            pygame.draw.rect(
                screen,
                (15, 15, 15),  # MATTE_BLACK
                [
                    self.x + self.width // 2 - wheel_width + 3,
                    screen_y + self.height // 4 - wheel_height,
                    wheel_width,
                    wheel_height,
                ],
                0,
                3,
            )
            
            # Draw name above car
            name_font = pygame.font.SysFont("arial", 16)
            name_text = name_font.render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.x, screen_y - self.height // 2 - 15))
            screen.blit(name_text, name_rect)
    
    def update(self, dt, player_lane, obstacles, race_length):
        # Update lane change cooldown
        if self.lane_change_cooldown > 0:
            self.lane_change_cooldown -= dt
        
        # Update position based on speed
        self.position += self.speed * dt * 10  # 10 meters per unit of speed
        
        # Check if finished
        if self.position >= race_length and not self.finished:
            self.finished = True
            self.finish_time = time.time()
        
        # AI decision making - only if not finished
        if not self.finished and self.lane_change_cooldown <= 0:
            # Check for obstacles in current lane
            obstacle_ahead = False
            
            # First check for static obstacles
            for obstacle in obstacles:
                if not hasattr(obstacle, 'is_car') and obstacle.lane == self.lane:
                    obstacle_ahead = True
                    break
                    
            # Then check for other cars
            car_ahead = False
            for other in obstacles:
                if (hasattr(other, 'is_car') and 
                    other != self and  # Don't detect self
                    other.lane == self.lane):
                    car_ahead = True
                    break
            
            # Decide whether to change lanes
            if obstacle_ahead or car_ahead:
                # Find a safe lane to move to
                safe_lanes = []
                for l in range(6):  # 6 lanes
                    if l != self.lane:
                        lane_safe = True
                        
                        # Check for obstacles in the potential lane
                        for obstacle in obstacles:
                            if not hasattr(obstacle, 'is_car') and obstacle.lane == l:
                                lane_safe = False
                                break
                                
                        # Check for other cars in the potential lane
                        for other in obstacles:
                            if (hasattr(other, 'is_car') and 
                                other != self and  # Don't detect self
                                other.lane == l):
                                lane_safe = False
                                break
                                
                        if lane_safe:
                            safe_lanes.append(l)
                
                if safe_lanes:
                    self.target_lane = random.choice(safe_lanes)
                    self.lane_change_cooldown = random.uniform(1.0, 3.0)
            
            # Occasionally try to block the player (based on difficulty)
            elif random.random() < 0.02 * self.difficulty and abs(self.lane - player_lane) <= 1:
                self.target_lane = player_lane
                self.lane_change_cooldown = random.uniform(1.0, 3.0)
            
            # Occasionally change lanes randomly
            elif random.random() < 0.01:
                new_lane = random.randint(0, 5)  # 6 lanes
                if new_lane != self.lane:
                    self.target_lane = new_lane
                    self.lane_change_cooldown = random.uniform(1.0, 3.0)
        
        # Move towards target lane
        if self.lane != self.target_lane:
            if self.target_lane > self.lane:
                self.lane += 1
            else:
                self.lane -= 1
            self.x = self.lane_positions[self.lane]
        
        # Adjust speed randomly (based on difficulty)
        if random.random() < 0.05:
            # Higher difficulty means more consistent speed
            variation = 0.2 - (self.difficulty * 0.02)  # 0.1 to 0.18
            self.speed *= random.uniform(1 - variation, 1 + variation)
            
            # Ensure speed stays within reasonable bounds
            min_speed = 5 * 0.7
            max_speed = 5 * (1.0 + self.difficulty * 0.15)
            self.speed = max(min_speed, min(self.speed, max_speed))

class RaceManager:
    """Manages the race mode gameplay"""
    def __init__(self, screen_width, screen_height, lane_positions, car_width, car_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lane_positions = lane_positions
        self.car_width = car_width
        self.car_height = car_height
        self.race_length = 5000  # 5000 meters (5km) race by default
        self.opponents = []
        self.start_time = 0
        self.race_started = False
        self.race_finished = False
        self.player_position = 0
        self.player_finished = False
        self.player_finish_time = 0
        self.countdown_timer = 3  # 3 second countdown
        self.results = []
        
    def initialize_race(self, player_lane):
        """Set up a new race with opponents"""
        self.opponents = []
        
        # Create 5 opponents in different lanes
        available_lanes = list(range(6))  # 6 lanes
        available_lanes.remove(player_lane)  # Remove player's lane
        
        for i in range(5):
            if available_lanes:
                lane = random.choice(available_lanes)
                available_lanes.remove(lane)
            else:
                # If we run out of unique lanes, pick any lane except player's
                lane = random.randint(0, 5)
                while lane == player_lane:
                    lane = random.randint(0, 5)
            
            # Create opponent with varying difficulty
            difficulty = random.randint(1, 5)
            opponent = RaceOpponent(
                lane=lane,
                position=0,
                difficulty=difficulty,
                lane_positions=self.lane_positions,
                car_width=self.car_width,
                car_height=self.car_height
            )
            opponent.name = f"Racer {i+1}"
            self.opponents.append(opponent)
        
        self.start_time = time.time()
        self.race_started = False
        self.race_finished = False
        self.player_position = 0
        self.player_finished = False
        self.player_finish_time = 0
        self.countdown_timer = 3
        self.results = []
    
    def update(self, dt, player_lane, player_position, obstacles):
        """Update race state"""
        # Update countdown
        if not self.race_started:
            self.countdown_timer -= dt
            if self.countdown_timer <= 0:
                self.race_started = True
                self.start_time = time.time()
            return
        
        # Store player position
        self.player_position = player_position
        
        # Check if player finished
        if player_position >= self.race_length and not self.player_finished:
            self.player_finished = True
            self.player_finish_time = time.time() - self.start_time
            self.results.append({
                "name": "Player",
                "time": self.player_finish_time,
                "position": len(self.results) + 1
            })
        
        # Update opponents
        for opponent in self.opponents:
            opponent.update(dt, player_lane, obstacles + self.opponents, self.race_length)
            
            # Check if opponent finished
            if opponent.finished and opponent not in [r.get("opponent") for r in self.results if "opponent" in r]:
                finish_time = opponent.finish_time - self.start_time
                self.results.append({
                    "name": opponent.name,
                    "time": finish_time,
                    "position": len(self.results) + 1,
                    "opponent": opponent  # Store reference to opponent
                })
        
        # Sort results by finish time
        self.results.sort(key=lambda x: x["time"])
        
        # Update positions based on sorted results
        for i, result in enumerate(self.results):
            result["position"] = i + 1
        
        # Check if race is finished (player and all opponents have finished)
        if self.player_finished and all(opponent.finished for opponent in self.opponents):
            self.race_finished = True
    
    def draw(self, screen, player_position):
        """Draw race elements"""
        # Draw finish line if it's within view
        finish_line_relative_pos = self.race_length - player_position
        if -50 < finish_line_relative_pos < self.screen_height:
            finish_y = self.screen_height - 150 - finish_line_relative_pos
            
            # Draw checkered pattern
            square_size = 20
            for i in range(self.screen_width // square_size):
                for j in range(2):  # 2 rows of checkered pattern
                    if (i + j) % 2 == 0:
                        pygame.draw.rect(
                            screen,
                            (255, 255, 255),  # White
                            [i * square_size, finish_y + j * square_size, square_size, square_size]
                        )
                    else:
                        pygame.draw.rect(
                            screen,
                            (0, 0, 0),  # Black
                            [i * square_size, finish_y + j * square_size, square_size, square_size]
                        )
        
        # Draw distance markers every 1000m
        for marker in range(1000, self.race_length, 1000):
            marker_relative_pos = marker - player_position
            if -50 < marker_relative_pos < self.screen_height:
                marker_y = self.screen_height - 150 - marker_relative_pos
                
                # Draw line across road
                pygame.draw.line(
                    screen,
                    (255, 255, 255),  # White
                    (0, marker_y),
                    (self.screen_width, marker_y),
                    2
                )
                
                # Draw distance text
                font = pygame.font.SysFont("arial", 24)
                text = font.render(f"{marker}m", True, (255, 255, 255))
                screen.blit(text, (self.screen_width - 80, marker_y - 15))
        
        # Draw opponents
        for opponent in self.opponents:
            opponent.draw(screen, player_position, self.screen_height)
        
        # Draw countdown if race not started
        if not self.race_started:
            font = pygame.font.SysFont("arial", 72, bold=True)
            if self.countdown_timer > 0:
                text = font.render(str(int(self.countdown_timer) + 1), True, (255, 0, 0))
            else:
                text = font.render("GO!", True, (0, 255, 0))
            
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text, text_rect)
        
        # Draw race progress
        self.draw_race_progress(screen)
        
        # Draw results if race is finished
        if self.race_finished:
            self.draw_results(screen)
    
    def draw_race_progress(self, screen):
        """Draw race progress UI"""
        # Draw progress bar at top of screen
        bar_width = self.screen_width - 100
        bar_height = 20
        bar_x = 50
        bar_y = 30
        
        # Background bar
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            [bar_x, bar_y, bar_width, bar_height],
            0,
            5
        )
        
        # Calculate progress percentages
        player_progress = min(1.0, self.player_position / self.race_length)
        player_width = int(bar_width * player_progress)
        
        # Draw player progress
        pygame.draw.rect(
            screen,
            (0, 255, 0),  # Green for player
            [bar_x, bar_y, player_width, bar_height],
            0,
            5
        )
        
        # Draw opponent progress markers
        for opponent in self.opponents:
            opponent_progress = min(1.0, opponent.position / self.race_length)
            opponent_x = bar_x + int(bar_width * opponent_progress)
            
            # Draw a triangle marker
            pygame.draw.polygon(
                screen,
                opponent.color,
                [
                    (opponent_x, bar_y - 5),
                    (opponent_x - 5, bar_y - 15),
                    (opponent_x + 5, bar_y - 15)
                ]
            )
        
        # Draw player position and remaining distance
        font = pygame.font.SysFont("arial", 18)
        position_text = font.render(f"Position: {self.get_player_position()}/{len(self.opponents) + 1}", True, (255, 255, 255))
        screen.blit(position_text, (bar_x, bar_y + bar_height + 5))
        
        distance_text = font.render(f"Distance: {int(self.player_position)}m / {self.race_length}m", True, (255, 255, 255))
        screen.blit(distance_text, (bar_x + bar_width - 200, bar_y + bar_height + 5))
        
        # Draw elapsed time
        if self.race_started:
            if self.player_finished:
                elapsed = self.player_finish_time
            else:
                elapsed = time.time() - self.start_time
            
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            hundredths = int((elapsed % 1) * 100)
            
            time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}.{hundredths:02d}", True, (255, 255, 255))
            screen.blit(time_text, (self.screen_width - 150, bar_y))
    
    def draw_results(self, screen):
        """Draw race results when finished"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Draw results box
        box_width = 400
        box_height = 300
        box_x = (self.screen_width - box_width) // 2
        box_y = (self.screen_height - box_height) // 2
        
        pygame.draw.rect(
            screen,
            (50, 50, 80),
            [box_x, box_y, box_width, box_height],
            0,
            10
        )
        
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            [box_x, box_y, box_width, box_height],
            2,
            10
        )
        
        # Draw title
        title_font = pygame.font.SysFont("arial", 36, bold=True)
        title_text = title_font.render("RACE RESULTS", True, (255, 255, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, box_y + 30))
        screen.blit(title_text, title_rect)
        
        # Draw results
        result_font = pygame.font.SysFont("arial", 24)
        y_pos = box_y + 80
        
        for result in self.results:
            # Highlight player's result
            if result["name"] == "Player":
                color = (0, 255, 0)  # Green for player
            else:
                color = (255, 255, 255)  # White for opponents
            
            # Format time
            minutes = int(result["time"] // 60)
            seconds = int(result["time"] % 60)
            hundredths = int((result["time"] % 1) * 100)
            time_str = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"
            
            # Draw position
            pos_text = result_font.render(f"{result['position']}.", True, color)
            screen.blit(pos_text, (box_x + 30, y_pos))
            
            # Draw name
            name_text = result_font.render(result["name"], True, color)
            screen.blit(name_text, (box_x + 60, y_pos))
            
            # Draw time
            time_text = result_font.render(time_str, True, color)
            screen.blit(time_text, (box_x + box_width - 150, y_pos))
            
            y_pos += 30
        
        # Draw continue prompt
        prompt_font = pygame.font.SysFont("arial", 18)
        prompt_text = prompt_font.render("Press ENTER to continue", True, (200, 200, 200))
        prompt_rect = prompt_text.get_rect(center=(self.screen_width // 2, box_y + box_height - 30))
        screen.blit(prompt_text, prompt_rect)
    
    def get_player_position(self):
        """Get player's current race position (1st, 2nd, etc.)"""
        # Count how many opponents are ahead of player
        ahead_count = sum(1 for opponent in self.opponents if opponent.position > self.player_position)
        return ahead_count + 1  # Add 1 because positions start at 1, not 0
    
    def get_race_score(self):
        """Calculate score based on race performance"""
        if not self.player_finished:
            return 0
        
        # Base score depends on position
        position = next((r["position"] for r in self.results if r["name"] == "Player"), 0)
        if position == 0:
            return 0
            
        position_scores = {
            1: 1000,  # 1st place
            2: 750,   # 2nd place
            3: 500,   # 3rd place
            4: 300,   # 4th place
            5: 200,   # 5th place
            6: 100    # 6th place
        }
        
        base_score = position_scores.get(position, 50)
        
        # Bonus for finishing quickly
        time_bonus = max(0, 500 - int(self.player_finish_time * 10))
        
        return base_score + time_bonus
