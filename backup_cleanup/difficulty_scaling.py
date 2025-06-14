#!/usr/bin/env python3
"""
Difficulty Scaling Module for Car Racing Game
Implements gradual traffic speed/density increase and complex obstacle patterns
"""
import random
import math
import time
from typing import List, Dict, Any, Tuple, Optional

class DifficultyManager:
    """
    Manages game difficulty scaling based on time played, distance traveled, or score
    """
    
    def __init__(self):
        # Base difficulty settings
        self.base_settings = {
            'obstacle_spawn_interval': 5.0,  # seconds between obstacle spawns
            'car_spawn_interval': 6.0,      # seconds between car spawns
            'max_obstacles': 3,             # maximum obstacles on screen
            'max_cars': 3,                  # maximum cars on screen
            'obstacle_speed_multiplier': 1.0,  # multiplier for obstacle speed
            'pattern_complexity': 0,        # 0=simple, 1=medium, 2=complex
            'aggressive_ai_chance': 0.2,    # chance of spawning aggressive AI
            'speed_increment': 0.005        # base speed increment per frame
        }
        
        # Current difficulty settings (will be modified as game progresses)
        self.current_settings = self.base_settings.copy()
        
        # Difficulty progression thresholds
        self.distance_thresholds = [500, 1000, 2000, 3500, 5000, 7500, 10000]
        self.time_thresholds = [30, 60, 120, 180, 300, 480, 600]  # in seconds
        self.score_thresholds = [100, 250, 500, 1000, 2000, 3500, 5000]
        
        # Track game progress
        self.start_time = time.time()
        self.current_level = 0
        self.max_level = len(self.distance_thresholds)
        
        # Pattern definitions
        self.obstacle_patterns = self._initialize_patterns()
        self.current_pattern = None
        self.pattern_progress = 0
        
        # Notification system
        self.difficulty_increased = False
        self.notification_time = 0
        self.notification_duration = 3.0  # seconds
    
    def _initialize_patterns(self) -> Dict[int, List[Dict]]:
        """Initialize obstacle patterns of varying complexity"""
        patterns = {
            # Level 0 (Simple): Single obstacles in random lanes
            0: [
                {'type': 'single', 'description': 'Single obstacle in random lane'},
                {'type': 'gap', 'description': 'Single gap with obstacles on both sides'}
            ],
            
            # Level 1 (Medium): Basic patterns
            1: [
                {'type': 'zigzag', 'description': 'Zigzag pattern of obstacles'},
                {'type': 'double', 'description': 'Two adjacent obstacles'},
                {'type': 'gap', 'description': 'Single gap with obstacles on both sides'},
                {'type': 'alternating', 'description': 'Alternating obstacles in lanes'}
            ],
            
            # Level 2 (Complex): Advanced patterns
            2: [
                {'type': 'wall', 'description': 'Wall with single gap', 'gap_size': 1},
                {'type': 'zigzag', 'description': 'Complex zigzag pattern'},
                {'type': 'double_gap', 'description': 'Two gaps with obstacles elsewhere'},
                {'type': 'moving_wall', 'description': 'Wall with moving obstacles'},
                {'type': 'funnel', 'description': 'Funnel pattern forcing specific lane'}
            ],
            
            # Level 3 (Hard): Challenging patterns
            3: [
                {'type': 'wall', 'description': 'Wall with single gap', 'gap_size': 1},
                {'type': 'maze', 'description': 'Maze-like pattern requiring specific path'},
                {'type': 'moving_zigzag', 'description': 'Zigzag with moving obstacles'},
                {'type': 'narrow_corridor', 'description': 'Long narrow corridor'},
                {'type': 'wave', 'description': 'Wave pattern requiring timing'}
            ]
        }
        return patterns
    
    def update(self, distance: float, score: int, dt: float) -> None:
        """
        Update difficulty based on game progress
        
        Args:
            distance: Distance traveled in game
            score: Current score
            dt: Delta time since last update
        """
        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        
        # Check if we should increase difficulty level
        new_level = self.current_level
        
        # Check distance threshold
        for i, threshold in enumerate(self.distance_thresholds):
            if distance > threshold and i >= self.current_level:
                new_level = i + 1
                
        # Check time threshold as backup
        for i, threshold in enumerate(self.time_thresholds):
            if elapsed_time > threshold and i >= self.current_level:
                new_level = max(new_level, i + 1)
                
        # Check score threshold as another factor
        for i, threshold in enumerate(self.score_thresholds):
            if score > threshold and i >= self.current_level:
                new_level = max(new_level, i + 1)
        
        # Cap at max level
        new_level = min(new_level, self.max_level)
        
        # If level increased, update settings
        if new_level > self.current_level:
            self.current_level = new_level
            self._update_difficulty_settings()
            self.difficulty_increased = True
            self.notification_time = time.time()
        
        # Update notification status
        if self.difficulty_increased and time.time() - self.notification_time > self.notification_duration:
            self.difficulty_increased = False
    
    def _update_difficulty_settings(self) -> None:
        """Update game settings based on current difficulty level"""
        level_factor = self.current_level / self.max_level
        
        # Gradually decrease spawn intervals (more frequent spawns)
        self.current_settings['obstacle_spawn_interval'] = max(
            1.5,  # Minimum spawn interval
            self.base_settings['obstacle_spawn_interval'] * (1.0 - level_factor * 0.7)
        )
        
        self.current_settings['car_spawn_interval'] = max(
            2.0,  # Minimum spawn interval
            self.base_settings['car_spawn_interval'] * (1.0 - level_factor * 0.6)
        )
        
        # Increase maximum number of obstacles and cars
        self.current_settings['max_obstacles'] = min(
            6,  # Maximum obstacles
            int(self.base_settings['max_obstacles'] + level_factor * 3)
        )
        
        self.current_settings['max_cars'] = min(
            5,  # Maximum cars
            int(self.base_settings['max_cars'] + level_factor * 2)
        )
        
        # Increase obstacle speed
        self.current_settings['obstacle_speed_multiplier'] = (
            self.base_settings['obstacle_speed_multiplier'] + level_factor * 0.5
        )
        
        # Increase pattern complexity
        self.current_settings['pattern_complexity'] = min(
            3,  # Maximum complexity level
            int(level_factor * 3.99)  # Scale from 0 to 3
        )
        
        # Increase aggressive AI chance
        self.current_settings['aggressive_ai_chance'] = min(
            0.7,  # Maximum aggressive chance
            self.base_settings['aggressive_ai_chance'] + level_factor * 0.5
        )
        
        # Increase speed increment
        self.current_settings['speed_increment'] = (
            self.base_settings['speed_increment'] * (1.0 + level_factor * 0.5)
        )
        
        print(f"Difficulty increased to level {self.current_level}/{self.max_level}")
        print(f"New settings: {self.current_settings}")
    
    def get_obstacle_pattern(self, num_lanes: int) -> List[int]:
        """
        Get the next obstacle pattern based on current difficulty
        
        Args:
            num_lanes: Number of lanes in the game
            
        Returns:
            List of lane indices where obstacles should be placed
        """
        complexity = self.current_settings['pattern_complexity']
        
        # Select a pattern from the current complexity level
        available_patterns = self.obstacle_patterns.get(complexity, self.obstacle_patterns[0])
        pattern_info = random.choice(available_patterns)
        pattern_type = pattern_info['type']
        
        # Generate the actual pattern based on type
        if pattern_type == 'single':
            # Single obstacle in a random lane
            lane = random.randint(0, num_lanes - 1)
            return [lane]
            
        elif pattern_type == 'gap':
            # Create a wall with a single gap
            gap_pos = random.randint(0, num_lanes - 1)
            return [i for i in range(num_lanes) if i != gap_pos]
            
        elif pattern_type == 'double':
            # Two adjacent obstacles
            start_lane = random.randint(0, num_lanes - 2)
            return [start_lane, start_lane + 1]
            
        elif pattern_type == 'zigzag':
            # Zigzag pattern
            if complexity <= 1:
                # Simple zigzag
                start_lane = random.randint(0, num_lanes - 3)
                return [start_lane, start_lane + 2]
            else:
                # Complex zigzag
                lanes = []
                lane = random.randint(0, num_lanes - 1)
                for i in range(3):  # 3 obstacles in zigzag
                    lanes.append(lane)
                    lane = (lane + 2) % num_lanes
                return lanes
                
        elif pattern_type == 'wall':
            # Wall with a gap
            gap_size = pattern_info.get('gap_size', 1)
            gap_start = random.randint(0, num_lanes - gap_size)
            return [i for i in range(num_lanes) if i < gap_start or i >= gap_start + gap_size]
            
        elif pattern_type == 'double_gap':
            # Two gaps with obstacles elsewhere
            gaps = random.sample(range(num_lanes), 2)
            return [i for i in range(num_lanes) if i not in gaps]
            
        elif pattern_type == 'funnel':
            # Funnel pattern forcing a specific lane
            target_lane = random.randint(1, num_lanes - 2)
            return [i for i in range(num_lanes) if i != target_lane and i != target_lane - 1]
            
        elif pattern_type == 'maze':
            # Maze-like pattern
            # This is a more complex pattern that changes over time
            # For now, we'll just return a semi-random pattern
            return random.sample(range(num_lanes), num_lanes - 2)
            
        elif pattern_type == 'alternating':
            # Alternating obstacles
            return [i for i in range(0, num_lanes, 2)]
            
        # Default: return a single random obstacle
        return [random.randint(0, num_lanes - 1)]
    
    def should_spawn_aggressive_ai(self) -> bool:
        """Determine if the next AI car should be aggressive"""
        return random.random() < self.current_settings['aggressive_ai_chance']
    
    def get_notification(self) -> Optional[str]:
        """Get difficulty increase notification if available"""
        if self.difficulty_increased:
            return f"Difficulty Increased to Level {self.current_level}!"
        return None
    
    def get_speed_increment(self) -> float:
        """Get the current speed increment value"""
        return self.current_settings['speed_increment']
    
    def get_obstacle_speed_multiplier(self) -> float:
        """Get the current obstacle speed multiplier"""
        return self.current_settings['obstacle_speed_multiplier']
    
    def get_spawn_intervals(self) -> Tuple[float, float]:
        """Get the current spawn intervals for obstacles and cars"""
        return (
            self.current_settings['obstacle_spawn_interval'],
            self.current_settings['car_spawn_interval']
        )
    
    def get_max_objects(self) -> Tuple[int, int]:
        """Get the maximum number of obstacles and cars"""
        return (
            self.current_settings['max_obstacles'],
            self.current_settings['max_cars']
        )
    
    def reset(self) -> None:
        """Reset difficulty to initial state"""
        self.current_settings = self.base_settings.copy()
        self.start_time = time.time()
        self.current_level = 0
        self.difficulty_increased = False
        self.notification_time = 0
        self.current_pattern = None
        self.pattern_progress = 0


