#!/usr/bin/env python3
# Performance-optimized version of car_game_advanced_new.py
# Key optimizations:
# - Reduced particle effects
# - Optimized rendering with surface caching
# - Limited game objects
# - Lower target frame rate
# - Simplified collision detection

import pygame
import random
import sys
import time
import math
import json
import os
import traceback
from typing import List, Tuple, Dict, Any, Optional

# Performance settings
TARGET_FPS = 30  # Lower target FPS for better performance
MAX_PARTICLES = 50  # Limit total particles
ENABLE_COMPLEX_EFFECTS = False  # Disable complex visual effects
BACKGROUND_CACHE_ENABLED = True  # Enable background caching

# For smooth transitions
from pygame.locals import *

# Initialize pygame
pygame.init()
try:
    pygame.mixer.init(
        frequency=22050, size=-16, channels=1, buffer=512
    )  # Simplified audio settings
    print("Sound mixer initialized successfully")
    sound_enabled = True
except pygame.error as e:
    print(f"Warning: Sound mixer initialization failed: {e}. Sound will be disabled.")
    sound_enabled = False
else:
    sound_enabled = True
    music_enabled = True

# Set up font system
DEFAULT_FONT = "arial"

# Get the screen info to make the game fit the window
info = pygame.display.Info()
SCREEN_WIDTH = min(info.current_w - 100, 800)  # Reduced max resolution
SCREEN_HEIGHT = min(info.current_h - 100, 600)  # Reduced max resolution

# Define base resolution for scaling calculations
BASE_WIDTH = 800
BASE_HEIGHT = 600

# Scale factor for responsive UI
SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT

# Game constants
STAR_COUNT = 15  # Reduced stars for better performance
LANE_WIDTH = SCREEN_WIDTH // 6
LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
CAR_WIDTH = 50
CAR_HEIGHT = 100
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 40
INITIAL_SPEED = 5
SPEED_INCREMENT = 0.005

# Day-Night cycle settings
DAY_NIGHT_CYCLE_DURATION = 120  # Slower cycle for less frequent updates
DAY_COLOR = (47, 79, 79)
DAY_COLOR_BOTTOM = (0, 128, 128)
NIGHT_COLOR = (5, 5, 25)
NIGHT_COLOR_BOTTOM = (20, 20, 40)
SUNRISE_COLOR = (255, 127, 80)
SUNRISE_COLOR_BOTTOM = (255, 99, 71)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 224)

# Game modes
GAME_MODE_ENDLESS = 0
GAME_MODE_TIME_ATTACK = 1
GAME_MODE_MISSIONS = 2

# Mission types
MISSION_COLLECT_COINS = 0
MISSION_DISTANCE = 1
MISSION_AVOID_CRASHES = 2
MISSION_USE_POWERUPS = 3

def scale_value(value):
    """Scale a value based on screen size"""
    return int(value * min(SCALE_X, SCALE_Y))

def get_font(size, bold=False):
    """Get the appropriate font with the specified size and style"""
    try:
        return pygame.font.SysFont(DEFAULT_FONT, size, bold=bold)
    except Exception as e:
        print(f"Error loading font: {e}")
        return pygame.font.Font(None, size)

def scale_pos_x(x):
    """Scale an x position based on screen width"""
    return int(x * SCALE_X)

def scale_pos_y(y):
    """Scale a y position based on screen height"""
    return int(y * SCALE_Y)

def scale_rect(rect):
    """Scale a rectangle based on screen size"""
    return pygame.Rect(
        scale_pos_x(rect[0]),
        scale_pos_y(rect[1]),
        scale_value(rect[2]),
        scale_value(rect[3]),
    )

# Main game class will be implemented next
