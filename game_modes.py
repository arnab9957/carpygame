# Game modes implementation file
import pygame
import random
import time
import math
from race_mode import RaceManager

# Import this file in the main game to use these functions

def setup_race_mode(game):
    """Set up the race mode for the game"""
    # Initialize race manager if it doesn't exist
    if not hasattr(game, "race_manager"):
        game.race_manager = RaceManager(
            screen_width=game.screen.get_width(),
            screen_height=game.screen.get_height(),
            lane_positions=game.LANE_POSITIONS,
            car_width=game.CAR_WIDTH,
            car_height=game.CAR_HEIGHT
        )
    
    # Initialize a new race
    game.race_manager.initialize_race(game.player_car.lane)
    
    # Set race-specific game properties
    game.race_length = game.race_manager.race_length
    game.race_started = False
    game.race_finished = False
    
    # Clear obstacles for race start
    game.obstacles = []
    game.other_cars = []
    
    # Reset player position
    game.player_car.position = 0
    
    # Show race start prompt
    if hasattr(game, "prompt_system"):
        game.prompt_system.show_custom_prompt("Race Mode: Be the first to reach the finish line!", 3.0)

def update_race_mode(game, dt):
    """Update race mode logic"""
    # Update race manager
    obstacles = game.obstacles + game.other_cars
    game.race_manager.update(
        dt=dt,
        player_lane=game.player_car.lane,
        player_position=game.distance_traveled,
        obstacles=obstacles
    )
    
    # Check if race is finished
    if game.race_manager.race_finished and not game.game_over:
        # Calculate score based on race results
        race_score = game.race_manager.get_race_score()
        game.score += race_score
        
        # Mark game as over but don't show crash animation
        game.game_over = True
        game.game_has_been_played = True
    
    # Generate fewer obstacles in race mode
    current_time = time.time()
    
    # Only generate obstacles if race has started
    if game.race_manager.race_started:
        # Generate obstacles less frequently in race mode
        if current_time - game.last_obstacle_time > random.uniform(5.0, 10.0):
            # Limit number of obstacles
            if len(game.obstacles) < 2:
                # Choose a lane that doesn't have an opponent or obstacle
                available_lanes = list(range(6))
                
                # Remove lanes with obstacles
                for obstacle in game.obstacles:
                    if obstacle.lane in available_lanes:
                        available_lanes.remove(obstacle.lane)
                
                # Remove lanes with opponents
                for opponent in game.race_manager.opponents:
                    if opponent.lane in available_lanes:
                        available_lanes.remove(opponent.lane)
                
                # Remove player's lane
                if game.player_car.lane in available_lanes:
                    available_lanes.remove(game.player_car.lane)
                
                # If there are available lanes, create an obstacle
                if available_lanes:
                    lane = random.choice(available_lanes)
                    game.obstacles.append(game.Obstacle(lane))
                    game.last_obstacle_time = current_time

def draw_race_mode(game):
    """Draw race mode specific elements"""
    # Draw race elements (finish line, opponents, etc.)
    game.race_manager.draw(game.screen, game.distance_traveled)
    
    # Draw race-specific UI elements
    if not game.race_manager.race_finished:
        # Draw race progress at top of screen
        font = game.font_small
        
        # Draw position
        position = game.race_manager.get_player_position()
        position_text = font.render(f"Position: {position}/6", True, (255, 255, 255))
        game.screen.blit(position_text, (10, 90))
        
        # Draw distance to finish
        remaining = game.race_length - game.distance_traveled
        if remaining > 0:
            distance_text = font.render(f"Remaining: {int(remaining)}m", True, (255, 255, 255))
            game.screen.blit(distance_text, (10, 120))

def handle_race_input(game, event):
    """Handle race mode specific input"""
    # Handle input for race results screen
    if game.race_manager.race_finished and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            # End the race and return to menu
            game.game_over = True
            return True
    return False