# Example of how to integrate this with the main game:
"""
# In the main game class:
from difficulty_scaling import DifficultyManager

class Game:
    def __init__(self):
        # ... existing initialization ...
        self.difficulty_manager = DifficultyManager()
        
    def reset_game(self):
        # ... existing reset code ...
        self.difficulty_manager.reset()
        
    def update(self):
        # ... existing update code ...
        
        # Update difficulty based on game progress
        self.difficulty_manager.update(self.distance_traveled, self.score, dt)
        
        # Use difficulty settings for game mechanics
        max_obstacles, max_cars = self.difficulty_manager.get_max_objects()
        obstacle_interval, car_interval = self.difficulty_manager.get_spawn_intervals()
        
        # Spawn obstacles based on pattern
        if time_to_spawn_obstacle and len(self.obstacles) < max_obstacles:
            pattern = self.difficulty_manager.get_obstacle_pattern(len(LANE_POSITIONS))
            for lane in pattern:
                self.obstacles.append(Obstacle(lane))
        
        # Adjust speed increment
        SPEED_INCREMENT = self.difficulty_manager.get_speed_increment()
        
        # Show notification if difficulty increased
        notification = self.difficulty_manager.get_notification()
        if notification:
            self.prompt_system.show_custom_prompt(notification, duration=3.0)
"""
