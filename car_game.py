#!/usr/bin/env python3
import pygame
import random
import sys
import time
import math
import json
import os
import traceback
from typing import List, Tuple, Dict, Any, Optional

# Music player has been removed, we'll handle music directly
MusicPlayer = None

# For smooth transitions
from pygame.locals import *

# Initialize pygame
pygame.init()
try:
    pygame.mixer.init(
        frequency=44100, size=-16, channels=2, buffer=512
    )  # More specific initialization
    print("Sound mixer initialized successfully")
    sound_enabled = True
except pygame.error as e:
    print(f"Warning: Sound mixer initialization failed: {e}. Sound will be disabled.")
    sound_enabled = False
else:
    sound_enabled = True
    music_enabled = True

# Set up font system
# Try to load Pixelify Sans font if available, otherwise fall back to default fonts
try:
    # Create fonts directory if it doesn't exist
    if not os.path.exists("fonts"):
        os.makedirs("fonts")
        print("Created fonts directory")
    
    # Define font file paths
    PIXELIFY_SANS_REGULAR = "fonts/PixelifySans-Regular.ttf"
    PIXELIFY_SANS_BOLD = "fonts/PixelifySans-Bold.ttf"
    
    # Check if font files exist, if not, we'll use system fonts
    has_pixelify_font = os.path.exists(PIXELIFY_SANS_REGULAR) and os.path.exists(PIXELIFY_SANS_BOLD)
    
    if not has_pixelify_font:
        print("Pixelify Sans font files not found. Using system fonts instead.")
        # We'll use system fonts with fallback to default pygame fonts
        DEFAULT_FONT = "arial"
    else:
        print("Pixelify Sans font files found and will be used.")
except Exception as e:
    print(f"Error setting up font system: {e}")
    DEFAULT_FONT = "arial"

# Get the screen info to make the game fit the window
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w  # Use full screen width
SCREEN_HEIGHT = info.current_h  # Use full screen height

# Define base resolution for scaling calculations
BASE_WIDTH = 1280
BASE_HEIGHT = 720

# Scale factor for responsive UI
SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT

# Game constants
STAR_COUNT = 5  # Reduced for performance  # Reduced for performance


def scale_value(value):
    """Scale a value based on screen size"""
    return int(value * min(SCALE_X, SCALE_Y))


def get_font(size, bold=False):
    """Get the appropriate font with the specified size and style"""
    try:
        if 'has_pixelify_font' in globals() and has_pixelify_font:
            if bold:
                return pygame.font.Font(PIXELIFY_SANS_BOLD, size)
            else:
                return pygame.font.Font(PIXELIFY_SANS_REGULAR, size)
        else:
            # Fall back to system font
            return pygame.font.SysFont(DEFAULT_FONT, size, bold=bold)
    except Exception as e:
        print(f"Error loading font: {e}")
        # Ultimate fallback to default pygame font
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


# Sound effects
# Sound settings
sound_enabled = False
music_enabled = False

try:
    # Create a sounds directory if it doesn't exist
    if not os.path.exists("sounds"):
        os.makedirs("sounds")
        print("Created sounds directory")

    # Define sound file paths
    SOUND_ENGINE = "sounds/engine.wav"
    SOUND_CRASH = "sounds/crash.wav"
    SOUND_POWERUP = "sounds/powerup.wav"
    SOUND_COIN = "sounds/coin.wav"
    SOUND_MENU_SELECT = "sounds/menu_select.wav"
    SOUND_MENU_NAVIGATE = "sounds/menu_navigate.wav"
    SOUND_BOOST = "sounds/boost.wav"
    SOUND_SHIELD = "sounds/shield.wav"
    SOUND_GAME_OVER = "sounds/game_over.wav"
    SOUND_BACKGROUND_MUSIC = "sounds/background_music.mp3"
    SOUND_MENU_MUSIC = "sounds/main_menu.wav"  # New menu music file

    # Create placeholder sound files if they don't exist
    def create_placeholder_sound(filename, duration=1.0, freq=440):
        if not os.path.exists(filename):
            print(f"Creating placeholder sound: {filename}")
            import wave
            import struct
            import math

            # Create a simple sine wave as placeholder
            sample_rate = 44100
            amplitude = 4096
            num_samples = int(duration * sample_rate)

            with wave.open(filename, "w") as wav_file:
                wav_file.setparams(
                    (1, 2, sample_rate, num_samples, "NONE", "not compressed")
                )

                for i in range(num_samples):
                    sample = amplitude * math.sin(2 * math.pi * freq * i / sample_rate)
                    packed_sample = struct.pack("h", int(sample))
                    wav_file.writeframes(packed_sample)

    # Create placeholder sounds with different frequencies for distinction
    create_placeholder_sound(SOUND_ENGINE, duration=2.0, freq=200)
    create_placeholder_sound(SOUND_CRASH, duration=0.5, freq=100)
    create_placeholder_sound(SOUND_POWERUP, duration=0.3, freq=800)
    create_placeholder_sound(SOUND_COIN, duration=0.2, freq=1000)
    create_placeholder_sound(SOUND_MENU_SELECT, duration=0.2, freq=600)
    create_placeholder_sound(SOUND_MENU_NAVIGATE, duration=0.1, freq=500)
    create_placeholder_sound(SOUND_BOOST, duration=0.4, freq=300)
    create_placeholder_sound(SOUND_SHIELD, duration=0.3, freq=700)
    create_placeholder_sound(SOUND_GAME_OVER, duration=1.0, freq=150)

    # For background music, create a longer placeholder
    if not os.path.exists(SOUND_BACKGROUND_MUSIC):
        print(f"Creating placeholder music: {SOUND_BACKGROUND_MUSIC}")
        # Create a simple text file as placeholder since MP3 creation is complex
        with open(SOUND_BACKGROUND_MUSIC, "w") as f:
            f.write("Placeholder for background music")

    # For menu music, create a placeholder
    if not os.path.exists(SOUND_MENU_MUSIC):
        print(f"Creating placeholder menu music: {SOUND_MENU_MUSIC}")
        # Create a simple text file as placeholder since MP3 creation is complex
        with open(SOUND_MENU_MUSIC, "w") as f:
            f.write("Placeholder for chill synth racing menu music")

    # Check if pygame mixer is initialized
    if pygame.mixer.get_init():
        # Load sounds
        sound_engine = pygame.mixer.Sound(SOUND_ENGINE)
        sound_crash = pygame.mixer.Sound(SOUND_CRASH)
        sound_powerup = pygame.mixer.Sound(SOUND_POWERUP)
        sound_coin = pygame.mixer.Sound(SOUND_COIN)
        sound_menu_select = pygame.mixer.Sound(SOUND_MENU_SELECT)
        sound_menu_navigate = pygame.mixer.Sound(SOUND_MENU_NAVIGATE)
        sound_boost = pygame.mixer.Sound(SOUND_BOOST)
        sound_shield = pygame.mixer.Sound(SOUND_SHIELD)
        sound_game_over = pygame.mixer.Sound(SOUND_GAME_OVER)

        # Set volume levels
        sound_engine.set_volume(0.3)
        sound_crash.set_volume(0.7)
        sound_powerup.set_volume(0.5)
        sound_coin.set_volume(0.4)
        sound_menu_select.set_volume(0.5)
        sound_menu_navigate.set_volume(0.3)
        sound_boost.set_volume(0.6)
        sound_shield.set_volume(0.5)
        sound_game_over.set_volume(0.7)

        # Sound settings
        sound_enabled = True
        music_enabled = True
    else:
        print("Sound mixer not initialized, sounds will be disabled")
        sound_enabled = False
        music_enabled = False

except Exception as e:
    print(f"Error initializing sounds: {e}")
    sound_enabled = False
    music_enabled = False

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

# Prompt system colors
PROMPT_BG = (0, 0, 0, 180)  # Semi-transparent black
PROMPT_BORDER = (255, 255, 0)  # Yellow border
PROMPT_TEXT = (255, 255, 255)  # White text
PROMPT_HIGHLIGHT = (255, 165, 0)  # Orange highlight

# Menu color palette
DEEP_BLUE = (26, 35, 126)  # #1A237E - Primary background
NEON_YELLOW = (255, 255, 0)  # #FFFF00 - Buttons and highlights
SLEEK_SILVER = (204, 204, 204)  # #CCCCCC - UI elements and borders
BRIGHT_RED = (255, 62, 65)  # #FF3E41 - Call-to-action buttons

# Animation settings
TRANSITION_SPEED = 0.8  # seconds for a full transition
FADE_SPEED = 0.5  # seconds for a full fade
SLIDE_DISTANCE = 300  # pixels to slide during transitions

# Gameplay color palette
DARK_SLATE = (47, 79, 79)  # #2F4F4F - Top of gradient
TEAL = (0, 128, 128)  # #008080 - Bottom of gradient
MATTE_BLACK = (15, 15, 15)  # #0F0F0F - Car bodies
METALLIC_SILVER = (192, 192, 192)  # #C0C0C0 - UI overlays
ELECTRIC_PURPLE = (191, 64, 191)  # #BF40BF - Speed indicators
NEON_GREEN = (80, 200, 120)  # #50C878 - Boost effects

# Power-up colors
BOOST_COLOR = (255, 140, 0)  # Orange for speed boost
SHIELD_COLOR = (30, 144, 255)  # Dodger blue for shield
MAGNET_COLOR = (255, 215, 0)  # Gold for coin magnet
COIN_COLOR = (255, 223, 0)  # Gold for coins
SLOW_MO_COLOR = (138, 43, 226)  # Purple for slow motion

# Game settings
LANE_WIDTH = SCREEN_WIDTH // 8  # Changed to 8 lanes
LANE_POSITIONS = [
    LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(8)
]  # Now 8 lane positions
CAR_WIDTH = 60
CAR_HEIGHT = 120
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
INITIAL_SPEED = 5
SPEED_INCREMENT = 0.005  # Smoother acceleration

# Day-Night cycle settings
DAY_NIGHT_CYCLE_DURATION = 60  # seconds for a full cycle
DAY_COLOR = (47, 79, 79)  # DARK_SLATE for day sky top
DAY_COLOR_BOTTOM = (0, 128, 128)  # TEAL for day sky bottom
NIGHT_COLOR = (5, 5, 25)  # Dark blue for night sky top
NIGHT_COLOR_BOTTOM = (20, 20, 40)  # Slightly lighter blue for night sky bottom
SUNRISE_COLOR = (255, 127, 80)  # Coral for sunrise/sunset top
SUNRISE_COLOR_BOTTOM = (255, 99, 71)  # Tomato for sunrise/sunset bottom
STAR_COUNT = 5  # Reduced for performance  # Reduced for performance

# Power-up settings
POWERUP_WIDTH = 40
POWERUP_HEIGHT = 40
POWERUP_DURATION = 5  # seconds
BOOST_MULTIPLIER = 1.8  # Increased from 1.5 to 1.8 for more noticeable boost
SHIELD_DURATION = 7  # seconds
MAGNET_RANGE = 150  # pixels
SLOW_MO_FACTOR = 0.5  # 50% slower
COIN_VALUE = 10  # points

# Game modes
GAME_MODE_ENDLESS = 0
GAME_MODE_TIME_ATTACK = 1
GAME_MODE_MISSIONS = 2
GAME_MODE_RACE = 3  # New Race Mode

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
GAME_MODE_MISSIONS = 2

# Mission types
MISSION_COLLECT_COINS = 0
MISSION_DISTANCE = 1
MISSION_AVOID_CRASHES = 2
MISSION_USE_POWERUPS = 3


class HighScoreManager:
    def __init__(self, filename="highscores.json"):
        self.filename = filename
        self.highscores = {"endless": [], "time_attack": [], "missions": [], "race": []}
        self.load_highscores()

    def load_highscores(self):
        """Load high scores from file if it exists"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as f:
                    self.highscores = json.load(f)
                # Ensure all required keys exist
                for key in ["endless", "time_attack", "missions", "race"]:
                    if key not in self.highscores:
                        self.highscores[key] = []
        except Exception as e:
            print(f"Error loading high scores: {e}")
            # If there's an error, we'll use the default empty high scores
            self.highscores = {"endless": [], "time_attack": [], "missions": [], "race": []}

    def save_highscores(self):
        """Save high scores to file"""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.highscores, f)
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def add_score(self, game_mode, player_name, score, distance=0, coins=0):
        """Add a new score to the appropriate game mode list only if it's higher than the current maximum"""
        mode_key = self._get_mode_key(game_mode)

        # Check if this is a new high score
        current_scores = self.highscores[mode_key]

        # If there are no scores yet, or if this score is higher than the highest score
        if not current_scores or score > max(
            [s["score"] for s in current_scores], default=0
        ):
            print(f"New highest score: {score}!")

            # Create score entry with timestamp
            score_entry = {
                "name": player_name,
                "score": score,
                "distance": distance,
                "coins": coins,
                "date": time.strftime("%Y-%m-%d %H:%M"),
            }

            # Add to appropriate list
            self.highscores[mode_key].append(score_entry)

            # Sort by score (descending)
            self.highscores[mode_key].sort(key=lambda x: x["score"], reverse=True)

            # Keep only top 10 scores
            self.highscores[mode_key] = self.highscores[mode_key][:10]

            # Save to file
            self.save_highscores()
            return True
        else:
            print(f"Score {score} is not higher than the current highest score.")
            return False

    def get_highscores(self, game_mode):
        """Get high scores for the specified game mode"""
        mode_key = self._get_mode_key(game_mode)
        return self.highscores[mode_key]

    def is_high_score(self, game_mode, score):
        """Check if the score qualifies as a high score (only if it's the highest)"""
        mode_key = self._get_mode_key(game_mode)
        scores = self.highscores[mode_key]

        # If there are no scores yet, it's automatically a high score
        if not scores:
            return True

        # Otherwise, check if it's higher than the highest score
        return score > max([s["score"] for s in scores])

    def _get_mode_key(self, game_mode):
        """Convert game mode constant to string key"""
        if game_mode == GAME_MODE_ENDLESS:
            return "endless"
        elif game_mode == GAME_MODE_TIME_ATTACK:
            return "time_attack"
        elif game_mode == GAME_MODE_RACE:
            return "race"
        elif game_mode == GAME_MODE_MISSIONS:
            return "missions"
        else:
            return "endless"  # Default

    def delete_score(self, game_mode, index):
        """Delete a score at the specified index from the high scores list"""
        mode_key = self._get_mode_key(game_mode)

        if 0 <= index < len(self.highscores[mode_key]):
            # Remove the score at the specified index
            deleted_score = self.highscores[mode_key].pop(index)
            print(f"Deleted score: {deleted_score['score']} by {deleted_score['name']}")

            # Save the updated high scores
            self.save_highscores()
            return True
        else:
            print(f"Invalid index: {index}")
            return False


class Particle:
    def __init__(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int],
        size: float,
        velocity: Tuple[float, float],
        lifetime: float,
        alpha: int = 255,
        shrink: bool = True,
        gravity: float = 0,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.initial_size = size
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alpha = alpha
        self.shrink = shrink
        self.gravity = gravity
        self.creation_time = time.time()

    def update(self, dt: float) -> None:
        # Scale velocity by delta time for frame-rate independence
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt

        # Apply gravity
        if self.gravity > 0:
            self.velocity = (self.velocity[0], self.velocity[1] + self.gravity * dt)

        # Update lifetime
        self.lifetime -= dt

        # Update size if shrinking
        if self.shrink:
            self.size = self.initial_size * (self.lifetime / self.max_lifetime)

        # Update alpha (fade out)
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))

    def draw(self, screen: pygame.Surface) -> None:
        if self.lifetime <= 0:
            return

        try:
            # Create a surface with per-pixel alpha
            particle_surface = pygame.Surface(
                (self.size * 2, self.size * 2), pygame.SRCALPHA
            )

            # Make sure alpha is within valid range
            alpha = max(0, min(255, self.alpha))

            # Make sure color values are valid
            r = max(0, min(255, self.color[0]))
            g = max(0, min(255, self.color[1]))
            b = max(0, min(255, self.color[2]))

            # Draw the particle with alpha
            pygame.draw.circle(
                particle_surface,
                (r, g, b, alpha),
                (self.size, self.size),
                self.size,
            )

            # Blit the particle surface onto the screen
            screen.blit(particle_surface, (self.x - self.size, self.y - self.size))
        except Exception as e:
            # Silently fail if there's an error drawing a particle
            pass

    def is_alive(self) -> bool:
        return self.lifetime > 0


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
        self.last_update_time = time.time()
        # Pre-create some surfaces for common particle sizes to improve performance
        self.surface_cache = {}
        
    def add_particle(self, particle: Particle) -> None:
        """Add a particle with a limit for performance"""
        # Stricter limit on total particles for better performance
        if len(self.particles) >= 50:  # Reduced from 100 to 50
            # Replace oldest particle instead of just dropping new ones
            oldest_index = 0
            oldest_time = float('inf')
            for i, p in enumerate(self.particles):
                if p.creation_time < oldest_time:
                    oldest_time = p.creation_time
                    oldest_index = i
            self.particles[oldest_index] = particle
        else:
            self.particles.append(particle)

    def update(self, dt: float) -> None:
        """Update all particles with improved performance"""
        # If dt is not provided or is zero, calculate it
        if dt <= 0:
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

        # Cap dt to avoid large jumps
        dt = min(dt, 0.1)

        # More efficient in-place filtering
        i = 0
        while i < len(self.particles):
            particle = self.particles[i]
            particle.update(dt)
            if particle.is_alive():
                i += 1
            else:
                # Remove dead particles in-place (faster than creating a new list)
                self.particles[i] = self.particles[-1]
                self.particles.pop()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all particles with improved performance"""
        # Batch similar particles together to reduce surface creation
        for particle in self.particles:
            if particle.lifetime <= 0:
                continue

            try:
                # Round size to nearest integer to improve cache hits
                size = int(particle.size)
                if size <= 0:
                    continue
                    
                # Make sure alpha is within valid range
                alpha = max(0, min(255, particle.alpha))

                # Make sure color values are valid
                r = max(0, min(255, particle.color[0]))
                g = max(0, min(255, particle.color[1]))
                b = max(0, min(255, particle.color[2]))
                
                # Use cached surface if available for this size
                surface_key = size
                if surface_key not in self.surface_cache:
                    # Create and cache a new surface for this size
                    self.surface_cache[surface_key] = pygame.Surface(
                        (size * 2, size * 2), pygame.SRCALPHA
                    )
                    
                # Get the cached surface and clear it
                particle_surface = self.surface_cache[surface_key]
                particle_surface.fill((0, 0, 0, 0))
                
                # Draw the particle with alpha
                pygame.draw.circle(
                    particle_surface,
                    (r, g, b, alpha),
                    (size, size),
                    size,
                )

                # Blit the particle surface onto the screen
                screen.blit(particle_surface, (particle.x - size, particle.y - size))
            except:
                # Silently fail if there's an error drawing a particle
                pass

    def create_spark(
        self, x: float, y: float, count: int = 5, intensity: float = 1.0
    ) -> None:
        """Create spark particles at the given position with adjustable intensity - optimized version"""
        for _ in range(count):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150) * intensity * scale_value(1.0)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            # Simplified color choices - fewer options
            color_choice = random.choice(
                [
                    (255, 255, 0),  # Yellow
                    (255, 165, 0),  # Orange
                ]
            )

            # Create the particle with enhanced properties based on intensity
            particle = Particle(
                x=x + random.uniform(-5, 5) * intensity * scale_value(1.0),
                y=y + random.uniform(-5, 5) * intensity * scale_value(1.0),
                color=color_choice,
                size=random.uniform(1, 3) * intensity * scale_value(1.0),
                velocity=velocity,
                lifetime=random.uniform(0.2, 0.6) * intensity,  # Shorter lifetime
                shrink=True,
                gravity=random.uniform(-10, 10) * intensity * scale_value(1.0),
            )
            self.add_particle(particle)

            # Add a glow effect for fewer particles
            if random.random() < 0.2:  # Reduced from 0.3 to 0.2
                glow = Particle(
                    x=particle.x,
                    y=particle.y,
                    color=color_choice,
                    size=particle.size * 1.5,  # Smaller glow (reduced from 2)
                    velocity=particle.velocity,
                    lifetime=particle.lifetime * 0.7,
                    alpha=80,  # Reduced from 100
                    shrink=True,
                    gravity=particle.gravity,
                )
                self.add_particle(glow)

    def create_smoke(
        self,
        x: float,
        y: float,
        count: int = 3,  # Reduced default from 5 to 3
        color_base: Tuple[int, int, int] = None,
    ) -> None:
        """Create smoke particles at the given position with optional color base - optimized version"""
        for _ in range(count):
            # Upward and slightly random velocity
            velocity = (random.uniform(-10, 10), random.uniform(-30, -10))

            # Color with random variation
            if color_base:
                # Use provided color base with some variation
                r = min(255, max(0, color_base[0] + random.randint(-20, 20)))
                g = min(255, max(0, color_base[1] + random.randint(-20, 20)))
                b = min(255, max(0, color_base[2] + random.randint(-20, 20)))
                color = (r, g, b)
            else:
                # Default gray smoke
                gray_value = random.randint(150, 200)
                color = (gray_value, gray_value, gray_value)

            # Create the particle with more dynamic properties
            particle = Particle(
                x=x + random.uniform(-8, 8),  # Add position variation
                y=y + random.uniform(-8, 8),
                color=color,
                size=random.uniform(5, 15),  # Smaller size range (was 5-20)
                velocity=velocity,
                lifetime=random.uniform(0.5, 1.5),  # Shorter lifetime (was 0.5-2.5)
                shrink=True,  # Always shrink for consistency
                gravity=random.uniform(-8, -2),  # Variable rise speed
            )
            self.add_particle(particle)

            # Add smaller particles less frequently
            if random.random() < 0.3:  # Reduced from 0.5 to 0.3
                small_particle = Particle(
                    x=particle.x + random.uniform(-5, 5),
                    y=particle.y + random.uniform(-5, 5),
                    color=color,
                    size=particle.size * 0.5,
                    velocity=(
                        velocity[0] * 1.2,
                        velocity[1] * 1.2,
                    ),  # Move a bit faster
                    lifetime=particle.lifetime * 0.7,
                    shrink=True,
                    gravity=particle.gravity * 0.8,
                )
                self.add_particle(small_particle)

    def create_crash(self, x: float, y: float) -> None:
        """Create an enhanced crash effect with multiple particle types but optimized for performance"""
        # Create a burst of sparks with high intensity but fewer particles
        self.create_spark(x, y, count=8, intensity=1.5)  # Reduced from 15 to 8

        # Create smoke with different colors for a more dramatic effect but fewer particles
        self.create_smoke(x, y, count=3)  # Reduced from 5 to 3
        self.create_smoke(x, y, count=5, color_base=(100, 100, 100))  # Reduced from 10 to 5
        self.create_smoke(x, y, count=4, color_base=(50, 50, 50))  # Reduced from 8 to 4

        # Add some fire/explosion particles - reduced count
        for _ in range(10):  # Reduced from 20 to 10
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 250) * scale_value(1.0)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            # Fire colors
            color_choice = random.choice(
                [
                    (255, 0, 0),  # Red
                    (255, 69, 0),  # Red-Orange
                    (255, 140, 0),  # Dark Orange
                    (255, 165, 0),  # Orange
                ]
            )

            # Create fire particle
            fire_particle = Particle(
                x=x + random.uniform(-10, 10) * scale_value(1.0),
                y=y + random.uniform(-10, 10) * scale_value(1.0),
                color=color_choice,
                size=random.uniform(5, 15) * scale_value(1.0),
                velocity=velocity,
                lifetime=random.uniform(0.3, 0.8),
                shrink=True,
                gravity=random.uniform(-50, 50) * scale_value(1.0),
            )
            self.add_particle(fire_particle)

            # Add glow effect to fewer fire particles
            if random.random() < 0.3:  # Reduced from 0.5 to 0.3
                glow = Particle(
                    x=fire_particle.x,
                    y=fire_particle.y,
                    color=color_choice,
                    size=fire_particle.size * 2,
                    velocity=fire_particle.velocity,
                    lifetime=fire_particle.lifetime * 0.7,
                    alpha=100,
                    shrink=True,
                    gravity=fire_particle.gravity,
                )
                self.add_particle(glow)

        # Create debris particles with enhanced physics - reduced count
        for _ in range(12):  # Reduced from 25 to 12
            # Random velocity in all directions, but stronger than sparks
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 400) * scale_value(1.0)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            # Random colors for debris - add car color variations
            color_choice = random.choice(
                [
                    (100, 100, 100),  # Gray
                    (80, 80, 80),  # Dark Gray
                    (50, 50, 50),  # Very Dark Gray
                    (100, 0, 0),  # Dark Red (car parts)
                ]
            )

            # Create the particle with gravity and rotation
            particle = Particle(
                x=x + random.uniform(-15, 15) * scale_value(1.0),
                y=y + random.uniform(-15, 15) * scale_value(1.0),
                color=color_choice,
                size=random.uniform(3, 12) * scale_value(1.0),
                velocity=velocity,
                lifetime=random.uniform(0.5, 2.0),
                shrink=True,  # Always shrink for consistency
                gravity=random.uniform(150, 300) * scale_value(1.0),
            )
            self.add_particle(particle)

        # Create a shockwave effect - reduced count
        for i in range(5):  # Reduced from 10 to 5
            size = (5 + i * 5) * scale_value(1.0)  # Increasing sizes
            alpha = 200 - i * 20  # Decreasing alpha

            shockwave = Particle(
                x=x,
                y=y,
                color=(255, 255, 255),  # White shockwave
                size=size,
                velocity=(0, 0),  # Stationary
                lifetime=0.1 + i * 0.05,  # Longer lifetime for larger rings
                alpha=alpha,
                shrink=False,
                gravity=0,
            )
            self.add_particle(shockwave)

    def create_boost_trail(self, x: float, y: float) -> None:
        """Create optimized boost trail particles behind a car"""
        # Create fewer particles at slightly different positions
        for _ in range(3):  # Reduced from 5 to 3 particles
            # Random position variation
            pos_x = x + random.uniform(-15, 15)
            pos_y = y + random.uniform(-8, 8)

            # Downward velocity (car is moving up the screen)
            velocity = (random.uniform(-8, 8), random.uniform(15, 40))

            # Random color from boost colors with fewer variations
            color_choice = random.choice(
                [
                    BOOST_COLOR,
                    (255, 140, 0),  # Dark Orange
                    (255, 99, 71),  # Tomato
                ]
            )

            # Create the main particle
            particle = Particle(
                x=pos_x,
                y=pos_y,
                color=color_choice,
                size=random.uniform(6, 10),  # Slightly smaller size range
                velocity=velocity,
                lifetime=random.uniform(0.4, 0.8),  # Slightly shorter lifetime
                shrink=True,
                gravity=random.uniform(-5, 5),  # Some drift up, some down
            )
            self.add_particle(particle)

            # Add a glow effect for fewer particles
            if random.random() < 0.4:  # Reduced from 0.6 to 0.4
                glow = Particle(
                    x=pos_x,
                    y=pos_y,
                    color=color_choice,
                    size=particle.size * 1.5,  # Smaller glow (reduced from 1.8)
                    velocity=particle.velocity,
                    lifetime=particle.lifetime * 0.7,
                    alpha=100,  # Semi-transparent
                    shrink=True,
                    gravity=particle.gravity,
                )
                self.add_particle(glow)

        # Add spark particles less frequently
        if random.random() < 0.2:  # Reduced from 0.3 to 0.2
            self.create_spark(x, y, count=2, intensity=0.7)  # Reduced from 3 to 2

    def create_tire_tracks(self, x: float, y: float, is_drifting: bool = False) -> None:
        """Create tire track marks on the road"""
        # Determine intensity based on whether the car is drifting
        count = 8 if is_drifting else 3
        size_factor = 1.5 if is_drifting else 1.0

        for _ in range(count):
            # Position with slight variation
            pos_x = x + random.uniform(-20, 20)
            pos_y = y + random.uniform(-5, 5)

            # Darker color for tire tracks
            darkness = random.randint(20, 40)
            color = (darkness, darkness, darkness)

            # Create the tire mark particle
            particle = Particle(
                x=pos_x,
                y=pos_y,
                color=color,
                size=random.uniform(2, 4) * size_factor,
                velocity=(0, 0),  # Stationary
                lifetime=random.uniform(1.0, 3.0),  # Longer lifetime
                shrink=False,
                gravity=0,
            )
            self.add_particle(particle)

        # Add some smoke if drifting
        if is_drifting:
            self.create_smoke(x, y, count=5, color_base=(50, 50, 50))

    def create_water_splash(self, x: float, y: float) -> None:
        """Create water splash effect"""
        # Create water droplets
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            # Blue/white colors for water
            color_choice = random.choice(
                [
                    (0, 191, 255),  # Deep Sky Blue
                    (135, 206, 250),  # Light Sky Blue
                    (173, 216, 230),  # Light Blue
                    (240, 248, 255),  # Alice Blue
                    (240, 255, 255),  # Azure
                ]
            )

            # Create water particle
            particle = Particle(
                x=x + random.uniform(-10, 10),
                y=y + random.uniform(-10, 10),
                color=color_choice,
                size=random.uniform(2, 6),
                velocity=velocity,
                lifetime=random.uniform(0.5, 1.2),
                shrink=True,
                gravity=random.uniform(100, 300),  # Water falls down
            )
            self.add_particle(particle)


class PowerUp:
    def __init__(self, lane, type):
        self.lane = lane
        self.x = LANE_POSITIONS[lane]
        self.y = -POWERUP_HEIGHT // 2
        self.width = POWERUP_WIDTH
        self.height = POWERUP_HEIGHT
        self.type = type  # 'boost', 'shield', 'magnet', 'coin', 'slow_mo'

        # Set color based on type
        if self.type == "boost":
            self.color = BOOST_COLOR
            self.symbol = "⚡"
        elif self.type == "shield":
            self.color = SHIELD_COLOR
            self.symbol = "🛡️"
        elif self.type == "magnet":
            self.color = MAGNET_COLOR
            self.symbol = "🧲"
        elif self.type == "coin":
            self.color = COIN_COLOR
            self.symbol = "💰"
        elif self.type == "slow_mo":
            self.color = SLOW_MO_COLOR
            self.symbol = "⏱️"

        self.pulse_effect = 0
        self.collected = False

    def draw(self, screen):
        """Draw the power-up with enhanced animations"""
        # Skip drawing if collected
        if self.collected:
            return

        # Pulsating effect
        self.pulse_effect = (self.pulse_effect + 0.1) % (2 * math.pi)
        pulse_size = math.sin(self.pulse_effect) * 5
        
        # Rotation effect
        rotation_angle = (pygame.time.get_ticks() * 0.05) % 360
        
        # Floating up and down animation
        float_offset = math.sin(pygame.time.get_ticks() * 0.003) * 3
        draw_y = self.y + float_offset

        # Draw power-up with glow effect
        for offset in range(3, 0, -1):
            glow_color = (*self.color, 100 - offset * 30)
            glow_surface = pygame.Surface(
                (
                    self.width + offset * 4 + pulse_size,
                    self.height + offset * 4 + pulse_size,
                ),
                pygame.SRCALPHA,
            )
            pygame.draw.circle(
                glow_surface,
                glow_color,
                (glow_surface.get_width() // 2, glow_surface.get_height() // 2),
                (self.width + offset * 4 + pulse_size) // 2,
            )
            screen.blit(
                glow_surface,
                (
                    self.x - glow_surface.get_width() // 2,
                    draw_y - glow_surface.get_height() // 2,
                ),
            )

        # Draw main power-up
        pygame.draw.circle(screen, self.color, (self.x, draw_y), self.width // 2)
        
        # Draw inner highlight for 3D effect
        highlight_color = (
            min(self.color[0] + 50, 255),
            min(self.color[1] + 50, 255),
            min(self.color[2] + 50, 255),
        )
        pygame.draw.circle(
            screen, 
            highlight_color, 
            (self.x - self.width // 8, draw_y - self.height // 8), 
            self.width // 4
        )

        # Draw symbol with rotation
        font = get_font(20, bold=True)
        symbol_text = font.render(self.symbol, True, WHITE)
        
        # Create a rotated version of the symbol
        if self.type != "coin":  # Don't rotate coin symbol
            rotated_symbol = pygame.transform.rotate(symbol_text, rotation_angle)
            symbol_rect = rotated_symbol.get_rect(center=(self.x, draw_y))
            screen.blit(rotated_symbol, symbol_rect)
        else:
            symbol_rect = symbol_text.get_rect(center=(self.x, draw_y))
            screen.blit(symbol_text, symbol_rect)
            
        # Add special effects based on power-up type
        if self.type == "boost":
            # Add speed lines
            for i in range(3):
                angle = rotation_angle + i * 120
                rad_angle = math.radians(angle)
                line_length = self.width // 2 + 5 + pulse_size // 2
                end_x = self.x + math.cos(rad_angle) * line_length
                end_y = draw_y + math.sin(rad_angle) * line_length
                pygame.draw.line(
                    screen,
                    BOOST_COLOR,
                    (self.x, draw_y),
                    (end_x, end_y),
                    2
                )
        elif self.type == "shield":
            # Add shield ring
            shield_radius = self.width // 2 + 5 + pulse_size // 2
            pygame.draw.circle(
                screen,
                SHIELD_COLOR,
                (self.x, draw_y),
                shield_radius,
                2
            )
        elif self.type == "magnet":
            # Add magnetic field lines
            for i in range(4):
                angle = rotation_angle + i * 90
                rad_angle = math.radians(angle)
                line_start = self.width // 2 - 5
                line_end = self.width // 2 + 10 + pulse_size // 2
                
                start_x = self.x + math.cos(rad_angle) * line_start
                start_y = draw_y + math.sin(rad_angle) * line_start
                end_x = self.x + math.cos(rad_angle) * line_end
                end_y = draw_y + math.sin(rad_angle) * line_end
                
                pygame.draw.line(
                    screen,
                    MAGNET_COLOR,
                    (start_x, start_y),
                    (end_x, end_y),
                    2
                )
        elif self.type == "slow_mo":
            # Add clock hand animation
            hand_length = self.width // 2 - 5
            hand_angle = math.radians(rotation_angle * 2)  # Rotate twice as fast
            hand_x = self.x + math.cos(hand_angle) * hand_length
            hand_y = draw_y + math.sin(hand_angle) * hand_length
            
            pygame.draw.line(
                screen,
                SLOW_MO_COLOR,
                (self.x, draw_y),
                (hand_x, hand_y),
                2
            )

    def move(self, speed):
        self.y += speed

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2

    def collides_with(self, car):
        if self.collected:
            return False
        return (
            abs(self.x - car.x) < (self.width + car.width) // 2
            and abs(self.y - car.y) < (self.height + car.height) // 2
        )

    def collect(self):
        self.collected = True


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.color = COIN_COLOR
        self.collected = False
        self.pulse_effect = random.random() * 2 * math.pi

    def draw(self, screen):
        """Draw the coin with enhanced animations"""
        if self.collected:
            return

        # Pulsating effect
        self.pulse_effect = (self.pulse_effect + 0.1) % (2 * math.pi)
        pulse_size = math.sin(self.pulse_effect) * 2
        
        # Spinning animation
        spin_angle = (pygame.time.get_ticks() * 0.1) % 360
        spin_scale = abs(math.sin(math.radians(spin_angle))) * 0.3 + 0.7  # 0.7 to 1.0 scale
        
        # Draw coin with glow and 3D effect
        # Outer glow
        for offset in range(3, 0, -1):
            glow_radius = (self.width // 2 + pulse_size + offset * 2) * spin_scale
            glow_alpha = 100 - offset * 30
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surface,
                (*self.color, glow_alpha),
                (glow_radius, glow_radius),
                glow_radius
            )
            screen.blit(
                glow_surface,
                (self.x - glow_radius, self.y - glow_radius)
            )
        
        # Main coin body
        coin_radius = (self.width // 2 + pulse_size) * spin_scale
        pygame.draw.circle(
            screen, self.color, (self.x, self.y), coin_radius
        )
        
        # Inner highlight
        inner_radius = coin_radius * 0.7
        pygame.draw.circle(
            screen, (255, 255, 200), (self.x, self.y), inner_radius
        )
        
        # Dollar sign or coin detail that rotates with the coin
        if spin_angle < 90 or spin_angle > 270:  # Only show when coin is "facing forward"
            font_size = int(coin_radius * 1.2)
            font = get_font(font_size, bold=True)
            dollar_text = font.render("$", True, (255, 223, 0))
            text_rect = dollar_text.get_rect(center=(self.x, self.y))
            screen.blit(dollar_text, text_rect)

    def move(self, speed):
        self.y += speed

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2

    def collides_with(self, car):
        if self.collected:
            return False
        return (
            abs(self.x - car.x) < (self.width + car.width) // 2
            and abs(self.y - car.y) < (self.height + car.height) // 2
        )

    def collect(self):
        self.collected = True


class Car:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lane = 1  # Starting lane (0-7 for 8 lanes)

        # Power-up states
        self.has_shield = False
        self.shield_timer = 0
        self.has_boost = False
        self.boost_timer = 0
        self.has_magnet = False
        self.magnet_timer = 0
        self.has_slow_mo = False
        self.slow_mo_timer = 0

        # Boost energy
        self.boost_energy = 0
        self.max_boost_energy = 100

        # Animation variables
        self.swerve_offset = 0
        self.swerve_direction = 0
        self.is_boosting = False
        self.boost_particles = []

        # Particle effects
        self.tire_smoke_cooldown = 0

    def draw(self, screen):
        # Calculate actual x position with swerve offset
        actual_x = self.x + self.swerve_offset

        # Add bounce animation effect when driving
        bounce_offset = math.sin(pygame.time.get_ticks() * 0.01) * 2
        draw_y = self.y + bounce_offset

        # Car body
        pygame.draw.rect(
            screen,
            self.color,
            [
                actual_x - self.width // 2,
                draw_y - self.height // 2,
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
                actual_x - self.width // 2,
                draw_y - self.height // 2,
                self.width // 2,
                self.height,
            ],
            0,
            10,
        )

        # Windshield
        windshield_width = int(self.width * 0.8)
        windshield_height = int(self.height * 0.3)
        windshield_x = actual_x - windshield_width // 2
        windshield_y = draw_y - self.height // 2 + int(self.height * 0.15)
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
        roof_x = actual_x - roof_width // 2
        roof_y = draw_y - self.height // 2 + int(self.height * 0.15) + windshield_height
        pygame.draw.rect(
            screen, self.color, [roof_x, roof_y, roof_width, roof_height], 0, 5
        )

        # Rear window
        rear_window_width = int(self.width * 0.7)
        rear_window_height = int(self.height * 0.2)
        rear_window_x = actual_x - rear_window_width // 2
        rear_window_y = roof_y + roof_height
        pygame.draw.rect(
            screen,
            (100, 200, 255),
            [rear_window_x, rear_window_y, rear_window_width, rear_window_height],
            0,
            5,
        )

        # Wheels with rotation animation
        wheel_width = int(self.width * 0.25)
        wheel_height = int(self.height * 0.15)
        wheel_rotation = (pygame.time.get_ticks() * 0.2) % 360  # Rotation angle based on time

        # Front left wheel
        self.draw_wheel(
            screen, 
            actual_x - self.width // 2 - 3,
            draw_y - self.height // 4,
            wheel_width,
            wheel_height,
            wheel_rotation
        )

        # Front right wheel
        self.draw_wheel(
            screen,
            actual_x + self.width // 2 - wheel_width + 3,
            draw_y - self.height // 4,
            wheel_width,
            wheel_height,
            wheel_rotation
        )

        # Rear left wheel
        self.draw_wheel(
            screen,
            actual_x - self.width // 2 - 3,
            draw_y + self.height // 4 - wheel_height,
            wheel_width,
            wheel_height,
            wheel_rotation
        )

        # Rear right wheel
        self.draw_wheel(
            screen,
            actual_x + self.width // 2 - wheel_width + 3,
            draw_y + self.height // 4 - wheel_height,
            wheel_width,
            wheel_height,
            wheel_rotation
        )

        # Headlights with glow effect
        headlight_width = int(self.width * 0.15)
        headlight_height = int(self.height * 0.08)

        # Left headlight glow - pulsating effect
        glow_intensity = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5 + 0.5  # 0.5 to 1.5
        for offset in range(3, 0, -1):
            glow_color = (255, 255, 100, int((100 - offset * 30) * glow_intensity))
            glow_surface = pygame.Surface(
                (headlight_width + offset * 4, headlight_height + offset * 4),
                pygame.SRCALPHA,
            )
            pygame.draw.rect(
                glow_surface,
                glow_color,
                [0, 0, headlight_width + offset * 4, headlight_height + offset * 4],
                0,
                5,
            )
            screen.blit(
                glow_surface,
                (
                    actual_x - self.width // 2 + 5 - offset * 2,
                    draw_y - self.height // 2 + 5 - offset * 2,
                ),
            )

        # Left headlight
        pygame.draw.rect(
            screen,
            NEON_YELLOW,
            [
                actual_x - self.width // 2 + 5,
                draw_y - self.height // 2 + 5,
                headlight_width,
                headlight_height,
            ],
            0,
            3,
        )

        # Right headlight glow
        for offset in range(3, 0, -1):
            glow_color = (255, 255, 100, int((100 - offset * 30) * glow_intensity))
            glow_surface = pygame.Surface(
                (headlight_width + offset * 4, headlight_height + offset * 4),
                pygame.SRCALPHA,
            )
            pygame.draw.rect(
                glow_surface,
                glow_color,
                [0, 0, headlight_width + offset * 4, headlight_height + offset * 4],
                0,
                5,
            )
            screen.blit(
                glow_surface,
                (
                    actual_x + self.width // 2 - headlight_width - 5 - offset * 2,
                    draw_y - self.height // 2 + 5 - offset * 2,
                ),
            )

        # Right headlight
        pygame.draw.rect(
            screen,
            NEON_YELLOW,
            [
                actual_x + self.width // 2 - headlight_width - 5,
                draw_y - self.height // 2 + 5,
                headlight_width,
                headlight_height,
            ],
            0,
            3,
        )

        # Taillights with brake light animation
        taillight_width = int(self.width * 0.15)
        taillight_height = int(self.height * 0.08)
        
        # Brake light effect - brighter when slowing down
        brake_intensity = 1.0
        if hasattr(self, 'prev_speed') and hasattr(self, 'speed'):
            if self.speed < self.prev_speed:
                brake_intensity = 1.5  # Brighter when braking
        
        # Taillight color with brake intensity
        taillight_color = (
            min(int(BRIGHT_RED[0] * brake_intensity), 255),
            min(int(BRIGHT_RED[1] * brake_intensity), 255),
            min(int(BRIGHT_RED[2] * brake_intensity), 255)
        )

        # Left taillight
        pygame.draw.rect(
            screen,
            taillight_color,
            [
                actual_x - self.width // 2 + 5,
                draw_y + self.height // 2 - taillight_height - 5,
                taillight_width,
                taillight_height,
            ],
            0,
            3,
        )

        # Right taillight
        pygame.draw.rect(
            screen,
            taillight_color,
            [
                actual_x + self.width // 2 - taillight_width - 5,
                draw_y + self.height // 2 - taillight_height - 5,
                taillight_width,
                taillight_height,
            ],
            0,
            3,
        )

        # Draw boost particles if boosting
        if self.is_boosting:
            for i in range(5):
                particle_x = random.randint(
                    int(actual_x - self.width // 3), int(actual_x + self.width // 3)
                )
                particle_y = draw_y + self.height // 2 + random.randint(5, 15)
                particle_size = random.randint(3, 8)
                particle_color = random.choice(
                    [BOOST_COLOR, (255, 69, 0), (255, 215, 0)]
                )
                pygame.draw.circle(
                    screen, particle_color, (particle_x, particle_y), particle_size
                )

        # Draw shield if active
        if self.has_shield:
            shield_radius = max(self.width, self.height) * 0.7
            shield_surface = pygame.Surface(
                (shield_radius * 2, shield_radius * 2), pygame.SRCALPHA
            )

            # Pulsating effect based on remaining time
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 10
            shield_alpha = int(100 + pulse)

            # Draw shield with transparency
            pygame.draw.circle(
                shield_surface,
                (*SHIELD_COLOR, shield_alpha),
                (shield_radius, shield_radius),
                shield_radius,
            )
            
            # Add rotating shield effect
            rotation_angle = (pygame.time.get_ticks() * 0.05) % 360
            num_segments = 8
            for i in range(num_segments):
                segment_angle = rotation_angle + (i * (360 / num_segments))
                start_angle = math.radians(segment_angle)
                end_angle = math.radians(segment_angle + 20)
                
                # Calculate arc points
                arc_points = []
                for angle in range(int(math.degrees(start_angle)), int(math.degrees(end_angle)) + 1, 5):
                    rad = math.radians(angle)
                    x = shield_radius + math.cos(rad) * (shield_radius - 5)
                    y = shield_radius + math.sin(rad) * (shield_radius - 5)
                    arc_points.append((x, y))
                
                # Draw arc segment if we have enough points
                if len(arc_points) >= 2:
                    pygame.draw.lines(
                        shield_surface,
                        (*SHIELD_COLOR, 200),
                        False,
                        arc_points,
                        3
                    )

            screen.blit(
                shield_surface, (actual_x - shield_radius, draw_y - shield_radius)
            )

        # Draw magnet effect if active
        if self.has_magnet:
            magnet_radius = MAGNET_RANGE
            magnet_surface = pygame.Surface(
                (magnet_radius * 2, magnet_radius * 2), pygame.SRCALPHA
            )

            # Pulsating effect
            pulse = math.sin(pygame.time.get_ticks() * 0.005) * 5
            magnet_alpha = int(30 + pulse)

            # Draw magnet field with transparency
            pygame.draw.circle(
                magnet_surface,
                (*MAGNET_COLOR, magnet_alpha),
                (magnet_radius, magnet_radius),
                magnet_radius,
            )
            
            # Add animated magnetic field lines
            rotation_angle = (pygame.time.get_ticks() * 0.03) % 360
            for i in range(8):  # 8 field lines
                angle = rotation_angle + (i * 45)
                rad_angle = math.radians(angle)
                
                # Inner point
                inner_x = magnet_radius + math.cos(rad_angle) * (magnet_radius * 0.3)
                inner_y = magnet_radius + math.sin(rad_angle) * (magnet_radius * 0.3)
                
                # Outer point
                outer_x = magnet_radius + math.cos(rad_angle) * (magnet_radius - 5)
                outer_y = magnet_radius + math.sin(rad_angle) * (magnet_radius - 5)
                
                # Draw magnetic field line
                pygame.draw.line(
                    magnet_surface,
                    (*MAGNET_COLOR, 100),
                    (inner_x, inner_y),
                    (outer_x, outer_y),
                    3
                )

            screen.blit(
                magnet_surface, (actual_x - magnet_radius, draw_y - magnet_radius)
            )

        # Draw boost energy meter
        self.draw_boost_meter(screen)
        
        # Store current speed for brake light animation
        self.prev_speed = getattr(self, 'speed', 5)
        
    def draw_wheel(self, screen, x, y, width, height, rotation_angle):
        """Draw a wheel with rotation animation"""
        # Draw the wheel base
        pygame.draw.rect(
            screen,
            MATTE_BLACK,
            [x, y, width, height],
            0,
            3,
        )
        
        # Draw wheel rim
        rim_width = width - 6
        rim_height = height - 6
        rim_x = x + 3
        rim_y = y + 3
        
        pygame.draw.rect(
            screen,
            SLEEK_SILVER,
            [rim_x, rim_y, rim_width, rim_height],
            0,
            2,
        )
        
        # Draw spokes to show rotation
        center_x = x + width // 2
        center_y = y + height // 2
        spoke_length = min(rim_width, rim_height) // 2 - 2
        
        for i in range(4):  # 4 spokes
            angle = math.radians(rotation_angle + i * 90)
            end_x = center_x + math.cos(angle) * spoke_length
            end_y = center_y + math.sin(angle) * spoke_length
            
            pygame.draw.line(
                screen,
                MATTE_BLACK,
                (center_x, center_y),
                (end_x, end_y),
                2
            )

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANE_POSITIONS[self.lane]
            # Add swerve effect - negative offset for left movement
            self.swerve_offset = -self.width // 2
            self.swerve_direction = -1
            # Add tire smoke effect
            self.tire_smoke_cooldown = 0.2  # Will create smoke for 0.2 seconds

    def move_right(self):
        if self.lane < 7:  # Using 7 as the maximum lane index (for 8 lanes total)
            self.lane += 1
            self.x = LANE_POSITIONS[self.lane]
            # Add swerve effect - positive offset for right movement
            self.swerve_offset = self.width // 2
            self.swerve_direction = 1
            # Add tire smoke effect
            self.tire_smoke_cooldown = 0.2  # Will create smoke for 0.2 seconds

    def update(self, dt):
        # Update swerve animation
        if self.swerve_offset != 0:
            # Make swerve speed proportional to dt for consistent animation
            swerve_speed = 200 * dt  # pixels per second
            if self.swerve_direction < 0:
                self.swerve_offset = max(0, self.swerve_offset - swerve_speed)
            else:
                self.swerve_offset = min(0, self.swerve_offset + swerve_speed)

        # Update power-up timers
        if self.has_shield:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.has_shield = False

        if self.has_boost:
            self.boost_timer -= dt
            if self.boost_timer <= 0:
                self.has_boost = False
                self.is_boosting = False

        if self.has_magnet:
            self.magnet_timer -= dt
            if self.magnet_timer <= 0:
                self.has_magnet = False

        if self.has_slow_mo:
            self.slow_mo_timer -= dt
            if self.slow_mo_timer <= 0:
                self.has_slow_mo = False

        # Update tire smoke cooldown
        if self.tire_smoke_cooldown > 0:
            self.tire_smoke_cooldown -= dt

    def activate_shield(self):
        self.has_shield = True
        self.shield_timer = SHIELD_DURATION

    def activate_boost(self):
        self.has_boost = True
        self.boost_timer = POWERUP_DURATION
        self.is_boosting = True

    def activate_magnet(self):
        self.has_magnet = True
        self.magnet_timer = POWERUP_DURATION

    def activate_slow_mo(self):
        self.has_slow_mo = True
        self.slow_mo_timer = POWERUP_DURATION

    def add_boost_energy(self, amount):
        self.boost_energy = min(self.max_boost_energy, self.boost_energy + amount)

    def use_boost_energy(self):
        if self.boost_energy >= 30:
            self.boost_energy -= 30
            self.activate_boost()
            return True
        return False

    def draw_boost_meter(self, screen):
        # Draw boost energy meter
        meter_width = 150
        meter_height = 15
        meter_x = 10
        meter_y = SCREEN_HEIGHT - 30

        # Background
        pygame.draw.rect(
            screen, MATTE_BLACK, (meter_x, meter_y, meter_width, meter_height), 0, 5
        )

        # Fill based on energy
        energy_width = int(meter_width * (self.boost_energy / self.max_boost_energy))
        pygame.draw.rect(
            screen, BOOST_COLOR, (meter_x, meter_y, energy_width, meter_height), 0, 5
        )

        # Border
        pygame.draw.rect(
            screen, WHITE, (meter_x, meter_y, meter_width, meter_height), 1, 5
        )

        # Label
        font = get_font(16, bold=True)
        text = font.render("BOOST", True, WHITE)
        screen.blit(text, (meter_x + meter_width + 10, meter_y))


class Obstacle:
    def __init__(self, lane):
        self.lane = lane
        self.x = LANE_POSITIONS[lane]
        self.y = -OBSTACLE_HEIGHT // 2
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.color = BRIGHT_RED
        self.type = random.choice(["cone", "barrier", "pothole"])

    def draw(self, screen):
        if self.type == "cone":
            # Traffic cone with glow effect
            for offset in range(3, 0, -1):
                glow_color = (255, 100, 0, 100 - offset * 30)
                glow_surface = pygame.Surface(
                    (self.width + offset * 4, self.height + offset * 4), pygame.SRCALPHA
                )
                pygame.draw.polygon(
                    glow_surface,
                    glow_color,
                    [
                        (self.width // 2, 0),
                        (0, self.height + offset * 4),
                        (self.width + offset * 4, self.height + offset * 4),
                    ],
                )
                screen.blit(
                    glow_surface,
                    (
                        self.x - self.width // 2 - offset * 2,
                        self.y - self.height // 2 - offset * 2,
                    ),
                )

            # Traffic cone
            pygame.draw.polygon(
                screen,
                (255, 140, 0),
                [
                    (self.x, self.y - self.height // 2),
                    (self.x - self.width // 2, self.y + self.height // 2),
                    (self.x + self.width // 2, self.y + self.height // 2),
                ],
            )
            pygame.draw.rect(
                screen,
                WHITE,
                [
                    self.x - self.width // 4,
                    self.y - self.height // 4,
                    self.width // 2,
                    self.height // 4,
                ],
            )
        elif self.type == "barrier":
            # Road barrier with glow effect
            for offset in range(3, 0, -1):
                glow_color = (255, 50, 50, 100 - offset * 30)
                glow_surface = pygame.Surface(
                    (self.width + offset * 4, self.height + offset * 4), pygame.SRCALPHA
                )
                pygame.draw.rect(
                    glow_surface,
                    glow_color,
                    [0, 0, self.width + offset * 4, self.height + offset * 4],
                    0,
                    5,
                )
                screen.blit(
                    glow_surface,
                    (
                        self.x - self.width // 2 - offset * 2,
                        self.y - self.height // 2 - offset * 2,
                    ),
                )

            # Road barrier
            pygame.draw.rect(
                screen,
                BRIGHT_RED,
                [
                    self.x - self.width // 2,
                    self.y - self.height // 2,
                    self.width,
                    self.height,
                ],
                0,
                5,
            )
            for i in range(3):
                y_pos = self.y - self.height // 2 + (i * self.height // 3)
                pygame.draw.rect(
                    screen,
                    SLEEK_SILVER,
                    [self.x - self.width // 2, y_pos, self.width, self.height // 6],
                )
        else:  # pothole
            # Pothole with glow effect
            for offset in range(3, 0, -1):
                glow_color = (0, 0, 50, 100 - offset * 30)
                glow_surface = pygame.Surface(
                    (self.width + offset * 4, self.height + offset * 4), pygame.SRCALPHA
                )
                pygame.draw.ellipse(
                    glow_surface,
                    glow_color,
                    [0, 0, self.width + offset * 4, self.height + offset * 4],
                )
                screen.blit(
                    glow_surface,
                    (
                        self.x - self.width // 2 - offset * 2,
                        self.y - self.height // 2 - offset * 2,
                    ),
                )

            # Pothole
            pygame.draw.ellipse(
                screen,
                MATTE_BLACK,
                [
                    self.x - self.width // 2,
                    self.y - self.height // 2,
                    self.width,
                    self.height,
                ],
            )
            # Inner pothole with gradient
            inner_color = (20, 20, 40)
            pygame.draw.ellipse(
                screen,
                inner_color,
                [
                    self.x - self.width // 2 + 5,
                    self.y - self.height // 2 + 5,
                    self.width - 10,
                    self.height - 10,
                ],
            )

    def move(self, speed):
        self.y += speed

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2

    def collides_with(self, car):
        return (
            abs(self.x - car.x) < (self.width + car.width) // 2
            and abs(self.y - car.y) < (self.height + car.height) // 2
        )


class MovingObstacle(Obstacle):
    def __init__(self, lane):
        super().__init__(lane)
        self.move_direction = random.choice([-1, 1])
        self.move_speed = random.uniform(0.5, 2.0)
        self.original_x = self.x
        self.move_range = LANE_WIDTH * 0.4
        self.move_progress = 0

    def update(self, dt):
        # Move side to side
        self.move_progress += self.move_speed * dt
        offset = math.sin(self.move_progress) * self.move_range
        self.x = self.original_x + offset


class OtherCar:
    def __init__(self, lane):
        self.lane = lane
        self.x = LANE_POSITIONS[lane]
        self.y = -CAR_HEIGHT // 2
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = random.choice(
            [NEON_GREEN, ELECTRIC_PURPLE, (255, 165, 0), (128, 0, 128), METALLIC_SILVER]
        )
        self.car_type = random.choice(["sedan", "suv", "truck"])
        if self.car_type == "truck":
            self.height = int(CAR_HEIGHT * 1.3)
        elif self.car_type == "suv":
            self.height = int(CAR_HEIGHT * 1.1)
        self.is_car = True  # Flag to identify as a car for AI detection

    def draw(self, screen):
        # Car body
        if self.car_type == "truck":
            # Truck body (cab + trailer)
            cab_height = self.height // 3

            # Trailer
            pygame.draw.rect(
                screen,
                METALLIC_SILVER,
                [
                    self.x - self.width // 2,
                    self.y - self.height // 2 + cab_height,
                    self.width,
                    self.height - cab_height,
                ],
                0,
                5,
            )

            # Add metallic effect with gradient
            highlight_color = (
                min(METALLIC_SILVER[0] + 40, 255),
                min(METALLIC_SILVER[1] + 40, 255),
                min(METALLIC_SILVER[2] + 40, 255),
            )
            pygame.draw.rect(
                screen,
                highlight_color,
                [
                    self.x - self.width // 2,
                    self.y - self.height // 2 + cab_height,
                    self.width // 2,
                    self.height - cab_height,
                ],
                0,
                5,
            )

            # Cab
            pygame.draw.rect(
                screen,
                self.color,
                [
                    self.x - self.width // 2,
                    self.y - self.height // 2,
                    self.width,
                    cab_height,
                ],
                0,
                5,
            )

            # Add metallic effect with gradient to cab
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
                    self.y - self.height // 2,
                    self.width // 2,
                    cab_height,
                ],
                0,
                5,
            )

            # Windshield
            windshield_width = int(self.width * 0.7)
            windshield_height = int(cab_height * 0.6)
            windshield_x = self.x - windshield_width // 2
            windshield_y = self.y - self.height // 2 + int(cab_height * 0.2)
            pygame.draw.rect(
                screen,
                (100, 200, 255),
                [windshield_x, windshield_y, windshield_width, windshield_height],
                0,
                3,
            )

            # Wheels (6 wheels for truck)
            wheel_width = int(self.width * 0.2)
            wheel_height = int(self.height * 0.1)

            wheel_positions = [
                (
                    self.x - self.width // 2 - 3,
                    self.y - self.height // 2 + cab_height - wheel_height // 2,
                ),
                (
                    self.x + self.width // 2 - wheel_width + 3,
                    self.y - self.height // 2 + cab_height - wheel_height // 2,
                ),
                (self.x - self.width // 2 - 3, self.y),
                (self.x + self.width // 2 - wheel_width + 3, self.y),
                (
                    self.x - self.width // 2 - 3,
                    self.y + self.height // 2 - wheel_height,
                ),
                (
                    self.x + self.width // 2 - wheel_width + 3,
                    self.y + self.height // 2 - wheel_height,
                ),
            ]

            for pos in wheel_positions:
                pygame.draw.rect(
                    screen,
                    MATTE_BLACK,
                    [pos[0], pos[1], wheel_width, wheel_height],
                    0,
                    3,
                )
                # Add wheel rim
                pygame.draw.rect(
                    screen,
                    SLEEK_SILVER,
                    [pos[0] + 3, pos[1] + 3, wheel_width - 6, wheel_height - 6],
                    0,
                    3,
                )

        else:  # sedan or SUV
            # Car body
            pygame.draw.rect(
                screen,
                self.color,
                [
                    self.x - self.width // 2,
                    self.y - self.height // 2,
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
                    self.y - self.height // 2,
                    self.width // 2,
                    self.height,
                ],
                0,
                10,
            )

            # Windshield
            windshield_width = int(self.width * 0.8)
            windshield_height = int(self.height * 0.25)
            windshield_x = self.x - windshield_width // 2
            windshield_y = self.y - self.height // 2 + int(self.height * 0.15)
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
            roof_y = (
                self.y - self.height // 2 + int(self.height * 0.15) + windshield_height
            )
            pygame.draw.rect(
                screen, self.color, [roof_x, roof_y, roof_width, roof_height], 0, 5
            )

            # Rear window
            rear_window_width = int(self.width * 0.7)
            rear_window_height = int(self.height * 0.2)
            rear_window_x = self.x - rear_window_width // 2
            rear_window_y = roof_y + roof_height
            pygame.draw.rect(
                screen,
                (100, 200, 255),
                [rear_window_x, rear_window_y, rear_window_width, rear_window_height],
                0,
                5,
            )

            # Wheels
            wheel_width = int(self.width * 0.25)
            wheel_height = int(self.height * 0.15)

            wheel_positions = [
                (self.x - self.width // 2 - 3, self.y - self.height // 4),
                (self.x + self.width // 2 - wheel_width + 3, self.y - self.height // 4),
                (
                    self.x - self.width // 2 - 3,
                    self.y + self.height // 4 - wheel_height,
                ),
                (
                    self.x + self.width // 2 - wheel_width + 3,
                    self.y + self.height // 4 - wheel_height,
                ),
            ]

            for pos in wheel_positions:
                pygame.draw.rect(
                    screen,
                    MATTE_BLACK,
                    [pos[0], pos[1], wheel_width, wheel_height],
                    0,
                    3,
                )
                # Add wheel rim
                pygame.draw.rect(
                    screen,
                    SLEEK_SILVER,
                    [pos[0] + 3, pos[1] + 3, wheel_width - 6, wheel_height - 6],
                    0,
                    3,
                )

            # Headlights
            headlight_width = int(self.width * 0.15)
            headlight_height = int(self.height * 0.08)

            # Left headlight
            pygame.draw.rect(
                screen,
                NEON_YELLOW,
                [
                    self.x - self.width // 2 + 5,
                    self.y - self.height // 2 + 5,
                    headlight_width,
                    headlight_height,
                ],
                0,
                3,
            )

            # Right headlight
            pygame.draw.rect(
                screen,
                NEON_YELLOW,
                [
                    self.x + self.width // 2 - headlight_width - 5,
                    self.y - self.height // 2 + 5,
                    headlight_width,
                    headlight_height,
                ],
                0,
                3,
            )

            # Taillights
            taillight_width = int(self.width * 0.15)
            taillight_height = int(self.height * 0.08)

            # Left taillight
            pygame.draw.rect(
                screen,
                BRIGHT_RED,
                [
                    self.x - self.width // 2 + 5,
                    self.y + self.height // 2 - taillight_height - 5,
                    taillight_width,
                    taillight_height,
                ],
                0,
                3,
            )

            # Right taillight
            pygame.draw.rect(
                screen,
                BRIGHT_RED,
                [
                    self.x + self.width // 2 - taillight_width - 5,
                    self.y + self.height // 2 - taillight_height - 5,
                    taillight_width,
                    taillight_height,
                ],
                0,
                3,
            )

    def move(self, speed):
        self.y += speed

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.height // 2

    def collides_with(self, car):
        return (
            abs(self.x - car.x) < (self.width + car.width) // 2
            and abs(self.y - car.y) < (self.height + car.height) // 2
        )


class AIControlledCar(OtherCar):
    def __init__(self, lane):
        super().__init__(lane)
        self.ai_type = random.choice(["normal", "aggressive", "cautious"])
        self.lane_change_cooldown = 0
        self.brake_cooldown = 0
        self.is_braking = False
        self.target_lane = lane

    def update(self, dt, player_lane, obstacles):
        # Update lane change cooldown
        if self.lane_change_cooldown > 0:
            self.lane_change_cooldown -= dt

        # Update brake cooldown
        if self.brake_cooldown > 0:
            self.brake_cooldown -= dt
            if self.brake_cooldown <= 0:
                self.is_braking = False

        # AI decision making
        if self.lane_change_cooldown <= 0:
            # Check for obstacles in current lane
            obstacle_ahead = False
            
            # First check for static obstacles
            for obstacle in obstacles:
                if not hasattr(obstacle, 'is_car') and obstacle.lane == self.lane and obstacle.y > self.y and obstacle.y - self.y < 300:
                    obstacle_ahead = True
                    break
                    
            # Then check for other cars
            car_ahead = False
            for other in obstacles:
                if (hasattr(other, 'is_car') and 
                    other != self and  # Don't detect self
                    other.lane == self.lane and 
                    other.y > self.y and 
                    other.y - self.y < 250):
                    car_ahead = True
                    break

            # Decide whether to change lanes
            if obstacle_ahead or car_ahead:
                # Find a safe lane to move to
                safe_lanes = []
                for l in range(8):  # Changed from 6 to 8 lanes
                    if l != self.lane:
                        lane_safe = True
                        
                        # Check for obstacles in the potential lane
                        for obstacle in obstacles:
                            if not hasattr(obstacle, 'is_car') and obstacle.lane == l and abs(obstacle.y - self.y) < 200:
                                lane_safe = False
                                break
                                
                        # Check for other cars in the potential lane
                        for other in obstacles:
                            if (hasattr(other, 'is_car') and 
                                other != self and  # Don't detect self
                                other.lane == l and 
                                abs(other.y - self.y) < 200):
                                lane_safe = False
                                break
                                
                        if lane_safe:
                            safe_lanes.append(l)

                if safe_lanes:
                    self.target_lane = random.choice(safe_lanes)
                    self.lane_change_cooldown = random.uniform(2.0, 4.0)
                elif self.ai_type == "aggressive":
                    # Aggressive cars might brake suddenly
                    if random.random() < 0.3 and self.brake_cooldown <= 0:
                        self.is_braking = True
                        self.brake_cooldown = random.uniform(0.5, 1.5)
            elif (
                self.ai_type == "aggressive"
                and random.random() < 0.05
                and self.lane != player_lane
            ):
                # Aggressive cars might randomly change lanes to block player
                self.target_lane = player_lane
                self.lane_change_cooldown = random.uniform(2.0, 4.0)
            elif self.ai_type == "normal" and random.random() < 0.02:
                # Normal cars occasionally change lanes randomly
                new_lane = random.randint(0, 7)  # Changed from 0-5 to 0-7 for 8 lanes
                if new_lane != self.lane:
                    self.target_lane = new_lane
                    self.lane_change_cooldown = random.uniform(2.0, 5.0)

        # Move towards target lane
        if self.lane != self.target_lane:
            if self.target_lane > self.lane:
                self.lane += 1
            else:
                self.lane -= 1
            self.x = LANE_POSITIONS[self.lane]


class SettingsMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = get_font(int(screen_height * 0.06), bold=True)
        self.font_medium = get_font(int(screen_height * 0.04), bold=True)
        self.font_small = get_font(int(screen_height * 0.03))
        
        # Settings options
        self.settings = {
            "FULLSCREEN": ["OFF", "ON"],
            "SOUND": ["OFF", "ON"],
            "MUSIC": ["OFF", "ON"],
            "DIFFICULTY": ["EASY", "NORMAL", "HARD"],
        }
        
        # Current values (indexes into the settings arrays)
        self.current_values = {
            "FULLSCREEN": 1 if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN else 0,  # Check if already in fullscreen
            "SOUND": 1 if sound_enabled else 0,  # Based on global sound setting
            "MUSIC": 1 if music_enabled else 0,  # Based on global music setting
            "DIFFICULTY": 1,  # NORMAL by default
        }
        
        self.selected_option = 0
        self.background = None
        self.create_background()
        self.button_rects = []  # Store button rectangles for mouse interaction
        
        # Animation variables
        self.animation_progress = 0
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_duration = 500  # milliseconds
        
        # Toggle animation variables
        self.toggle_animation = False
        self.toggle_start_time = 0
        self.toggle_duration = 0.3  # seconds
        self.toggle_option = None
        self.toggle_old_value = None
        self.toggle_new_value = None
        self.toggle_rect = None
        
        # Store original window size for returning from fullscreen
        self.windowed_size = (screen_width, screen_height)
    
    def create_background(self):
        # Create a semi-transparent background
        self.background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        self.background.fill((0, 0, 0, 180))  # Semi-transparent black
        
        # Add some decorative elements
        for i in range(20):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 3)
            pygame.draw.circle(self.background, SLEEK_SILVER, (x, y), size)
    
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont(
            "arial", int(screen_height * 0.06), bold=True
        )
        self.font_medium = pygame.font.SysFont(
            "arial", int(screen_height * 0.04), bold=True
        )
        self.font_small = pygame.font.SysFont("arial", int(screen_height * 0.03))
        self.create_background()
    
    def draw(self):
        # Draw to the main screen
        self.draw_to_surface(self.screen)
        pygame.display.flip()
    
    def draw_pulsating_highlight(self, rect, color, thickness=2):
        """Draw a pulsating highlight around the given rectangle"""
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5  # 0.0 to 1.0
        
        # Calculate pulsating size and alpha
        expand = int(pulse * 6)
        alpha = int(128 + pulse * 127)  # 128-255
        
        # Create a surface for the highlight
        highlight_rect = rect.inflate(expand, expand)
        highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        
        # Draw the highlight with alpha
        highlight_color = (*color, alpha)
        pygame.draw.rect(highlight_surface, highlight_color, (0, 0, highlight_rect.width, highlight_rect.height), thickness, border_radius=5)
        
        # Draw the highlight
        self.screen.blit(highlight_surface, highlight_rect.topleft)
    
    def draw_to_surface(self, surface):
        # Draw background
        surface.blit(self.background, (0, 0))
        
        # Calculate animation progress
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.animation_start_time
        animation_progress = min(1.0, elapsed / self.animation_duration)
        
        # Draw title with animation
        title_text = self.font_large.render("SETTINGS", True, NEON_YELLOW)
        title_rect = title_text.get_rect(
            center=(self.screen_width // 2, self.screen_height * 0.2)
        )
        
        # Apply animation to title - slide in from top
        if animation_progress < 1.0:
            title_offset_y = int((1.0 - animation_progress) * -50)
            title_rect.y += title_offset_y
            title_alpha = int(animation_progress * 255)
            
            # Create a temporary surface for the title with alpha
            title_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
            title_surface.fill((0, 0, 0, 0))
            title_surface.blit(title_text, (0, 0))
            title_surface.set_alpha(title_alpha)
            
            # Draw the title with animation
            surface.blit(title_surface, title_rect)
        else:
            # Draw normal title
            surface.blit(title_text, title_rect)
        
        # Draw glow effect around title
        for offset in range(5, 0, -1):
            glow_rect = title_rect.copy()
            glow_rect.inflate_ip(offset * 2, offset * 2)
            pygame.draw.rect(
                surface,
                (
                    min(NEON_YELLOW[0], 255),
                    min(NEON_YELLOW[1] - offset * 10, 255),
                    min(NEON_YELLOW[2], 255),
                ),
                glow_rect,
                2,
                border_radius=10,
            )
        
        # Store button rects for mouse interaction
        self.button_rects = []
        
        # Draw settings options with staggered animation
        y_offset = self.screen_height * 0.35
        for i, (option, values) in enumerate(self.settings.items()):
            # Calculate option animation progress - staggered effect
            option_delay = 0.1 * i  # 100ms delay between each option
            option_progress = min(
                1.0, max(0, (animation_progress - option_delay) / 0.5)
            )
            
            # Draw option name
            if i == self.selected_option:
                color = ELECTRIC_PURPLE
                # Pulsating effect
                pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
                option_text = self.font_medium.render(f"> {option} <", True, color)
            else:
                color = WHITE
                option_text = self.font_medium.render(option, True, color)
            
            option_rect = option_text.get_rect(
                midright=(self.screen_width // 2 - 20, y_offset)
            )
            
            # Draw current value
            current_value = values[self.current_values[option]]
            value_text = self.font_medium.render(current_value, True, NEON_GREEN)
            value_rect = value_text.get_rect(
                midleft=(self.screen_width // 2 + 20, y_offset)
            )
            
            # Store button rect for mouse interaction
            button_rect = pygame.Rect(
                option_rect.left - 20,
                option_rect.top - 10,
                option_rect.width + value_rect.width + 60,
                option_rect.height + 20
            )
            self.button_rects.append(button_rect)
            
            # Apply animation to options - slide in from right
            if option_progress < 1.0:
                option_offset_x = int((1.0 - option_progress) * 100)
                option_rect.x += option_offset_x
                value_rect.x += option_offset_x
                option_alpha = int(option_progress * 255)
                
                # Create temporary surfaces with alpha
                option_surface = pygame.Surface(option_text.get_size(), pygame.SRCALPHA)
                option_surface.fill((0, 0, 0, 0))
                option_surface.blit(option_text, (0, 0))
                option_surface.set_alpha(option_alpha)
                
                value_surface = pygame.Surface(value_text.get_size(), pygame.SRCALPHA)
                value_surface.fill((0, 0, 0, 0))
                value_surface.blit(value_text, (0, 0))
                value_surface.set_alpha(option_alpha)
                
                # Draw with animation
                surface.blit(option_surface, option_rect)
                surface.blit(value_surface, value_rect)
            else:
                # Draw normal option and value
                surface.blit(option_text, option_rect)
                surface.blit(value_text, value_rect)
            
            if i == self.selected_option and option_progress >= 0.5:
                # Draw glowing border around selected option
                for offset in range(3, 0, -1):
                    glow_rect = button_rect.copy()
                    glow_rect.inflate_ip(offset * pulse, offset * pulse)
                    pygame.draw.rect(surface, color, glow_rect, 2, border_radius=5)
            
            # Draw left/right arrows
            if i == self.selected_option:
                # Left arrow
                left_arrow = self.font_medium.render("<", True, NEON_YELLOW)
                left_rect = left_arrow.get_rect(
                    midright=(value_rect.left - 10, y_offset)
                )
                surface.blit(left_arrow, left_rect)
                
                # Right arrow
                right_arrow = self.font_medium.render(">", True, NEON_YELLOW)
                right_rect = right_arrow.get_rect(
                    midleft=(value_rect.right + 10, y_offset)
                )
                surface.blit(right_arrow, right_rect)
            
            y_offset += 60
        
        # Draw back button
        back_text = self.font_medium.render("BACK", True, BRIGHT_RED)
        back_rect = back_text.get_rect(
            center=(self.screen_width // 2, self.screen_height * 0.8)
        )
        
        # Store back button rect
        back_button_rect = back_rect.copy()
        back_button_rect.inflate_ip(40, 20)
        self.button_rects.append(back_button_rect)
        
        # Apply animation to back button
        back_delay = 0.1 * len(self.settings)
        back_progress = min(1.0, max(0, (animation_progress - back_delay) / 0.5))
        
        if back_progress < 1.0:
            back_offset_y = int((1.0 - back_progress) * 50)
            back_rect.y += back_offset_y
            back_alpha = int(back_progress * 255)
            
            # Create a temporary surface for the back button with alpha
            back_surface = pygame.Surface(back_text.get_size(), pygame.SRCALPHA)
            back_surface.fill((0, 0, 0, 0))
            back_surface.blit(back_text, (0, 0))
            back_surface.set_alpha(back_alpha)
            
            # Draw the back button with animation
            surface.blit(back_surface, back_rect)
        else:
            # Draw normal back button
            surface.blit(back_text, back_rect)
        
        # Draw glowing border around back button if it's the last option
        if self.selected_option == len(self.settings) and back_progress >= 0.5:
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
            for offset in range(3, 0, -1):
                glow_rect = back_button_rect.copy()
                glow_rect.inflate_ip(offset * pulse, offset * pulse)
                pygame.draw.rect(surface, BRIGHT_RED, glow_rect, 2, border_radius=5)
        
        # Draw controls hint with fade-in animation
        controls_text = self.font_small.render(
            "UP/DOWN: Navigate | LEFT/RIGHT: Change | ENTER: Apply | ESC: Back",
            True,
            SLEEK_SILVER
        )
        controls_rect = controls_text.get_rect(
            center=(self.screen_width // 2, self.screen_height * 0.9)
        )
        
        # Apply animation to controls hint - fade in
        if animation_progress < 1.0:
            controls_alpha = int(animation_progress * 255)
            
            # Create a temporary surface for the controls with alpha
            controls_surface = pygame.Surface(controls_text.get_size(), pygame.SRCALPHA)
            controls_surface.fill((0, 0, 0, 0))
            controls_surface.blit(controls_text, (0, 0))
            controls_surface.set_alpha(controls_alpha)
            
            # Draw the controls with animation
            surface.blit(controls_surface, controls_rect)
        else:
            # Draw normal controls
            surface.blit(controls_text, controls_rect)
    
    def animate_option_toggle(self, option, old_value, new_value):
        """Animate transitioning between option values"""
        # Animation parameters
        duration = 0.3  # seconds
        start_time = time.time()
        
        # Calculate the position of the value text
        option_index = list(self.settings.keys()).index(option)
        y_offset = self.screen_height * 0.35 + option_index * 60
        value_rect = pygame.Rect(
            self.screen_width // 2 + 20,
            y_offset - 15,
            100,
            30
        )
        
        # Create surfaces for old and new values
        old_surface = self.font_medium.render(old_value, True, WHITE)
        new_surface = self.font_medium.render(new_value, True, WHITE)
        
        # Store original screen content
        original_bg = self.screen.copy()
        
        # Animation loop
        clock = pygame.time.Clock()
        while True:
            current_time = time.time()
            progress = min(1.0, (current_time - start_time) / duration)
            
            # Restore background
            self.screen.blit(original_bg, (0, 0))
            
            if progress < 0.5:
                # First half: fade out old value and slide up
                alpha = int(255 * (1 - progress * 2))
                offset_y = int(-20 * progress * 2)
                
                # Create a temporary surface with alpha
                temp_surface = pygame.Surface(old_surface.get_size(), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))
                temp_surface.blit(old_surface, (0, 0))
                temp_surface.set_alpha(alpha)
                
                # Draw with offset
                self.screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
            else:
                # Second half: fade in new value and slide down
                alpha = int(255 * ((progress - 0.5) * 2))
                offset_y = int(20 * (1 - (progress - 0.5) * 2))
                
                # Create a temporary surface with alpha
                temp_surface = pygame.Surface(new_surface.get_size(), pygame.SRCALPHA)
                temp_surface.fill((0, 0, 0, 0))
                temp_surface.blit(new_surface, (0, 0))
                temp_surface.set_alpha(alpha)
                
                # Draw with offset
                self.screen.blit(temp_surface, (value_rect.x, value_rect.y + offset_y))
            
            # Add some particle effects
            if random.random() < 0.3:
                # Create sparkle effect around the toggled option
                for _ in range(2):
                    sparkle_x = value_rect.centerx + random.uniform(-value_rect.width/2, value_rect.width/2)
                    sparkle_y = value_rect.centery + random.uniform(-value_rect.height/2, value_rect.height/2)
                    
                    # Get color based on the option
                    if option == "FULLSCREEN":
                        color = NEON_YELLOW
                    elif option == "SOUND":
                        color = NEON_GREEN
                    elif option == "MUSIC":
                        color = ELECTRIC_PURPLE
                    else:
                        color = SLEEK_SILVER
                    
                    # Create particles directly if particle system is available
                    try:
                        if hasattr(pygame.display.get_surface(), "_game"):
                            game = pygame.display.get_surface()._game
                            if hasattr(game, "particle_system"):
                                particle = Particle(
                                    x=sparkle_x,
                                    y=sparkle_y,
                                    color=color,
                                    size=random.uniform(1, 3),
                                    velocity=(random.uniform(-30, 30), random.uniform(-30, 30)),
                                    lifetime=random.uniform(0.3, 0.6),
                                    shrink=True,
                                    gravity=0
                                )
                                game.particle_system.add_particle(particle)
                    except:
                        pass  # Silently fail if particle system is not accessible
            
            pygame.display.flip()
            
            # Check if animation is complete
            if progress >= 1.0:
                break
            
            # Handle events during animation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # Cap the frame rate
            clock.tick(60)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            # Handle music end event - play next song in playlist
            elif event.type == pygame.USEREVENT + 1:
                if hasattr(self, "_advance_playlist"):
                    self._advance_playlist()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "BACK"
                elif event.key == pygame.K_UP:
                    self.selected_option = max(0, self.selected_option - 1)
                    # Play menu navigation sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_navigate.play()
                        except:
                            pass
                elif event.key == pygame.K_DOWN:
                    self.selected_option = min(len(self.settings), self.selected_option + 1)
                    # Play menu navigation sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_navigate.play()
                        except:
                            pass
                elif event.key == pygame.K_LEFT:
                    if self.selected_option < len(self.settings):
                        option = list(self.settings.keys())[self.selected_option]
                        values = self.settings[option]
                        old_value = values[self.current_values[option]]
                        self.current_values[option] = (self.current_values[option] - 1) % len(values)
                        new_value = values[self.current_values[option]]
                        
                        # Play menu navigation sound
                        if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                            try:
                                sound_menu_navigate.play()
                            except:
                                pass
                        
                        # Animate the option toggle
                        self.animate_option_toggle(option, old_value, new_value)
                        
                        # Apply the setting
                        result = self.apply_setting(option)
                        if result:
                            return result
                elif event.key == pygame.K_RIGHT:
                    if self.selected_option < len(self.settings):
                        option = list(self.settings.keys())[self.selected_option]
                        values = self.settings[option]
                        old_value = values[self.current_values[option]]
                        self.current_values[option] = (self.current_values[option] + 1) % len(values)
                        new_value = values[self.current_values[option]]
                        
                        # Play menu navigation sound
                        if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                            try:
                                sound_menu_navigate.play()
                            except:
                                pass
                        
                        # Animate the option toggle
                        self.animate_option_toggle(option, old_value, new_value)
                        
                        # Apply the setting
                        result = self.apply_setting(option)
                        if result:
                            return result
                elif event.key == pygame.K_RETURN:
                    # Play menu selection sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_select.play()
                        except:
                            pass
                    
                    # If back button is selected
                    if self.selected_option == len(self.settings):
                        return "BACK"
                    else:
                        # Apply the selected setting
                        option = list(self.settings.keys())[self.selected_option]
                        result = self.apply_setting(option)
                        if result:
                            return result
            # Handle mouse movement for hover effect
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                # Check if mouse is over any option
                for i, button_rect in enumerate(self.button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        new_selection = i if i < len(self.settings) else len(self.settings)
                        if self.selected_option != new_selection:
                            self.selected_option = new_selection
                            # Play menu navigation sound
                            if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                                try:
                                    sound_menu_navigate.play()
                                except:
                                    pass
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if any option was clicked
                    for i, button_rect in enumerate(self.button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            # Play menu selection sound
                            if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                                try:
                                    sound_menu_select.play()
                                except:
                                    pass
                            
                            # If it's the back button
                            if i == len(self.settings):
                                return "BACK"
                            else:
                                # Toggle the setting
                                option = list(self.settings.keys())[i]
                                values = self.settings[option]
                                old_value = values[self.current_values[option]]
                                self.current_values[option] = (self.current_values[option] + 1) % len(values)
                                new_value = values[self.current_values[option]]
                                
                                # Animate the option toggle
                                self.animate_option_toggle(option, old_value, new_value)
                                
                                # Apply the setting
                                result = self.apply_setting(option)
                                if result:
                                    return result
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
                return "RESIZE"
        return None
    
    def apply_setting(self, option):
        # Apply the setting change
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
        
        if option == "FULLSCREEN":
            if self.current_values[option] == 1:  # ON
                # Save current window size before going fullscreen
                self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
                
                # Get the display info for proper fullscreen resolution
                info = pygame.display.Info()
                SCREEN_WIDTH = info.current_w
                SCREEN_HEIGHT = info.current_h
                
                # Set fullscreen mode
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), 
                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
                
                # Update menu dimensions
                self.screen_width = SCREEN_WIDTH
                self.screen_height = SCREEN_HEIGHT
                
                # Update scale factors
                SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                
                # Update fonts for new screen size
                self.font_large = get_font(int(self.screen_height * 0.06), bold=True)
                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)
                self.font_small = get_font(int(self.screen_height * 0.03))
                
                # Recreate background for new dimensions
                self.create_background()
                
                print(f"Switched to fullscreen mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                return "FULLSCREEN_CHANGED"
            else:  # OFF
                # Restore previous window size
                if hasattr(self, 'windowed_size'):
                    window_width, window_height = self.windowed_size
                else:
                    # Default size if no previous size is stored
                    window_width, window_height = 1280, 720
                
                # Update global variables
                SCREEN_WIDTH = window_width
                SCREEN_HEIGHT = window_height
                
                # Set windowed mode
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), 
                    pygame.RESIZABLE
                )
                
                # Update menu dimensions
                self.screen_width = SCREEN_WIDTH
                self.screen_height = SCREEN_HEIGHT
                
                # Update scale factors
                SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                
                # Update fonts for new screen size
                self.font_large = get_font(int(self.screen_height * 0.06), bold=True)
                self.font_medium = get_font(int(self.screen_height * 0.04), bold=True)
                self.font_small = get_font(int(self.screen_height * 0.03))
                
                # Recreate background for new dimensions
                self.create_background()
                
                print(f"Switched to windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                return "FULLSCREEN_CHANGED"
        elif option == "SOUND":
            # Toggle sound
            global sound_enabled
            sound_enabled = bool(self.current_values[option])
            print(f"Sound {'enabled' if sound_enabled else 'disabled'}")
            return None
        elif option == "MUSIC":
            # Toggle music
            global music_enabled
            music_enabled = bool(self.current_values[option])
            print(f"Music {'enabled' if music_enabled else 'disabled'}")
            return None

        # Other settings would be applied here
        print(f"Setting {option} changed to {self.settings[option][self.current_values[option]]}")
        return None


class PauseMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = get_font(int(screen_height * 0.06), bold=True)
        self.font_medium = get_font(int(screen_height * 0.04), bold=True)
        self.font_small = get_font(int(screen_height * 0.03))
        self.options = ["RESUME", "OPTIONS", "MAIN MENU", "EXIT"]
        self.selected_option = 0
        self.background = None
        self.create_background()
        self.button_rects = []  # Store button rectangles for mouse interaction

        # Animation variables
        self.animation_progress = 0
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_duration = 500  # milliseconds
        
        # Store original window size for returning from fullscreen
        self.windowed_size = (screen_width, screen_height)

    def create_background(self):
        # Create a semi-transparent background
        self.background = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        self.background.fill((0, 0, 0, 180))  # Semi-transparent black

        # Add some decorative elements
        for i in range(20):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 3)
            pygame.draw.circle(self.background, SLEEK_SILVER, (x, y), size)

    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.SysFont(
            "arial", int(screen_height * 0.06), bold=True
        )
        self.font_medium = pygame.font.SysFont(
            "arial", int(screen_height * 0.04), bold=True
        )
        self.font_small = pygame.font.SysFont("arial", int(screen_height * 0.03))
        self.create_background()

    def draw(self):
        # Draw to the main screen
        self.draw_to_surface(self.screen)
        pygame.display.flip()

    def draw_to_surface(self, surface):
        # Draw background
        surface.blit(self.background, (0, 0))

        # Calculate animation progress
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.animation_start_time
        animation_progress = min(1.0, elapsed / self.animation_duration)

        # Draw title with animation
        title_text = self.font_large.render("PAUSED", True, NEON_YELLOW)
        title_rect = title_text.get_rect(
            center=(self.screen_width // 2, self.screen_height * 0.2)
        )

        # Apply animation to title - slide in from top
        if animation_progress < 1.0:
            title_offset_y = int((1.0 - animation_progress) * -50)
            title_rect.y += title_offset_y
            title_alpha = int(animation_progress * 255)

            # Create a temporary surface for the title with alpha
            title_surface = pygame.Surface(title_text.get_size(), pygame.SRCALPHA)
            title_surface.fill((0, 0, 0, 0))
            title_surface.blit(title_text, (0, 0))
            title_surface.set_alpha(title_alpha)

            # Draw the title with animation
            surface.blit(title_surface, title_rect)
        else:
            # Draw normal title
            surface.blit(title_text, title_rect)

        # Draw glow effect around title
        for offset in range(5, 0, -1):
            glow_rect = title_rect.copy()
            glow_rect.inflate_ip(offset * 2, offset * 2)
            pygame.draw.rect(
                surface,
                (
                    min(NEON_YELLOW[0], 255),
                    min(NEON_YELLOW[1] - offset * 10, 255),
                    min(NEON_YELLOW[2], 255),
                ),
                glow_rect,
                2,
                border_radius=10,
            )

        # Store button rects for mouse interaction
        self.button_rects = []

        # Draw menu options with staggered animation
        for i, option in enumerate(self.options):
            # Calculate option animation progress - staggered effect
            option_delay = 0.1 * i  # 100ms delay between each option
            option_progress = min(
                1.0, max(0, (animation_progress - option_delay) / 0.5)
            )

            if i == self.selected_option:
                color = ELECTRIC_PURPLE
                # Pulsating effect
                pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2
                text = self.font_medium.render(f"> {option} <", True, color)
            else:
                color = WHITE
                text = self.font_medium.render(option, True, color)

            rect = text.get_rect(
                center=(
                    self.screen_width // 2,
                    self.screen_height * 0.4 + i * self.screen_height * 0.08,
                )
            )

            # Store button rect for mouse interaction
            button_rect = rect.copy()
            button_rect.inflate_ip(40, 20)  # Make clickable area slightly larger
            self.button_rects.append(button_rect)

            # Apply animation to options - slide in from right
            if option_progress < 1.0:
                option_offset_x = int((1.0 - option_progress) * 100)
                rect.x += option_offset_x
                option_alpha = int(option_progress * 255)

                # Create a temporary surface for the option with alpha
                option_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
                option_surface.fill((0, 0, 0, 0))
                option_surface.blit(text, (0, 0))
                option_surface.set_alpha(option_alpha)

                # Draw the option with animation
                surface.blit(option_surface, rect)
            else:
                # Draw normal option
                surface.blit(text, rect)

            if i == self.selected_option and option_progress >= 0.5:
                # Draw glowing border around selected option
                button_rect = rect.copy()
                button_rect.inflate_ip(20, 10)
                for offset in range(3, 0, -1):
                    glow_rect = button_rect.copy()
                    glow_rect.inflate_ip(offset * pulse, offset * pulse)
                    pygame.draw.rect(surface, color, glow_rect, 2, border_radius=5)

        # Draw controls hint with fade-in animation
        controls_text = self.font_small.render(
            "UP/DOWN: Navigate | ENTER: Select | ESC: Resume", True, SLEEK_SILVER
        )
        controls_rect = controls_text.get_rect(
            center=(self.screen_width // 2, self.screen_height * 0.85)
        )

        # Apply animation to controls hint - fade in
        if animation_progress < 1.0:
            controls_alpha = int(animation_progress * 255)

            # Create a temporary surface for the controls with alpha
            controls_surface = pygame.Surface(controls_text.get_size(), pygame.SRCALPHA)
            controls_surface.fill((0, 0, 0, 0))
            controls_surface.blit(controls_text, (0, 0))
            controls_surface.set_alpha(controls_alpha)

            # Draw the controls with animation
            surface.blit(controls_surface, controls_rect)
        else:
            # Draw normal controls
            surface.blit(controls_text, controls_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "EXIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "RESUME"
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(
                        self.options
                    )
                    # Play menu navigation sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_navigate.play()
                        except:
                            pass
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(
                        self.options
                    )
                    # Play menu navigation sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_navigate.play()
                        except:
                            pass
                elif event.key == pygame.K_RETURN:
                    # Play menu selection sound
                    if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                        try:
                            sound_menu_select.play()
                        except:
                            pass
                    return self.options[self.selected_option]
            # Handle mouse movement for hover effect
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                # Check if mouse is over any option
                for i, option in enumerate(self.options):
                    # Calculate option position
                    option_y = self.screen_height * 0.4 + i * self.screen_height * 0.08
                    option_rect = pygame.Rect(
                        self.screen_width // 2 - 100,  # Approximate width
                        option_y - 20,                 # Approximate height
                        200,                           # Width of clickable area
                        40                             # Height of clickable area
                    )
                    if option_rect.collidepoint(mouse_pos):
                        if self.selected_option != i:
                            self.selected_option = i
                            # Play menu navigation sound
                            if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                                try:
                                    sound_menu_navigate.play()
                                except:
                                    pass
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if any option was clicked
                    for i, option in enumerate(self.options):
                        # Calculate option position
                        option_y = self.screen_height * 0.4 + i * self.screen_height * 0.08
                        option_rect = pygame.Rect(
                            self.screen_width // 2 - 100,  # Approximate width
                            option_y - 20,                 # Approximate height
                            200,                           # Width of clickable area
                            40                             # Height of clickable area
                        )
                        if option_rect.collidepoint(mouse_pos):
                            # Play menu selection sound
                            if sound_enabled and hasattr(pygame, "mixer") and pygame.mixer.get_init():
                                try:
                                    sound_menu_select.play()
                                except:
                                    pass
                            return self.options[i]
            if event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
                return "RESIZE"
        return None

    def apply_setting(self, option):
        # Apply the setting change
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
        
        if option == "FULLSCREEN":
            if self.current_values[option] == 1:  # ON
                # Save current window size before going fullscreen
                self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
                
                # Get the display info for proper fullscreen resolution
                info = pygame.display.Info()
                SCREEN_WIDTH = info.current_w
                SCREEN_HEIGHT = info.current_h
                
                # Set fullscreen mode
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), 
                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
                
                # Update menu dimensions
                self.screen_width = SCREEN_WIDTH
                self.screen_height = SCREEN_HEIGHT
                
                # Update scale factors
                SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                
                # Update fonts for new screen size
                self.font_large = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.06), bold=True
                )
                self.font_medium = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.04), bold=True
                )
                self.font_small = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.03)
                )
                
                print(f"Switched to fullscreen mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                return "FULLSCREEN_CHANGED"
            else:  # OFF
                # Restore previous window size
                if hasattr(self, 'windowed_size'):
                    window_width, window_height = self.windowed_size
                else:
                    # Default size if no previous size is stored
                    window_width, window_height = 1280, 720
                
                # Update global variables
                SCREEN_WIDTH = window_width
                SCREEN_HEIGHT = window_height
                
                # Set windowed mode
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), 
                    pygame.RESIZABLE
                )
                
                # Update menu dimensions
                self.screen_width = SCREEN_WIDTH
                self.screen_height = SCREEN_HEIGHT
                
                # Update scale factors
                SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                
                # Recalculate lane positions
                LANE_WIDTH = SCREEN_WIDTH // 6
                LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                
                # Update fonts for new screen size
                self.font_large = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.06), bold=True
                )
                self.font_medium = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.04), bold=True
                )
                self.font_small = pygame.font.SysFont(
                    "arial", int(self.screen_height * 0.03)
                )
                
                print(f"Switched to windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                return "FULLSCREEN_CHANGED"
        elif option == "SOUND":
            # Toggle sound
            global sound_enabled
            sound_enabled = bool(self.current_values[option])
            print(f"Sound {'enabled' if sound_enabled else 'disabled'}")
            return None
        elif option == "MUSIC":
            # Toggle music
            global music_enabled
            music_enabled = bool(self.current_values[option])
            print(f"Music {'enabled' if music_enabled else 'disabled'}")
            return None

        # Other settings would be applied here
        print(f"Setting {option} changed to {self.settings[option][self.current_values[option]]}")
        return None


class TransitionEffect:
    """Class to handle smooth transitions between screens"""

    def __init__(self, screen, transition_type="fade"):
        self.screen = screen
        self.transition_type = transition_type
        self.progress = 0
        self.running = False
        self.start_time = 0
        self.duration = TRANSITION_SPEED
        self.callback = None
        self.from_surface = None
        self.to_surface = None
        self.direction = "out"  # "in" or "out"
        self.last_update_time = 0
        self.transition_color = BLACK  # Default transition color
        
        # Store original screen content
        if screen:
            self.screen_copy = screen.copy()

    def start(self, direction="out", duration=None, callback=None, transition_type=None, color=None):
        """Start a transition effect with optional parameters"""
        self.direction = direction
        self.progress = 0
        self.running = True
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.duration = duration if duration is not None else TRANSITION_SPEED
        self.callback = callback
        
        # Update transition type if specified
        if transition_type:
            self.transition_type = transition_type
            
        # Update transition color if specified
        if color:
            self.transition_color = color

        # Capture current screen state
        if direction == "out":
            self.from_surface = self.screen.copy()
        
        # Store original screen content
        self.screen_copy = self.screen.copy()

    def update(self, dt=None):
        """Update transition progress"""
        if not self.running:
            return False

        current_time = time.time()

        # If dt is not provided, calculate it
        if dt is None:
            dt = current_time - self.last_update_time

        self.last_update_time = current_time

        # Calculate progress (0 to 1)
        elapsed = current_time - self.start_time
        self.progress = min(elapsed / self.duration, 1.0)

        # If transition is complete
        if self.progress >= 1.0:
            self.running = False
            if self.callback:
                self.callback()
            return False

        return True

    def draw(self):
        """Draw the transition effect"""
        if not self.running:
            return

        if self.transition_type == "fade":
            self._draw_fade()
        elif self.transition_type == "slide_left":
            self._draw_slide("left")
        elif self.transition_type == "slide_right":
            self._draw_slide("right")
        elif self.transition_type == "slide_up":
            self._draw_slide("up")
        elif self.transition_type == "slide_down":
            self._draw_slide("down")
        elif self.transition_type == "zoom":
            self._draw_zoom()
        elif self.transition_type == "pixelate":
            self._draw_pixelate()
        elif self.transition_type == "radial":
            self._draw_radial()
        elif self.transition_type == "blinds":
            self._draw_blinds()
        elif self.transition_type == "rotate":
            self._draw_rotate()

    def _draw_fade(self):
        """Fade transition effect"""
        if self.direction == "out":
            # Fade out: from opaque to transparent
            alpha = int(255 * self.progress)
            overlay = pygame.Surface(
                (self.screen.get_width(), self.screen.get_height())
            )
            overlay.fill(self.transition_color)
            overlay.set_alpha(alpha)
            self.screen.blit(self.from_surface, (0, 0))
            self.screen.blit(overlay, (0, 0))
        else:
            # Fade in: from transparent to opaque
            alpha = int(255 * (1 - self.progress))
            overlay = pygame.Surface(
                (self.screen.get_width(), self.screen.get_height())
            )
            overlay.fill(self.transition_color)
            overlay.set_alpha(alpha)
            if self.to_surface:
                self.screen.blit(self.to_surface, (0, 0))
            self.screen.blit(overlay, (0, 0))

    def _draw_slide(self, direction):
        """Slide transition effect"""
        width, height = self.screen.get_width(), self.screen.get_height()

        if self.from_surface is None:
            return

        if direction == "left":
            offset = (
                int(-width * self.progress)
                if self.direction == "out"
                else int(width * (1 - self.progress))
            )
            self.screen.blit(self.from_surface, (offset, 0))
            if self.to_surface and self.direction == "in":
                self.screen.blit(self.to_surface, (offset - width, 0))
        elif direction == "right":
            offset = (
                int(width * self.progress)
                if self.direction == "out"
                else int(-width * (1 - self.progress))
            )
            self.screen.blit(self.from_surface, (offset, 0))
            if self.to_surface and self.direction == "in":
                self.screen.blit(self.to_surface, (offset + width, 0))
        elif direction == "up":
            offset = (
                int(-height * self.progress)
                if self.direction == "out"
                else int(height * (1 - self.progress))
            )
            self.screen.blit(self.from_surface, (0, offset))
            if self.to_surface and self.direction == "in":
                self.screen.blit(self.to_surface, (0, offset - height))
        elif direction == "down":
            offset = (
                int(height * self.progress)
                if self.direction == "out"
                else int(-height * (1 - self.progress))
            )
            self.screen.blit(self.from_surface, (0, offset))
            if self.to_surface and self.direction == "in":
                self.screen.blit(self.to_surface, (0, offset + height))

    def _draw_zoom(self):
        """Zoom transition effect"""
        width, height = self.screen.get_width(), self.screen.get_height()

        if self.direction == "out":
            # Zoom out
            scale = 1 - self.progress * 0.5
            scaled_width = int(width * scale)
            scaled_height = int(height * scale)

            scaled_surface = pygame.transform.smoothscale(
                self.from_surface, (scaled_width, scaled_height)
            )
            x = (width - scaled_width) // 2
            y = (height - scaled_height) // 2

            self.screen.fill(self.transition_color)
            self.screen.blit(scaled_surface, (x, y))

            # Add fade effect
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((*self.transition_color, int(255 * self.progress)))
            self.screen.blit(overlay, (0, 0))
        else:
            # Zoom in
            scale = 0.5 + self.progress * 0.5
            scaled_width = int(width * scale)
            scaled_height = int(height * scale)

            if self.to_surface:
                scaled_surface = pygame.transform.smoothscale(
                    self.to_surface, (scaled_width, scaled_height)
                )
                x = (width - scaled_width) // 2
                y = (height - scaled_height) // 2

                self.screen.fill(self.transition_color)
                self.screen.blit(scaled_surface, (x, y))

                # Add fade effect
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((*self.transition_color, int(255 * (1 - self.progress))))
                self.screen.blit(overlay, (0, 0))
                
    def _draw_pixelate(self):
        """Pixelate transition effect"""
        width, height = self.screen.get_width(), self.screen.get_height()
        
        if self.from_surface is None:
            return
            
        if self.direction == "out":
            # Calculate pixel size based on progress
            pixel_size = int(1 + self.progress * 20)  # 1 to 21 pixels
            
            # Create a smaller version of the screen
            small_width = max(1, width // pixel_size)
            small_height = max(1, height // pixel_size)
            
            # Scale down and then back up to create pixelation
            small_surface = pygame.transform.scale(self.from_surface, (small_width, small_height))
            pixelated = pygame.transform.scale(small_surface, (width, height))
            
            self.screen.blit(pixelated, (0, 0))
            
            # Add fade effect
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((*self.transition_color, int(150 * self.progress)))
            self.screen.blit(overlay, (0, 0))
        else:
            # Calculate pixel size based on progress
            pixel_size = int(20 * (1 - self.progress) + 1)  # 21 to 1 pixels
            
            if self.to_surface:
                # Scale down and then back up to create pixelation
                small_width = max(1, width // pixel_size)
                small_height = max(1, height // pixel_size)
                
                small_surface = pygame.transform.scale(self.to_surface, (small_width, small_height))
                pixelated = pygame.transform.scale(small_surface, (width, height))
                
                self.screen.blit(pixelated, (0, 0))
                
                # Add fade effect
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((*self.transition_color, int(150 * (1 - self.progress))))
                self.screen.blit(overlay, (0, 0))
                
    def _draw_radial(self):
        """Radial wipe transition effect"""
        width, height = self.screen.get_width(), self.screen.get_height()
        
        if self.from_surface is None:
            return
            
        # Create mask surface
        mask = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Calculate center and max radius
        center_x, center_y = width // 2, height // 2
        max_radius = math.sqrt(width**2 + height**2) / 2
        
        if self.direction == "out":
            # Calculate radius based on progress
            radius = max_radius * self.progress
            
            # Draw circle on mask
            pygame.draw.circle(mask, (0, 0, 0, 255), (center_x, center_y), int(radius))
            
            # Draw original surface
            self.screen.blit(self.from_surface, (0, 0))
            
            # Draw overlay with hole
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((*self.transition_color, 255))
            overlay.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            self.screen.blit(overlay, (0, 0))
        else:
            # Calculate radius based on progress
            radius = max_radius * (1 - self.progress)
            
            if self.to_surface:
                # Draw destination surface
                self.screen.blit(self.to_surface, (0, 0))
                
                # Draw circle on mask
                pygame.draw.circle(mask, (0, 0, 0, 255), (center_x, center_y), int(radius))
                
                # Draw overlay with hole
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((*self.transition_color, 255))
                overlay.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                self.screen.blit(overlay, (0, 0))
                
    def _draw_blinds(self):
        """Venetian blinds transition effect"""
        width, height = self.screen.get_width(), self.screen.get_height()
        
        if self.from_surface is None:
            return
            
        # Number of blinds
        num_blinds = 12
        blind_height = height // num_blinds
        
        if self.direction == "out":
            # Draw original surface
            self.screen.blit(self.from_surface, (0, 0))
            
            # Draw blinds
            for i in range(num_blinds):
                blind_y = i * blind_height
                blind_width = int(width * self.progress)
                
                # Alternate direction for each blind
                if i % 2 == 0:
                    blind_x = 0
                else:
                    blind_x = width - blind_width
                    
                pygame.draw.rect(
                    self.screen,
                    self.transition_color,
                    (blind_x, blind_y, blind_width, blind_height)
                )
        else:
            if self.to_surface:
                # Draw destination surface
                self.screen.blit(self.to_surface, (0, 0))
                
                # Draw blinds
                for i in range(num_blinds):
                    blind_y = i * blind_height
                    blind_width = int(width * (1 - self.progress))
                    
                    # Alternate direction for each blind
                    if i % 2 == 0:
                        blind_x = 0
                    else:
                        blind_x = width - blind_width
                        
                    pygame.draw.rect(
                        self.screen,
                        self.transition_color,
                        (blind_x, blind_y, blind_width, blind_height)
                    )
                    
    def _draw_rotate(self):
        """Rotation transition effect"""
        width, height = self.screen.get_width(), self.screen.get_height()
        
        if self.from_surface is None:
            return
            
        if self.direction == "out":
            # Calculate rotation angle and scale
            angle = 90 * self.progress  # Rotate up to 90 degrees
            scale = 1 - 0.5 * self.progress  # Scale down to 50%
            
            # Create rotated and scaled surface
            rotated = pygame.transform.rotozoom(self.from_surface, angle, scale)
            
            # Position in center
            rot_rect = rotated.get_rect(center=(width//2, height//2))
            
            # Fill background
            self.screen.fill(self.transition_color)
            
            # Draw rotated surface
            self.screen.blit(rotated, rot_rect)
            
            # Add fade effect
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((*self.transition_color, int(150 * self.progress)))
            self.screen.blit(overlay, (0, 0))
        else:
            if self.to_surface:
                # Calculate rotation angle and scale
                angle = 90 * (1 - self.progress)  # Rotate from 90 to 0 degrees
                scale = 0.5 + 0.5 * self.progress  # Scale up from 50% to 100%
                
                # Create rotated and scaled surface
                rotated = pygame.transform.rotozoom(self.to_surface, angle, scale)
                
                # Position in center
                rot_rect = rotated.get_rect(center=(width//2, height//2))
                
                # Fill background
                self.screen.fill(self.transition_color)
                
                # Draw rotated surface
                self.screen.blit(rotated, rot_rect)
                
                # Add fade effect
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                overlay.fill((*self.transition_color, int(150 * (1 - self.progress))))
                self.screen.blit(overlay, (0, 0))

    def set_to_surface(self, surface):
        """Set the destination surface for transitions"""
        self.to_surface = surface


class PromptSystem:
    """Class to handle in-game prompts and tutorials"""

    def __init__(self, screen):
        self.screen = screen
        self.prompts = {
            "welcome": {
                "text": "Welcome to Car Racing! Use LEFT and RIGHT arrows to change lanes.",
                "duration": 5.0,
                "shown": False,
            },
            "powerup_boost": {
                "text": "You got a BOOST power-up! Your speed is increased for a short time.",
                "duration": 3.0,
                "shown": False,
            },
            "powerup_shield": {
                "text": "You got a SHIELD power-up! You're protected from crashes.",
                "duration": 3.0,
                "shown": False,
            },
            "powerup_magnet": {
                "text": "You got a MAGNET power-up! Coins will be attracted to your car.",
                "duration": 3.0,
                "shown": False,
            },
            "powerup_slow_mo": {
                "text": "You got a SLOW-MO power-up! Time is slowed down.",
                "duration": 3.0,
                "shown": False,
            },
            "combo": {
                "text": "Nice! Keep collecting items to increase your combo multiplier!",
                "duration": 3.0,
                "shown": False,
            },
            "boost_energy": {
                "text": "Press SPACE to use your boost energy when the meter is filled!",
                "duration": 3.0,
                "shown": False,
            },
            "mission_complete": {
                "text": "Mission complete! Get ready for the next challenge.",
                "duration": 3.0,
                "shown": False,
            },
        }
        self.active_prompts = []
        self.font = get_font(scale_value(24), bold=True)
        self.small_font = get_font(scale_value(18))

    def show_prompt(self, prompt_id, custom_text=None):
        """Show a specific prompt"""
        if prompt_id in self.prompts and not self.prompts[prompt_id]["shown"]:
            prompt = self.prompts[prompt_id].copy()
            if custom_text:
                prompt["text"] = custom_text
            prompt["start_time"] = time.time()
            prompt["alpha"] = 0  # Start with transparent
            prompt["fade_in"] = True
            prompt["fade_out"] = False
            self.active_prompts.append(prompt)
            self.prompts[prompt_id]["shown"] = True
            return True
        return False

    def show_custom_prompt(self, text, duration=3.0):
        """Show a custom prompt with specified text and duration"""
        prompt = {
            "text": text,
            "duration": duration,
            "start_time": time.time(),
            "alpha": 0,
            "fade_in": True,
            "fade_out": False,
            "shown": False,
        }
        self.active_prompts.append(prompt)
        return True

    def update(self):
        """Update all active prompts"""
        current_time = time.time()

        # Process each active prompt
        for prompt in self.active_prompts[:]:
            elapsed = current_time - prompt["start_time"]

            # Handle fade in
            if prompt["fade_in"]:
                prompt["alpha"] = min(
                    255, int(elapsed * 510)
                )  # Fade in over 0.5 seconds
                if prompt["alpha"] >= 255:
                    prompt["fade_in"] = False

            # Check if it's time to start fading out
            if not prompt["fade_out"] and elapsed > prompt["duration"] - 0.5:
                prompt["fade_out"] = True

            # Handle fade out
            if prompt["fade_out"]:
                remaining = prompt["duration"] - elapsed
                prompt["alpha"] = max(
                    0, int(remaining * 510)
                )  # Fade out over 0.5 seconds

            # Remove expired prompts
            if elapsed > prompt["duration"]:
                self.active_prompts.remove(prompt)

    def draw(self):
        """Draw all active prompts"""
        if not self.active_prompts:
            return

        # Calculate positions for stacked prompts
        y_offset = scale_value(100)

        for prompt in self.active_prompts:
            # Create text surfaces
            text_surface = self.font.render(prompt["text"], True, PROMPT_TEXT)
            text_rect = text_surface.get_rect(
                center=(self.screen.get_width() // 2, y_offset)
            )

            # Create background surface with alpha
            padding = scale_value(20)
            bg_rect = pygame.Rect(
                text_rect.left - padding,
                text_rect.top - padding // 2,
                text_rect.width + padding * 2,
                text_rect.height + padding,
            )

            # Create a surface with per-pixel alpha
            bg_surface = pygame.Surface(
                (bg_rect.width, bg_rect.height), pygame.SRCALPHA
            )

            # Fill with semi-transparent background
            bg_color = (
                PROMPT_BG[0],
                PROMPT_BG[1],
                PROMPT_BG[2],
                min(180, prompt["alpha"]),
            )
            bg_surface.fill(bg_color)

            # Draw border with alpha
            border_color = (
                PROMPT_BORDER[0],
                PROMPT_BORDER[1],
                PROMPT_BORDER[2],
                prompt["alpha"],
            )
            pygame.draw.rect(
                bg_surface,
                border_color,
                (0, 0, bg_rect.width, bg_rect.height),
                2,
                border_radius=10,
            )

            # Apply alpha to text surface
            text_surface.set_alpha(prompt["alpha"])

            # Draw background and text
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(text_surface, text_rect)

            # Add "Press X to dismiss" text for longer prompts
            if prompt["duration"] > 3.0:
                dismiss_text = self.small_font.render(
                    "Press X to dismiss", True, PROMPT_HIGHLIGHT
                )
                dismiss_text.set_alpha(prompt["alpha"])
                dismiss_rect = dismiss_text.get_rect(
                    center=(self.screen.get_width() // 2, bg_rect.bottom - 10)
                )
                self.screen.blit(dismiss_text, dismiss_rect)

            # Increment y_offset for next prompt
            y_offset += bg_rect.height + scale_value(10)

    def handle_input(self, event):
        """Handle input for dismissing prompts"""
        # Don't consume scroll events
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 4 or event.button == 5):
            return False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            if self.active_prompts:
                # Start fade out for all prompts
                for prompt in self.active_prompts:
                    prompt["fade_out"] = True
                    # Make fade out faster
                    remaining_time = 0.5
                    prompt["duration"] = (
                        time.time() - prompt["start_time"] + remaining_time
                    )
                return True
        return False

    def reset(self):
        """Reset all prompts to be shown again"""
        for prompt_id in self.prompts:
            self.prompts[prompt_id]["shown"] = False
        self.active_prompts = []

    def resize(self):
        """Update font sizes after window resize"""
        self.font = get_font(scale_value(24), bold=True)
        self.small_font = get_font(scale_value(18))


class Game:
    def __init__(self):
        try:
            # Create a fullscreen window with error handling
            info = pygame.display.Info()
            SCREEN_WIDTH = info.current_w
            SCREEN_HEIGHT = info.current_h
            
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
            )
            pygame.display.set_caption("Car Racing Game")
            self.clock = pygame.time.Clock()
            
            # Music player has been removed, we'll handle music directly
            self.music_player = None
            
            # Track window state
            self.is_maximized = True
            self.pre_maximize_size = (1280, 720)  # Default windowed size

            # Set up fonts with scaling
            self.font = get_font(scale_value(36))
            self.font_large = get_font(scale_value(48), bold=True)
            self.font_medium = get_font(scale_value(36), bold=True)
            self.font_small = get_font(scale_value(24))

            self.particle_system = ParticleSystem()
            self.highscore_manager = HighScoreManager()

            # Initialize prompt system
            self.prompt_system = PromptSystem(self.screen)

            # Initialize transition effects
            self.transition = TransitionEffect(self.screen, "fade")
            self.transitioning = False

            # Day-night cycle variables
            self.cycle_time = 0
            self.day_phase = 0  # 0 = day, 0.25 = sunset, 0.5 = night, 0.75 = sunrise
            self.stars = []
            self.generate_stars()
            
            # Sparkle animation for menu background
            self.sparkles = []
            self.generate_sparkles(100)  # Create 100 sparkles

            # Create sounds directory if it doesn't exist
            if not os.path.exists("sounds"):
                os.makedirs("sounds")
                print("Created sounds directory")

            # Initialize sound effects
            self.init_sounds()

            self.reset_game()

            # Register event handler for window resize
            pygame.event.set_allowed(
                [
                    pygame.QUIT,
                    pygame.KEYDOWN,
                    pygame.KEYUP,
                    pygame.MOUSEBUTTONDOWN,
                    pygame.VIDEORESIZE,
                ]
            )

        except Exception as e:
            print(f"Error initializing game: {e}")
            traceback.print_exc()
            pygame.quit()
            sys.exit(1)

    def handle_resize(self, width, height):
        """Handle window resize event"""
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS

        try:
            print(f"Handling resize event: {width}x{height}")
            
            # Get display info to detect maximize
            info = pygame.display.Info()
            desktop_width, desktop_height = info.current_w, info.current_h
            
            # Check if this is likely a maximize event
            # On most systems, maximized window will be close to desktop size
            is_maximize_event = (width > desktop_width * 0.9 and height > desktop_height * 0.9)
            
            if is_maximize_event and not self.is_maximized:
                print("Maximize button detected - switching to fullscreen")
                # Store current window size before going fullscreen
                self.pre_maximize_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
                self.is_maximized = True
                
                # Switch to fullscreen
                self.toggle_fullscreen()
                return
            
            # Store current display surface to restore if needed
            try:
                old_surface = pygame.display.get_surface().copy()
            except:
                old_surface = None
                print("Could not copy old surface")
            
            # Update screen dimensions
            SCREEN_WIDTH = width
            SCREEN_HEIGHT = height
            print(f"Updated screen dimensions: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

            # Update scale factors
            SCALE_X = SCREEN_WIDTH / BASE_WIDTH
            SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
            print(f"Updated scale factors: X={SCALE_X:.2f}, Y={SCALE_Y:.2f}")

            # Recalculate lane positions
            LANE_WIDTH = SCREEN_WIDTH // 6
            LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
            print(f"Recalculated lane positions: {LANE_POSITIONS}")

            # Update player position
            if hasattr(self, "player_car"):
                self.player_car.x = LANE_POSITIONS[self.player_car.lane]
                self.player_car.y = SCREEN_HEIGHT - scale_value(150)
                print(f"Updated player position: x={self.player_car.x}, y={self.player_car.y}")

            # Resize the screen - use a more reliable approach
            print("Setting new display mode...")
            try:
                # Try to reinitialize the display for better compatibility
                current_flags = pygame.display.get_surface().get_flags()
                is_fullscreen = bool(current_flags & pygame.FULLSCREEN)
                
                if is_fullscreen:
                    # If we're in fullscreen, maintain fullscreen mode
                    self.screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), 
                        pygame.FULLSCREEN
                    )
                else:
                    # Otherwise use resizable mode
                    self.screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), 
                        pygame.RESIZABLE
                    )
                    # Reset maximized flag if we're in windowed mode
                    self.is_maximized = False
            except Exception as e:
                print(f"Error setting display mode: {e}")
                # Fallback to basic mode
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                
            print(f"New screen size: {self.screen.get_width()}x{self.screen.get_height()}")

            # Try to restore the previous surface content
            try:
                if old_surface:
                    scaled_surface = pygame.transform.scale(old_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    self.screen.blit(scaled_surface, (0, 0))
            except Exception as e:
                print(f"Could not restore previous screen content: {e}")

            # Update fonts
            self.font = get_font(scale_value(36))
            self.font_large = get_font(scale_value(48), bold=True)
            self.font_medium = get_font(scale_value(36), bold=True)
            self.font_small = get_font(scale_value(24))
            print("Updated fonts")

            # Regenerate stars for new screen size
            self.generate_stars()
            
            # Regenerate sparkles for new screen size
            if hasattr(self, "generate_sparkles"):
                self.generate_sparkles(100)
                
            # Update prompt system if it exists
            if hasattr(self, "prompt_system"):
                self.prompt_system.resize()
                print("Updated prompt system")
                
            # Force a redraw of the screen to apply changes
            pygame.display.flip()
            
            print(f"Window resized to {width}x{height}, scale factors: {SCALE_X:.2f}x{SCALE_Y:.2f}")
        except Exception as e:
            print(f"Error handling resize: {e}")
            traceback.print_exc()

        # Update fonts
        self.font = get_font(scale_value(36))
        self.font_large = get_font(scale_value(48), bold=True)
        self.font_medium = get_font(scale_value(36), bold=True)
        self.font_small = get_font(scale_value(24))

        # Regenerate stars for new screen size
        self.generate_stars()
        
                # Force a redraw of the screen to apply changes
        pygame.display.flip()

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
        
        try:
            # Store current display surface to restore if needed
            try:
                old_surface = pygame.display.get_surface().copy()
            except:
                old_surface = None
            
            # Check current display mode
            current_flags = pygame.display.get_surface().get_flags()
            is_fullscreen = bool(current_flags & pygame.FULLSCREEN)
            
            print(f"Toggling fullscreen. Current state: {'Fullscreen' if is_fullscreen else 'Windowed'}")
            
            if is_fullscreen:
                # Switch to windowed mode
                if hasattr(self, "pre_maximize_size") and self.pre_maximize_size:
                    window_width, window_height = self.pre_maximize_size
                    print(f"Restoring pre-maximize size: {window_width}x{window_height}")
                    self.pre_maximize_size = None
                elif hasattr(self, "windowed_size") and self.windowed_size:
                    window_width, window_height = self.windowed_size
                    print(f"Restoring windowed size: {window_width}x{window_height}")
                else:
                    # Default size if no previous size is stored
                    window_width, window_height = 1280, 720
                    print(f"Using default windowed size: {window_width}x{window_height}")
                
                # Update global variables
                SCREEN_WIDTH = window_width
                SCREEN_HEIGHT = window_height
                
                # Force windowed mode using a direct approach
                print("Setting windowed mode...")
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), 
                    pygame.RESIZABLE
                )
                pygame.display.set_caption("Car Racing Game")
                
                # Reset maximized flag
                self.is_maximized = False
            else:
                # Save current window size before going fullscreen
                if not self.is_maximized:  # Only save if not already maximized
                    self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
                    print(f"Saving windowed size: {self.windowed_size}")
                
                # Get the display info for proper fullscreen resolution
                info = pygame.display.Info()
                SCREEN_WIDTH = info.current_w
                SCREEN_HEIGHT = info.current_h
                print(f"Setting fullscreen resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                
                # Force fullscreen mode using a direct approach
                print("Setting fullscreen mode...")
                self.screen = pygame.display.set_mode(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), 
                    pygame.FULLSCREEN
                )
                pygame.display.set_caption("Car Racing Game")
                
                # Set maximized flag
                self.is_maximized = True
            
            # Update scale factors
            SCALE_X = SCREEN_WIDTH / BASE_WIDTH
            SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
            print(f"Updated scale factors: X={SCALE_X:.2f}, Y={SCALE_Y:.2f}")
            
            # Recalculate lane positions
            LANE_WIDTH = SCREEN_WIDTH // 6
            LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
            print(f"Recalculated lane positions: {LANE_POSITIONS}")
            
            # Try to restore the previous surface content
            try:
                if old_surface:
                    scaled_surface = pygame.transform.scale(old_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    self.screen.blit(scaled_surface, (0, 0))
                    pygame.display.flip()
            except Exception as e:
                print(f"Could not restore previous screen content: {e}")
                
            return not is_fullscreen  # Return new fullscreen state
            
        except Exception as e:
            print(f"Error in toggle_fullscreen: {e}")
            traceback.print_exc()
            # Try to recover by setting a safe display mode
            try:
                self.screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)
                pygame.display.set_caption("Car Racing Game")
                print("Recovered with safe display mode")
                return False
            except:
                print("Could not recover display mode")
                return False
            
        except Exception as e:
            print(f"Error in toggle_fullscreen: {e}")
            traceback.print_exc()
            # Try to recover by setting a safe display mode
            try:
                self.screen = pygame.display.set_mode((1024, 768), pygame.RESIZABLE)
                pygame.display.set_caption("Car Racing Game")
                print("Recovered with safe display mode")
                return False
            except:
                print("Could not recover display mode")
                return False
        
        # Update player position if it exists
        if hasattr(self, "player_car"):
            try:
                self.player_car.x = LANE_POSITIONS[self.player_car.lane]
                self.player_car.y = SCREEN_HEIGHT - scale_value(150)
                print(f"Updated player position: x={self.player_car.x}, y={self.player_car.y}")
            except Exception as e:
                print(f"Error updating player position: {e}")
        
        # Update fonts
        try:
            self.font = get_font(scale_value(36))
            self.font_large = get_font(scale_value(48), bold=True)
            self.font_medium = get_font(scale_value(36), bold=True)
            self.font_small = get_font(scale_value(24))
            print("Updated fonts")
        except Exception as e:
            print(f"Error updating fonts: {e}")
        
        # Regenerate stars for new screen size
        try:
            self.generate_stars()
            print("Regenerated stars")
        except Exception as e:
            print(f"Error regenerating stars: {e}")
        
        # Regenerate sparkles for new screen size
        try:
            if hasattr(self, "generate_sparkles"):
                self.generate_sparkles(100)
                print("Regenerated sparkles")
        except Exception as e:
            print(f"Error regenerating sparkles: {e}")
            
        # Update prompt system if it exists
        try:
            if hasattr(self, "prompt_system"):
                self.prompt_system.resize()
                print("Updated prompt system")
        except Exception as e:
            print(f"Error updating prompt system: {e}")
        
        # Force a redraw of the screen to apply changes
        try:
            pygame.display.flip()
            print("Screen updated")
        except Exception as e:
            print(f"Error updating screen: {e}")
            
        # Reinitialize any active sounds
        try:
            if sound_enabled and hasattr(self, "init_sounds"):
                self.init_sounds()
                print("Reinitialized sounds")
        except Exception as e:
            print(f"Error reinitializing sounds: {e}")
            
        return is_fullscreen


        print(
            f"Window resized to {width}x{height}, scale factors: {SCALE_X:.2f}x{SCALE_Y:.2f}"
        )

    def init_sounds(self):
        """Initialize sound effects with proper error handling"""
        try:
            if sound_enabled and pygame.mixer.get_init():
                # Define sound file paths
                self.SOUND_ENGINE = "sounds/engine.wav"
                self.SOUND_CRASH = "sounds/crash.wav"
                self.SOUND_POWERUP = "sounds/powerup.wav"
                self.SOUND_COIN = "sounds/coin.wav"
                self.SOUND_MENU_SELECT = "sounds/menu_select.wav"
                self.SOUND_MENU_NAVIGATE = "sounds/menu_navigate.wav"
                self.SOUND_BOOST = "sounds/boost.wav"
                self.SOUND_SHIELD = "sounds/shield.wav"
                self.SOUND_GAME_OVER = "sounds/game_over.wav"
                self.SOUND_BACKGROUND_MUSIC = "sounds/background_music.mp3"
                self.SOUND_MENU_MUSIC = "sounds/menu_music.mp3"  # Menu music file

                # Create placeholder sound files if they don't exist
                self.create_placeholder_sounds()

                # Load sounds
                self.sound_engine = pygame.mixer.Sound(self.SOUND_ENGINE)
                self.sound_crash = pygame.mixer.Sound(self.SOUND_CRASH)
                self.sound_powerup = pygame.mixer.Sound(self.SOUND_POWERUP)
                self.sound_coin = pygame.mixer.Sound(self.SOUND_COIN)
                self.sound_menu_select = pygame.mixer.Sound(self.SOUND_MENU_SELECT)
                self.sound_menu_navigate = pygame.mixer.Sound(self.SOUND_MENU_NAVIGATE)
                self.sound_boost = pygame.mixer.Sound(self.SOUND_BOOST)
                self.sound_shield = pygame.mixer.Sound(self.SOUND_SHIELD)
                self.sound_game_over = pygame.mixer.Sound(self.SOUND_GAME_OVER)

                # Set volume levels
                self.sound_engine.set_volume(0.3)
                self.sound_crash.set_volume(0.7)
                self.sound_powerup.set_volume(0.5)
                self.sound_coin.set_volume(0.4)
                self.sound_menu_select.set_volume(0.5)
                self.sound_menu_navigate.set_volume(0.3)
                self.sound_boost.set_volume(0.6)
                self.sound_shield.set_volume(0.5)
                self.sound_game_over.set_volume(0.7)

                # Engine sound channel for looping
                self.engine_channel = pygame.mixer.Channel(0)
                self.engine_playing = False

                # Menu music channel
                self.menu_music_channel = pygame.mixer.Channel(1)
                self.menu_music_playing = False

                print("Sound effects loaded successfully")
                return True
            else:
                print("Sound mixer not initialized, sounds will be disabled")
                return False
        except Exception as e:
            print(f"Error initializing sounds: {e}")
            traceback.print_exc()
            return False

    def create_placeholder_sounds(self):
        """Create placeholder sound files if they don't exist"""
        try:

            def create_placeholder_sound(filename, duration=1.0, freq=440):
                if not os.path.exists(filename):
                    print(f"Creating placeholder sound: {filename}")
                    import wave
                    import struct
                    import math

                    # Create a simple sine wave as placeholder
                    sample_rate = 44100
                    amplitude = 4096
                    num_samples = int(duration * sample_rate)

                    with wave.open(filename, "w") as wav_file:
                        wav_file.setparams(
                            (1, 2, sample_rate, num_samples, "NONE", "not compressed")
                        )

                        for i in range(num_samples):
                            sample = amplitude * math.sin(
                                2 * math.pi * freq * i / sample_rate
                            )
                            packed_sample = struct.pack("h", int(sample))
                            wav_file.writeframes(packed_sample)

            # Create engine sound with a lower frequency and longer duration for looping
            create_placeholder_sound(self.SOUND_ENGINE, duration=3.0, freq=150)

            # Create placeholder sounds with different frequencies for distinction
            create_placeholder_sound(self.SOUND_CRASH, duration=0.5, freq=100)
            create_placeholder_sound(self.SOUND_POWERUP, duration=0.3, freq=800)
            create_placeholder_sound(self.SOUND_COIN, duration=0.2, freq=1000)
            create_placeholder_sound(self.SOUND_MENU_SELECT, duration=0.2, freq=600)
            create_placeholder_sound(self.SOUND_MENU_NAVIGATE, duration=0.1, freq=500)
            create_placeholder_sound(self.SOUND_BOOST, duration=0.4, freq=300)
            create_placeholder_sound(self.SOUND_SHIELD, duration=0.3, freq=700)
            create_placeholder_sound(self.SOUND_GAME_OVER, duration=1.0, freq=150)

            # For background music, create a proper looping sound file
            if not os.path.exists(self.SOUND_BACKGROUND_MUSIC) or os.path.getsize(self.SOUND_BACKGROUND_MUSIC) < 1000:
                print(f"Creating proper background music: {self.SOUND_BACKGROUND_MUSIC}")
                # Create a longer, more complex sound for background music
                create_placeholder_sound(self.SOUND_BACKGROUND_MUSIC.replace('.mp3', '.wav'), duration=10.0, freq=220)
                # Rename the file to .mp3 extension
                if os.path.exists(self.SOUND_BACKGROUND_MUSIC.replace('.mp3', '.wav')):
                    os.rename(self.SOUND_BACKGROUND_MUSIC.replace('.mp3', '.wav'), self.SOUND_BACKGROUND_MUSIC)

            # For menu music, create a placeholder for chill synth racing track
            if not os.path.exists(self.SOUND_MENU_MUSIC) or os.path.getsize(self.SOUND_MENU_MUSIC) < 1000:
                print(f"Creating proper menu music: {self.SOUND_MENU_MUSIC}")
                # Create a longer, more complex sound for menu music
                create_placeholder_sound(self.SOUND_MENU_MUSIC.replace('.mp3', '.wav'), duration=8.0, freq=330)
                # Rename the file to .mp3 extension
                if os.path.exists(self.SOUND_MENU_MUSIC.replace('.mp3', '.wav')):
                    os.rename(self.SOUND_MENU_MUSIC.replace('.mp3', '.wav'), self.SOUND_MENU_MUSIC)

            print("Placeholder sounds created successfully")
            return True
        except Exception as e:
            print(f"Error creating placeholder sounds: {e}")
            traceback.print_exc()
            return False
            
    def play_background_music(self):
        """Play background music in a loop using track_01.mp3"""
        try:
            if sound_enabled and music_enabled and pygame.mixer.get_init():
                # Use track_01.mp3 as the background music
                track_01_path = "sounds/music/track_01.mp3"
                
                if os.path.exists(track_01_path) and os.path.getsize(track_01_path) > 1000:
                    print("Starting background music with track_01.mp3...")
                    pygame.mixer.music.load(track_01_path)
                    pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
                    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                    print("Background music started with track_01.mp3")
                    return True
                else:
                    # Fallback to default background music if track_01.mp3 is not available
                    if os.path.exists(self.SOUND_BACKGROUND_MUSIC) and os.path.getsize(self.SOUND_BACKGROUND_MUSIC) > 1000:
                        print("Track_01.mp3 not found, using fallback background music...")
                        pygame.mixer.music.load(self.SOUND_BACKGROUND_MUSIC)
                        pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
                        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                        print("Background music started (fallback mode)")
                        return True
            return False
        except Exception as e:
            print(f"Error playing background music: {e}")
            traceback.print_exc()
            return False
            
    def stop_background_music(self):
        """Stop the background music"""
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("Background music stopped")
        except Exception as e:
            print(f"Error stopping background music: {e}")
            traceback.print_exc()
            return False
    
    def _play_next_song(self):
        """Play the next song in the playlist"""
        try:
            if not self.music_playlist:
                return False
                
            # Load and play the current song
            current_song = self.music_playlist[self.current_music_index]
            print(f"Playing music: {current_song}")
            
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
            pygame.mixer.music.play(0)  # Play once
            
            # Set up an event for when the song ends
            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
            
            return True
        except Exception as e:
            print(f"Error playing song {self.current_music_index}: {e}")
            self._advance_playlist()  # Try the next song
            return False
    
    def _advance_playlist(self):
        """Advance to the next song in the playlist"""
        if not self.music_playlist:
            return
            
        self.current_music_index = (self.current_music_index + 1) % len(self.music_playlist)
        self._play_next_song()
            
    def stop_background_music(self):
        """Stop the background music"""
        try:
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                print("Background music stopped")
        except Exception as e:
            print(f"Error stopping background music: {e}")

    def generate_stars(self):
        """Generate random stars for the night sky"""
        self.stars = []
        for _ in range(STAR_COUNT):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)  # Stars only in top half of sky
            size = random.uniform(0.5, 2)
            brightness = random.uniform(0.5, 1.0)
            twinkle_speed = random.uniform(1.0, 3.0)
            self.stars.append(
                {
                    "x": x,
                    "y": y,
                    "size": size,
                    "brightness": brightness,
                    "twinkle_speed": twinkle_speed,
                    "twinkle_offset": random.uniform(0, 2 * math.pi),
                }
            )

    def generate_sparkles(self, count=30):  # Reduced from default 100 to 30
        """Generate sparkles for menu background animation"""
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
        """Update sparkle positions and properties"""
        # Limit the maximum number of sparkles
        max_sparkles = 50  # Set a maximum limit for sparkles
        if len(self.sparkles) > max_sparkles:
            # Remove excess sparkles
            self.sparkles = self.sparkles[:max_sparkles]
            
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
                
            # Occasionally remove sparkles (5% chance per second)
            if random.random() < 0.0008:  # ~5% chance per second at 60fps
                self.sparkles.remove(sparkle)
                break
    
    def draw_sparkles(self, surface):
        """Draw sparkles on the given surface"""
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

    def reset_game(self):
        # Use the selected car color if available
        car_color = RED  # Default red
        if hasattr(self, 'selected_car'):
            # Define car colors matching the garage options
            car_colors = [
                (255, 0, 0),    # Red
                (0, 0, 255),    # Blue
                (0, 255, 0),    # Green
                (255, 255, 0),  # Yellow
                (128, 0, 128)   # Purple
            ]
            if 0 <= self.selected_car < len(car_colors):
                car_color = car_colors[self.selected_car]
        
        self.player_car = Car(
            LANE_POSITIONS[3],  # Start in the middle lane (lane 3 of 0-7)
            SCREEN_HEIGHT - scale_value(150),
            scale_value(CAR_WIDTH),
            scale_value(CAR_HEIGHT),
            car_color,
        )
        self.obstacles = []
        self.other_cars = []
        self.powerups = []
        self.coins = []
        self.speed = INITIAL_SPEED
        self.score = 0
        self.coins_collected = 0
        self.game_over = False
        self.last_obstacle_time = time.time()
        self.last_car_time = time.time()
        self.last_powerup_time = time.time()
        self.last_coin_time = time.time()
        self.last_update_time = time.time()
        self.combo_count = 0
        self.combo_timer = 0
        self.score_multiplier = 1
        self.game_mode = GAME_MODE_ENDLESS
        self.distance_traveled = 0
        self.time_remaining = TIME_ATTACK_INITIAL_TIME  # for time attack mode
        self.time_attack_mission_type = random.randint(0, 5)  # Random Time Attack mission
        self.time_attack_target = 0
        self.time_attack_progress = 0
        self.time_attack_speed_timer = 0  # For speed maintenance mission
        self.time_attack_passed_cars = 0  # For passing cars mission
        self.time_attack_avoided_obstacles = 0  # For avoiding obstacles mission
        self.mission_type = random.randint(0, 3)  # For regular missions mode
        self.mission_target = 0
        self.mission_progress = 0
        self.set_mission()
        self.start_time = time.time()
        self.powerups_used = 0
        self.player_name = "Player"  # Default player name
        
        # Flag to track if a game has been played
        self.game_has_been_played = False

        # Reset prompt system
        if hasattr(self, "prompt_system"):
            self.prompt_system.reset()
            # Show welcome prompt after a short delay
            self.welcome_prompt_timer = 1.0  # Show welcome prompt after 1 second

        # Reset day-night cycle but keep the current time
        if hasattr(self, "day_phase"):
            self.cycle_time = self.day_phase * DAY_NIGHT_CYCLE_DURATION
        else:
            self.cycle_time = 0
            self.day_phase = 0

        # Stop menu music if it's playing
        if (
            sound_enabled
            and hasattr(self, "menu_music_channel")
            and self.menu_music_playing
        ):
            self.menu_music_channel.stop()
            self.menu_music_playing = False

    def set_mission(self):
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

    def update_mission_progress(self):
        """Update mission progress based on the current mission type"""
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
            
            # Play success sound if available
            if sound_enabled and hasattr(self, "sound_powerup"):
                self.sound_powerup.play()

    def handle_events(self):
        try:
            global SCREEN_WIDTH, SCREEN_HEIGHT, LANE_WIDTH, LANE_POSITIONS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                # Pass event to prompt system first
                if hasattr(self, "prompt_system") and self.prompt_system.handle_input(
                    event
                ):
                    continue

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player_car.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.player_car.move_right()
                    elif event.key == pygame.K_SPACE:
                        # Use boost when space is pressed
                        if self.player_car.use_boost_energy():
                            # Play boost sound
                            if sound_enabled and hasattr(self, "sound_boost"):
                                self.sound_boost.play()
                            # Show boost prompt if it's the first time
                            if hasattr(self, "prompt_system"):
                                self.prompt_system.show_prompt("powerup_boost")
                    elif event.key == pygame.K_t:
                        # Debug: Toggle time of day when T is pressed
                        self.cycle_time = (
                            self.cycle_time + DAY_NIGHT_CYCLE_DURATION / 4
                        ) % DAY_NIGHT_CYCLE_DURATION
                        self.day_phase = self.cycle_time / DAY_NIGHT_CYCLE_DURATION
                    elif event.key == pygame.K_F11:
                        # Toggle fullscreen mode when F11 is pressed
                        print("F11 key pressed - toggling fullscreen")
                        try:
                            # Store current game state
                            try:
                                current_state = self.screen.copy()
                            except:
                                current_state = None
                            
                            # Toggle fullscreen
                            new_fullscreen_state = self.toggle_fullscreen()
                            
                            # Restore game state if possible
                            try:
                                if current_state:
                                    scaled_state = pygame.transform.scale(current_state, (SCREEN_WIDTH, SCREEN_HEIGHT))
                                    self.screen.blit(scaled_state, (0, 0))
                                    pygame.display.flip()
                            except Exception as e:
                                print(f"Error restoring game state: {e}")
                                
                            print(f"Fullscreen toggle complete. New state: {'Fullscreen' if new_fullscreen_state else 'Windowed'}")
                        except Exception as e:
                            print(f"Error during fullscreen toggle: {e}")
                            traceback.print_exc()
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        # Show pause menu when ESC or P is pressed
                        pause_result = self.show_pause_menu()
                        if not pause_result:
                            return False
                # Handle mouse clicks for pause button
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if pause button was clicked
                        pause_button_rect = pygame.Rect(
                            SCREEN_WIDTH - scale_value(50),
                            scale_value(10),
                            scale_value(40),
                            scale_value(40),
                        )
                        if pause_button_rect.collidepoint(event.pos):
                            pause_result = self.show_pause_menu()
                            if not pause_result:
                                return False
                # Handle window resize
                elif event.type == pygame.VIDEORESIZE:
                    try:
                        # Handle resize with our enhanced method
                        self.handle_resize(event.w, event.h)
                    except Exception as e:
                        print(f"Error handling resize event: {e}")
                        traceback.print_exc()
            return True
        except Exception as e:
            print(f"Error handling events: {e}")
            traceback.print_exc()
            return False

    def show_name_input(self):
        """Show a screen to input player name for high score with transition animation"""
        # Add transition animation
        if hasattr(self, "transition"):
            self.transition.transition_type = "radial"
            self.transition.start(direction="in", duration=0.6)
            
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 400, 50)
        color_inactive = SLEEK_SILVER
        color_active = NEON_YELLOW
        color = color_inactive
        active = True
        text = self.player_name
        done = False

        title_font = get_font(48, bold=True)
        input_font = get_font(32)

        # Try to load the background image
        try:
            background_image = pygame.image.load("bgm.jpg")
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            has_background_image = True
        except Exception as e:
            print(f"Error loading background image for name input: {e}")
            has_background_image = False
            
            # Create a semi-transparent background as fallback
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            background.fill((0, 0, 0, 180))  # Semi-transparent black

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = input_box.collidepoint(event.pos)
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            self.player_name = text
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            # Limit name length to 15 characters
                            if len(text) < 15:
                                text += event.unicode

            # Draw background
            if has_background_image:
                # Use the loaded image as background
                self.screen.blit(background_image, (0, 0))
                
                # Add a semi-transparent overlay to make text more readable
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))  # Semi-transparent black
                self.screen.blit(overlay, (0, 0))
                
                # Draw sparkles animation
                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
                self.draw_sparkles(self.screen)
            else:
                # Use the gradient background
                self.screen.blit(background, (0, 0))

            # Draw title
            title_text = title_font.render("NEW HIGH SCORE!", True, NEON_YELLOW)
            title_rect = title_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            )
            self.screen.blit(title_text, title_rect)

            # Draw score
            score_text = input_font.render(
                f"Score: {self.score}", True, ELECTRIC_PURPLE
            )
            score_rect = score_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60)
            )
            self.screen.blit(score_text, score_rect)

            # Draw prompt
            prompt_text = input_font.render("Enter your name:", True, WHITE)
            prompt_rect = prompt_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
            )
            self.screen.blit(prompt_text, prompt_rect)

            # Draw input box
            pygame.draw.rect(self.screen, color, input_box, 2, border_radius=10)

            # Draw input text
            txt_surface = input_font.render(text, True, WHITE)
            # Ensure text doesn't overflow the input box
            width = max(400, txt_surface.get_width() + 10)
            input_box.w = width
            input_box.x = SCREEN_WIDTH // 2 - width // 2
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            # Draw instructions
            instruction_text = get_font(24).render(
                "Press ENTER to confirm", True, SLEEK_SILVER
            )
            instruction_rect = instruction_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
            )
            self.screen.blit(instruction_text, instruction_rect)

            pygame.display.flip()
            self.clock.tick(30)

        return text

    def show_highscores(self, player_name=None):
        """Show the high scores screen with delete buttons and transition animation"""
        # Add transition animation
        if hasattr(self, "transition"):
            self.transition.transition_type = "slide_up"
            self.transition.start(direction="in", duration=0.4)
            
        # Define colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        NEON_YELLOW = (255, 255, 0)
        ELECTRIC_PURPLE = (191, 64, 191)
        SLEEK_SILVER = (204, 204, 204)
        BRIGHT_RED = (255, 62, 65)
        NEON_GREEN = (57, 255, 20)
        LIGHT_BLUE = (0, 191, 255)

        # Get screen dimensions
        SCREEN_WIDTH = self.screen.get_width()
        SCREEN_HEIGHT = self.screen.get_height()

        # Try to load the background image
        try:
            background_image = pygame.image.load("bgm.jpg")
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            has_background_image = True
        except Exception as e:
            print(f"Error loading background image for high scores: {e}")
            has_background_image = False
            
            # Create a semi-transparent background as fallback
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            background.fill((0, 0, 0, 180))  # Semi-transparent black

        title_font = get_font(48, bold=True)
        score_font = get_font(24)
        tab_font = get_font(28, bold=True)

        # Initialize mode selection
        current_mode = self.game_mode
        mode_names = {
            GAME_MODE_ENDLESS: "ENDLESS MODE",
            GAME_MODE_TIME_ATTACK: "TIME ATTACK MODE",
            GAME_MODE_MISSIONS: "MISSIONS MODE",
            GAME_MODE_RACE: "RACE MODE"
        }
        mode_colors = {
            GAME_MODE_ENDLESS: NEON_YELLOW,
            GAME_MODE_TIME_ATTACK: ELECTRIC_PURPLE,
            GAME_MODE_MISSIONS: NEON_GREEN,
            GAME_MODE_RACE: LIGHT_BLUE
        }
        
        # Get high scores for current mode
        highscores = self.highscore_manager.get_highscores(current_mode)

        # Create delete buttons for each score
        delete_buttons = []

        # Ensure menu music is playing
        if (
            sound_enabled
            and music_enabled
            and hasattr(self, "menu_music_channel")
            and not self.menu_music_playing
        ):
            try:
                # Load menu music
                menu_music = pygame.mixer.Sound(self.SOUND_MENU_MUSIC)
                menu_music.set_volume(0.4)  # Set appropriate volume
                self.menu_music_channel.play(menu_music, loops=-1)  # Loop indefinitely
                self.menu_music_playing = True
                print("Menu music started")
            except Exception as e:
                print(f"Error playing menu music: {e}")

        # Create tab buttons for different game modes
        tab_buttons = []
        tab_width = SCREEN_WIDTH // 4
        tab_height = 40
        tab_y = SCREEN_HEIGHT // 6 - 20
        
        for i, mode in enumerate([GAME_MODE_ENDLESS, GAME_MODE_TIME_ATTACK, GAME_MODE_MISSIONS, GAME_MODE_RACE]):
            tab_rect = pygame.Rect(i * tab_width, tab_y, tab_width, tab_height)
            tab_buttons.append((tab_rect, mode))

        done = False
        while not done:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Stop menu music if playing
                    if (
                        sound_enabled
                        and hasattr(self, "menu_music_channel")
                        and self.menu_music_playing
                    ):
                        self.menu_music_channel.stop()
                        self.menu_music_playing = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    elif event.key == pygame.K_LEFT:
                        # Switch to previous mode
                        current_mode = (current_mode - 1) % 4
                        highscores = self.highscore_manager.get_highscores(current_mode)
                        delete_buttons = []  # Reset delete buttons
                    elif event.key == pygame.K_RIGHT:
                        # Switch to next mode
                        current_mode = (current_mode + 1) % 4
                        highscores = self.highscore_manager.get_highscores(current_mode)
                        delete_buttons = []  # Reset delete buttons
                    else:
                        done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Check if any tab was clicked
                        for tab_rect, mode in tab_buttons:
                            if tab_rect.collidepoint(mouse_pos):
                                if current_mode != mode:
                                    current_mode = mode
                                    highscores = self.highscore_manager.get_highscores(current_mode)
                                    delete_buttons = []  # Reset delete buttons
                                    # Play menu sound
                                    if sound_enabled and hasattr(self, "sound_menu_navigate"):
                                        self.sound_menu_navigate.play()
                                break

                        # Check if any delete button was clicked
                        button_clicked = False
                        for i, button_rect in enumerate(delete_buttons):
                            if button_rect.collidepoint(mouse_pos):
                                button_clicked = True
                                # Play menu sound
                                if sound_enabled and hasattr(self, "sound_menu_select"):
                                    self.sound_menu_select.play()
                                # Delete the score
                                if self.highscore_manager.delete_score(
                                    current_mode, i
                                ):
                                    # Refresh the high scores list
                                    highscores = self.highscore_manager.get_highscores(
                                        current_mode
                                    )
                                    # Don't exit the screen, just refresh the display
                                break

                        # Only exit if we clicked outside any button and not on a delete button
                        if not button_clicked:
                            # Check if we clicked on the "back" area at the bottom
                            back_area = pygame.Rect(
                                SCREEN_WIDTH // 4,
                                SCREEN_HEIGHT - 70,
                                SCREEN_WIDTH // 2,
                                40,
                            )
                            if back_area.collidepoint(mouse_pos):
                                # Play menu sound
                                if sound_enabled and hasattr(self, "sound_menu_select"):
                                    self.sound_menu_select.play()
                                done = True

            # Draw background
            if has_background_image:
                # Use the loaded image as background
                self.screen.blit(background_image, (0, 0))
                
                # Add a semi-transparent overlay to make text more readable
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))  # Semi-transparent black
                self.screen.blit(overlay, (0, 0))
                
                # Draw sparkles animation
                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
                self.draw_sparkles(self.screen)
            else:
                # Use the gradient background
                self.screen.blit(background, (0, 0))

            # Draw title
            title_text = title_font.render("HIGH SCORES", True, NEON_YELLOW)
            title_rect = title_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 10)
            )
            self.screen.blit(title_text, title_rect)
            
            # Draw tabs for different game modes
            for i, mode in enumerate([GAME_MODE_ENDLESS, GAME_MODE_TIME_ATTACK, GAME_MODE_MISSIONS, GAME_MODE_RACE]):
                tab_rect = pygame.Rect(i * tab_width, tab_y, tab_width, tab_height)
                
                # Highlight current mode tab
                if mode == current_mode:
                    pygame.draw.rect(self.screen, mode_colors[mode], tab_rect)
                    pygame.draw.rect(self.screen, WHITE, tab_rect, 2)
                else:
                    pygame.draw.rect(self.screen, (50, 50, 50, 150), tab_rect)
                    pygame.draw.rect(self.screen, SLEEK_SILVER, tab_rect, 1)
                
                # Draw tab text
                tab_text = tab_font.render(mode_names[mode].split()[0], True, WHITE)
                tab_text_rect = tab_text.get_rect(center=tab_rect.center)
                self.screen.blit(tab_text, tab_text_rect)

            # Draw mode name
            mode_text = score_font.render(mode_names[current_mode], True, mode_colors[current_mode])
            mode_rect = mode_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 50)
            )
            self.screen.blit(mode_text, mode_rect)

            # Draw column headers
            header_y = SCREEN_HEIGHT // 6 + 100
            rank_text = score_font.render("RANK", True, SLEEK_SILVER)
            name_text = score_font.render("NAME", True, SLEEK_SILVER)
            score_text = score_font.render("SCORE", True, SLEEK_SILVER)
            date_text = score_font.render("DATE", True, SLEEK_SILVER)
            action_text = score_font.render("ACTION", True, SLEEK_SILVER)

            self.screen.blit(
                rank_text, (SCREEN_WIDTH // 6 - rank_text.get_width() // 2, header_y)
            )
            self.screen.blit(
                name_text,
                (SCREEN_WIDTH * 2 // 6 - name_text.get_width() // 2, header_y),
            )
            self.screen.blit(
                score_text,
                (SCREEN_WIDTH * 3 // 6 - score_text.get_width() // 2, header_y),
            )
            self.screen.blit(
                date_text,
                (SCREEN_WIDTH * 4 // 6 - date_text.get_width() // 2, header_y),
            )
            self.screen.blit(
                action_text,
                (SCREEN_WIDTH * 5 // 6 - action_text.get_width() // 2, header_y),
            )

            # Draw horizontal line
            pygame.draw.line(
                self.screen,
                SLEEK_SILVER,
                (SCREEN_WIDTH // 10, header_y + 30),
                (SCREEN_WIDTH * 9 // 10, header_y + 30),
                2,
            )

            # Draw high scores
            delete_buttons = []  # Clear previous buttons

            if not highscores:
                no_scores_text = score_font.render("No high scores yet!", True, WHITE)
                no_scores_rect = no_scores_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                )
                self.screen.blit(no_scores_text, no_scores_rect)
            else:
                for i, score in enumerate(highscores):
                    y_pos = header_y + 60 + i * 40

                    # Highlight the player's score
                    if player_name and score["name"] == player_name:
                        highlight_rect = pygame.Rect(
                            SCREEN_WIDTH // 10, y_pos - 5, SCREEN_WIDTH * 8 // 10, 30
                        )
                        pygame.draw.rect(
                            self.screen,
                            (50, 50, 100, 100),
                            highlight_rect,
                            border_radius=5,
                        )

                    # Rank
                    rank_text = score_font.render(f"{i+1}", True, WHITE)
                    self.screen.blit(
                        rank_text,
                        (SCREEN_WIDTH // 6 - rank_text.get_width() // 2, y_pos),
                    )

                    # Name
                    name_text = score_font.render(score["name"], True, WHITE)
                    self.screen.blit(
                        name_text,
                        (SCREEN_WIDTH * 2 // 6 - name_text.get_width() // 2, y_pos),
                    )

                    # Score
                    score_text = score_font.render(f"{score['score']}", True, WHITE)
                    self.screen.blit(
                        score_text,
                        (SCREEN_WIDTH * 3 // 6 - score_text.get_width() // 2, y_pos),
                    )

                    # Date
                    date_text = score_font.render(score["date"], True, WHITE)
                    self.screen.blit(
                        date_text,
                        (SCREEN_WIDTH * 4 // 6 - date_text.get_width() // 2, y_pos),
                    )

                    # Delete button
                    delete_button_rect = pygame.Rect(
                        SCREEN_WIDTH * 5 // 6 - 40, y_pos - 10, 80, 30
                    )
                    pygame.draw.rect(
                        self.screen, BRIGHT_RED, delete_button_rect, border_radius=5
                    )
                    delete_text = score_font.render("Delete", True, WHITE)
                    delete_text_rect = delete_text.get_rect(
                        center=delete_button_rect.center
                    )
                    self.screen.blit(delete_text, delete_text_rect)

                    # Add button to the list
                    delete_buttons.append(delete_button_rect)

            # Draw back button area
            back_button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 40
            )
            pygame.draw.rect(
                self.screen, SLEEK_SILVER, back_button_rect, 2, border_radius=10
            )

            # Draw instructions
            instruction_text = score_font.render("Back to Menu", True, SLEEK_SILVER)
            instruction_rect = instruction_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
            )
            self.screen.blit(instruction_text, instruction_rect)

            pygame.display.flip()
            self.clock.tick(30)

    def show_pause_menu(self):
        # Pause engine sound if it's playing
        if sound_enabled and hasattr(self, "engine_channel") and self.engine_playing:
            self.engine_channel.pause()
            
        # Pause background music
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

        # Create pause menu
        pause_menu = PauseMenu(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Store the current game state
        game_state_surface = self.screen.copy()

        # Create slide-in animation for pause menu
        slide_progress = 0
        slide_duration = 0.3  # seconds
        slide_start_time = time.time()

        # Add a special transition effect for pause menu
        if hasattr(self, "transition"):
            # Use a quick blinds transition for pause effect
            self.transition.transition_type = "blinds"
            self.transition.start(direction="in", duration=0.3)

        # Play pause sound
        if sound_enabled and hasattr(self, "sound_menu_select"):
            self.sound_menu_select.play()

        # Main pause menu loop
        clock = pygame.time.Clock()
        while True:
            # Calculate slide animation progress
            current_time = time.time()
            slide_progress = min(
                1.0, (current_time - slide_start_time) / slide_duration
            )

            # Restore the game state as background
            self.screen.blit(game_state_surface, (0, 0))

            # Apply a darkening overlay with fade-in effect
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(180 * slide_progress)))  # Semi-transparent black
            self.screen.blit(overlay, (0, 0))

            # Draw and handle the pause menu with slide-in animation
            if slide_progress < 1.0:
                # Apply slide-in effect from top
                offset_y = int((1.0 - slide_progress) * -SCREEN_HEIGHT * 0.5)

                # Create a temporary surface for the menu
                temp_surface = pygame.Surface(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                )

                # Draw menu to temporary surface
                pause_menu.draw_to_surface(temp_surface)

                # Blit with offset for slide-in effect
                self.screen.blit(temp_surface, (0, offset_y))

                # Update display
                pygame.display.flip()
                clock.tick(60)

                # Handle events during animation
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Play menu sound
                            if sound_enabled and hasattr(self, "sound_menu_select"):
                                self.sound_menu_select.play()

                            # Resume engine sound
                            if (
                                sound_enabled
                                and hasattr(self, "engine_channel")
                                and self.engine_playing
                            ):
                                self.engine_channel.unpause()

                            return True

                # Continue animation
                if slide_progress < 1.0:
                    continue

            # Normal menu interaction once animation is complete
            pause_menu.draw()
            result = pause_menu.handle_input()

            if result == "RESUME":
                # Play menu sound
                if sound_enabled and hasattr(self, "sound_menu_select"):
                    self.sound_menu_select.play()

                # Resume engine sound
                if (
                    sound_enabled
                    and hasattr(self, "engine_channel")
                    and self.engine_playing
                ):
                    self.engine_channel.unpause()
                    
                # Resume background music
                if pygame.mixer.get_init():
                    pygame.mixer.music.unpause()

                # Slide-out animation
                slide_out_progress = 0
                slide_out_duration = 0.2  # seconds
                slide_out_start_time = time.time()

                while slide_out_progress < 1.0:
                    current_time = time.time()
                    slide_out_progress = min(
                        1.0, (current_time - slide_out_start_time) / slide_out_duration
                    )

                    # Restore the game state as background
                    self.screen.blit(game_state_surface, (0, 0))

                    # Apply a darkening overlay with fade-out effect
                    overlay = pygame.Surface(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                    )
                    overlay.fill((0, 0, 0, int(180 * (1.0 - slide_out_progress))))
                    self.screen.blit(overlay, (0, 0))

                    # Create a temporary surface for the menu
                    temp_surface = pygame.Surface(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                    )

                    # Draw menu to temporary surface
                    pause_menu.draw_to_surface(temp_surface)

                    # Blit with offset for slide-out effect
                    offset_y = int(slide_out_progress * -SCREEN_HEIGHT * 0.5)
                    self.screen.blit(temp_surface, (0, offset_y))

                    # Update display
                    pygame.display.flip()
                    clock.tick(60)

                return True
            elif result == "OPTIONS":
                self.show_settings_menu(game_state_surface)
            elif result == "MAIN MENU":
                # Play menu sound
                if sound_enabled and hasattr(self, "sound_menu_select"):
                    self.sound_menu_select.play()

                # Stop engine sound completely
                if (
                    sound_enabled
                    and hasattr(self, "engine_channel")
                    and self.engine_playing
                ):
                    self.engine_channel.stop()
                    self.engine_playing = False
                    
                # Stop background music when going to main menu
                self.stop_background_music()

                # Slide-out animation
                slide_out_progress = 0
                slide_out_duration = 0.2  # seconds
                slide_out_start_time = time.time()

                while slide_out_progress < 1.0:
                    current_time = time.time()
                    slide_out_progress = min(
                        1.0, (current_time - slide_out_start_time) / slide_out_duration
                    )

                    # Restore the game state as background
                    self.screen.blit(game_state_surface, (0, 0))

                    # Apply a darkening overlay with fade-out effect
                    overlay = pygame.Surface(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                    )
                    overlay.fill((0, 0, 0, int(180 * (1.0 - slide_out_progress))))
                    self.screen.blit(overlay, (0, 0))

                    # Create a temporary surface for the menu
                    temp_surface = pygame.Surface(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                    )

                    # Draw menu to temporary surface
                    pause_menu.draw_to_surface(temp_surface)

                    # Blit with offset for slide-out effect
                    offset_y = int(slide_out_progress * SCREEN_HEIGHT * 0.5)
                    self.screen.blit(temp_surface, (0, offset_y))

                    # Update display
                    pygame.display.flip()
                    clock.tick(60)

                self.game_over = True
                return True
            elif result == "EXIT":
                # Play menu sound
                if sound_enabled and hasattr(self, "sound_menu_select"):
                    self.sound_menu_select.play()

                # Stop engine sound
                if (
                    sound_enabled
                    and hasattr(self, "engine_channel")
                    and self.engine_playing
                ):
                    self.engine_channel.stop()

                return False
            elif result == "RESIZE":
                # Update the stored game state after resize
                game_state_surface = self.screen.copy()

            clock.tick(60)

    def show_updates_menu(self, background_surface):
        """Show the upcoming updates menu"""
        # Get current screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Add transition animation
        if hasattr(self, "transition"):
            self.transition.transition_type = "pixelate"
            self.transition.start(direction="in", duration=0.5)
        
        # Font sizes - increased for better visibility
        title_font_size = int(64 * (screen_height / 720))  # Increased from 48 to 64
        heading_font_size = int(36 * (screen_height / 720))  # Increased from 32 to 36
        text_font_size = int(26 * (screen_height / 720))  # Increased from 24 to 26
        
        # Enhanced colors for better visibility and attractiveness
        title_color = (255, 215, 0)  # Gold
        heading_colors = {
            "🔄": (100, 200, 255),  # Blue for Gameplay
            "💡": (255, 255, 100),  # Yellow for New Features
            "🎨": (255, 150, 200),  # Pink for Visual
            "🔊": (150, 255, 150),  # Green for Audio
            "🛠️": (200, 200, 200),  # Silver for Technical
            "💰": (255, 200, 100),  # Orange for Economy
            "🎮": (200, 150, 255),  # Purple for Game Modes
        }
        text_color = (255, 255, 255)  # White
        text_highlight_color = (255, 255, 150)  # Brighter light yellow for highlights
        back_button_color = (60, 60, 80)
        back_button_hover_color = (80, 80, 120)
        
        # Back button - more stylish with rounded corners
        back_button_rect = pygame.Rect(
            screen_width - 180, 
            screen_height - 70, 
            150, 
            50
        )
        back_button_hover = False
        
        # Content
        updates_content = [
            {
                "type": "heading",
                "text": "🔄 Gameplay Updates",
                "items": [
                    "Fuel System – Introduce a fuel bar that depletes over time, refueled by collecting fuel cans.",
                    "Weather Effects – Add rain, fog, or snow with associated physics (e.g., slippery roads).",
                    "Traffic Patterns – Smarter AI for traffic cars with lane-changing and different speeds.",
                    "Lane Merging or Road Splits – Add complexity by creating split paths or merging lanes.",
                    "Police Chase Mode – A special mode where players must avoid cops while racing.",
                    "Boss Levels – Introduce rare powerful vehicles to overtake or escape from.",
                    "Story Mode – Add cutscenes or narrative elements between missions.",
                    "Stunt Zones – Include ramps or destructible objects for extra points."
                ]
            },
            {
                "type": "heading",
                "text": "💡 New Features",
                "items": [
                    "Achievements System – Unlock badges for skill-based milestones (e.g., \"Drive 1000km\", \"Perfect Combo x10\").",
                    "Leaderboard Integration – Add local or online leaderboards for high scores and time attack.",
                    "Multiplayer Support – Add local 2-player split-screen or online racing (if ambitious).",
                    "Replay System – Let players watch their race with a camera switcher.",
                    "In-Game Camera Switching – Toggle between top-down, angled, or chase-view cameras."
                ]
            },
            {
                "type": "heading",
                "text": "🎨 Visual Enhancements",
                "items": [
                    "Dynamic Shadows & Lighting – Realistic shadow movement based on light sources.",
                    "Car Damage Effects – Visual wear, sparks, smoke, or denting when hitting obstacles.",
                    "Rain Particle Interaction – Water splashes on screen or tire effects during weather.",
                    "Headlight Reflections – Reflective surfaces or headlight trails during night mode.",
                    "Background Parallax Layers – Multi-depth layers (mountains, cities, etc.) to enhance movement feel."
                ]
            },
            {
                "type": "heading",
                "text": "🔊 Audio Improvements",
                "items": [
                    "Engine Sound Variants – Change engine sounds by speed or car type.",
                    "Voice Announcer – Add voice lines for events like \"Boost Ready!\" or \"Mission Complete!\".",
                    "Dynamic Music System – Music intensity changes based on speed or danger level."
                ]
            },
            {
                "type": "heading",
                "text": "🛠️ Technical & UX Updates",
                "items": [
                    "Save System – Save car unlocks, scores, and progress between sessions.",
                    "Key Rebinding – Allow players to change control bindings in settings.",
                    "Localization – Add support for multiple languages.",
                    "Accessibility Options – Colorblind modes, font scaling, sound cues for events."
                ]
            },
            {
                "type": "heading",
                "text": "💰 Economy & Progression",
                "items": [
                    "Upgrade System – Upgrade car attributes (speed, handling, fuel capacity, etc.) with coins.",
                    "Daily/Weekly Challenges – Offer time-based goals with special rewards.",
                    "Loot Boxes / Crates (non-pay) – Unlock random car skins or bonuses with collected tokens."
                ]
            },
            {
                "type": "heading",
                "text": "🎮 Enhanced Game Modes",
                "items": [
                    "Endless Hard Mode – Increase traffic and speed gradually, no power-ups.",
                    "Timed Boss Races – Face off against an elite AI racer in Time Attack format.",
                    "Delivery Missions – Pick up and drop off \"packages\" within time limits."
                ]
            }
        ]
        
        # Scrolling
        if not hasattr(self, 'updates_menu_scroll_y'):
            self.updates_menu_scroll_y = 0
        scroll_y = self.updates_menu_scroll_y
        max_scroll = 0  # Will be calculated when drawing
        scroll_speed = 15  # Reduced scroll speed for smoother scrolling
        
        # Main updates menu loop
        clock = pygame.time.Clock()
        running = True
        
        # Animation variables
        animation_time = 0
        
        while running:
            try:
                # Update animation time
                animation_time += 0.01
                
                # Restore the background
                self.screen.blit(background_surface, (0, 0))
                
                # Create a gradient overlay for more attractive background
                overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                for i in range(10):
                    y_pos = i * (screen_height // 10)
                    height = screen_height // 10
                    alpha = 180 + int(20 * math.sin(animation_time + i * 0.2))  # Animated transparency
                    color = (0, 0, 30 + i * 5, alpha)  # Gradient from dark blue to slightly lighter
                    pygame.draw.rect(overlay, color, (0, y_pos, screen_width, height))
                self.screen.blit(overlay, (0, 0))
                
                # Decorative elements removed as requested
                
                # Draw title with enhanced glow and animation effects
                title_font = pygame.font.SysFont("Arial", title_font_size, bold=True)
                
                # Create a background banner for the title
                banner_height = 100
                banner_rect = pygame.Rect(0, 30, screen_width, banner_height)
                banner_surface = pygame.Surface((screen_width, banner_height), pygame.SRCALPHA)
                
                # Create gradient banner with animation
                for i in range(banner_height):
                    alpha = 150 - int(i * 1.2)
                    if alpha < 0:
                        alpha = 0
                    # Animated color with time
                    r = 30 + int(20 * math.sin(animation_time * 0.5))
                    g = 30 + int(10 * math.sin(animation_time * 0.7 + 2))
                    b = 80 + int(30 * math.sin(animation_time * 0.3 + 4))
                    pygame.draw.line(
                        banner_surface, 
                        (r, g, b, alpha),
                        (0, i),
                        (screen_width, i)
                    )
                
                # Add animated particles to the banner
                for i in range(20):
                    particle_x = (screen_width * 0.5) + (screen_width * 0.4) * math.cos(animation_time * 0.2 + i * 0.3)
                    particle_y = banner_height * 0.5 + (banner_height * 0.3) * math.sin(animation_time * 0.3 + i * 0.2)
                    particle_size = 2 + int(2 * math.sin(animation_time + i))
                    particle_alpha = 100 + int(100 * math.sin(animation_time * 0.5 + i * 0.7))
                    pygame.draw.circle(
                        banner_surface,
                        (255, 255, 255, particle_alpha),
                        (int(particle_x), int(particle_y)),
                        particle_size
                    )
                
                self.screen.blit(banner_surface, banner_rect)
                
                # Draw enhanced glow effect for title
                glow_size = 5  # Increased from 3 to 5
                glow_intensity = 1.5 + 0.5 * math.sin(animation_time * 2)  # Pulsating glow
                for offset in range(glow_size, 0, -1):
                    glow_alpha = int((120 - offset * 20) * glow_intensity)
                    if glow_alpha > 255:
                        glow_alpha = 255
                    glow_color = (255, 215, 0, glow_alpha)
                    glow_text = title_font.render("UPCOMING UPDATES", True, glow_color)  # Changed to all caps
                    
                    # More dramatic glow spread
                    offsets = [
                        (offset * 1.5, 0),
                        (-offset * 1.5, 0),
                        (0, offset * 1.5),
                        (0, -offset * 1.5),
                        (offset, offset),
                        (-offset, -offset),
                        (offset, -offset),
                        (-offset, offset)
                    ]
                    
                    for x_off, y_off in offsets:
                        glow_rect = glow_text.get_rect(center=(screen_width // 2 + x_off, 63 + y_off))  # Adjusted from 70 to 63
                        self.screen.blit(glow_text, glow_rect)
                
                # Draw main title with shadow for depth
                shadow_text = title_font.render("UPCOMING UPDATES", True, (0, 0, 0, 180))
                shadow_rect = shadow_text.get_rect(center=(screen_width // 2 + 3, 63))  # Adjusted from 73 to 63
                self.screen.blit(shadow_text, shadow_rect)
                
                # Main title with slight animation
                title_y_offset = math.sin(animation_time * 2) * 2
                title_text = title_font.render("UPCOMING UPDATES", True, title_color)
                title_rect = title_text.get_rect(center=(screen_width // 2, 60 + title_y_offset))  # Decreased Y position from 70 to 60
                self.screen.blit(title_text, title_rect)
                
                # Add subtitle with increased vertical spacing
                subtitle_font = pygame.font.SysFont("Arial", int(title_font_size * 0.4), italic=True)
                subtitle_text = subtitle_font.render("Exciting new features coming soon!", True, (200, 200, 255))
                subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 130))  # Increased Y position from 110 to 130
                self.screen.blit(subtitle_text, subtitle_rect)
                
                # Draw content with scrolling
                heading_font = pygame.font.SysFont("Arial", heading_font_size, bold=True)
                text_font = pygame.font.SysFont("Arial", text_font_size + 2)  # Slightly larger text
                
                y_pos = 180 + scroll_y  # Increased starting position from 160 to 180 to accommodate subtitle
                content_height = 0
                
                # Content area with enhanced decorative border - better proportioned
                content_area = pygame.Rect(180, 160, screen_width - 360, screen_height - 240)  # More balanced padding
                
                # Draw decorative content area background with animated border
                border_color = (100, 150, 200, 100)
                
                # Create animated border
                border_width = 3  # Increased from 2 to 3
                border_pulse = (math.sin(animation_time * 2) + 1) / 2  # Value between 0 and 1
                border_alpha = int(100 + 100 * border_pulse)  # Pulsing transparency
                
                # Draw outer glow for content area
                for i in range(5, 0, -1):
                    glow_alpha = int(20 * (6-i) * border_pulse)
                    glow_rect = content_area.copy()
                    glow_rect.inflate_ip(i*2, i*2)
                    pygame.draw.rect(self.screen, (100, 150, 255, glow_alpha), glow_rect, border_radius=15)
                
                # Draw main border with animation
                pygame.draw.rect(self.screen, (border_color[0], border_color[1], border_color[2], border_alpha), 
                                content_area, border_width, border_radius=15)
                
                # Set clipping region to content area to ensure text stays within the box
                # Make the clipping region slightly larger vertically to allow for partial text rendering
                clip_rect = content_area.copy()
                clip_rect.y -= 15  # Extend 15 pixels above
                clip_rect.height += 30  # Extend 15 pixels below
                original_clip = self.screen.get_clip()
                self.screen.set_clip(clip_rect)
                
                # Add decorative corner accents
                corner_size = 20
                corner_positions = [
                    (content_area.left, content_area.top),  # Top-left
                    (content_area.right, content_area.top),  # Top-right
                    (content_area.left, content_area.bottom),  # Bottom-left
                    (content_area.right, content_area.bottom)  # Bottom-right
                ]
                
                for x, y in corner_positions:
                    # Draw corner accent with animation
                    accent_color = (200, 220, 255, border_alpha)
                    if (x == content_area.left and y == content_area.top) or (x == content_area.right and y == content_area.bottom):
                        # Top-left and bottom-right corners
                        pygame.draw.line(self.screen, accent_color, (x, y), (x + (corner_size if x == content_area.left else -corner_size), y), border_width)
                        pygame.draw.line(self.screen, accent_color, (x, y), (x, y + (corner_size if y == content_area.top else -corner_size)), border_width)
                    else:
                        # Top-right and bottom-left corners
                        pygame.draw.line(self.screen, accent_color, (x, y), (x + (corner_size if x == content_area.left else -corner_size), y), border_width)
                        pygame.draw.line(self.screen, accent_color, (x, y), (x, y + (corner_size if y == content_area.top else -corner_size)), border_width)
                
                for section in updates_content:
                    # Get the emoji from the section text to determine color
                    emoji = section["text"].split()[0]
                    heading_color = heading_colors.get(emoji, (135, 206, 250))  # Default to light sky blue
                    
                    # Draw section heading with enhanced background - SIMPLIFIED VERSION
                    # Calculate available width for heading
                    available_width = content_area.width - 100
                    
                    # Get the emoji from the section text
                    emoji = section["text"].split()[0]
                    heading_text_without_emoji = " ".join(section["text"].split()[1:])
                    
                    # Truncate heading text if needed
                    test_heading = heading_font.render(heading_text_without_emoji, True, heading_color)
                    if test_heading.get_width() > available_width:
                        # Calculate how many characters we can fit
                        char_ratio = available_width / test_heading.get_width()
                        max_chars = max(5, int(len(heading_text_without_emoji) * char_ratio) - 3)
                        heading_text_without_emoji = heading_text_without_emoji[:max_chars] + "..."
                    
                    # Render final heading with emoji
                    heading_text = heading_font.render(emoji + " " + heading_text_without_emoji, True, heading_color)
                    heading_rect = heading_text.get_rect(x=content_area.x + 60, y=y_pos)
                    
                    # Only draw if at least partially in view vertically
                    # More lenient check - draw if any part of the heading is in the content area vertically
                    if (y_pos + heading_rect.height > content_area.top - 10 and 
                        y_pos < content_area.bottom + 10):
                        # Draw heading background
                        bg_rect = heading_rect.copy()
                        bg_rect.inflate_ip(30, 15)
                        bg_rect.x -= 15
                        
                        # Make sure background stays within content area
                        if bg_rect.right > content_area.right - 20:
                            bg_rect.width = content_area.right - bg_rect.x - 20
                        
                        # Create simple background for heading
                        heading_bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                        heading_bg.fill((heading_color[0], heading_color[1], heading_color[2], 50))
                        
                        # Draw heading background
                        self.screen.blit(heading_bg, bg_rect)
                        
                        # Draw heading text with shadow for depth
                        shadow_text = heading_font.render(emoji + " " + heading_text_without_emoji, True, (0, 0, 0, 150))
                        shadow_rect = shadow_text.get_rect(x=heading_rect.x + 2, y=heading_rect.y + 2)
                        self.screen.blit(shadow_text, shadow_rect)
                        
                        # Draw main heading text
                        self.screen.blit(heading_text, heading_rect)
                    
                    y_pos += heading_rect.height + 25  # Increased spacing after headings from 20 to 25
                    content_height += heading_rect.height + 25
                    
                    # Draw section items with enhanced styling
                    for item_index, item in enumerate(section["items"]):
                        # Wrap text to fit within content area width
                        words = item.split()
                        lines = []
                        current_line = []
                        
                        # Split at the dash to highlight the feature name
                        feature_name = ""
                        feature_description = ""
                        if "–" in item:
                            parts = item.split("–", 1)
                            feature_name = parts[0].strip()
                            feature_description = "–" + parts[1].strip()
                            
                            # Add feature name as first line
                            lines.append(feature_name)
                            
                            # Process description for wrapping
                            words = feature_description.split()
                        
                        for word in words:
                            test_line = " ".join(current_line + [word])
                            test_width = text_font.size(test_line)[0]
                            
                            if test_width < screen_width - 500:  # More reasonable width limit
                                current_line.append(word)
                            else:
                                lines.append(" ".join(current_line))
                                current_line = [word]
                        
                        if current_line:
                            lines.append(" ".join(current_line))
                        
                        # Create item background with subtle animation
                        item_height = sum([text_font.size(line)[1] for line in lines]) + 8 * (len(lines) - 1) + 15
                        item_rect = pygame.Rect(200, y_pos - 5, screen_width - 480, item_height)  # Better proportioned width
                        
                        # Only draw if at least partially in view
                        if (item_rect.bottom > content_area.top - 15 and 
                            item_rect.top < content_area.bottom + 15):
                            # Alternate background colors for better readability
                            if item_index % 2 == 0:
                                # Create subtle animated background
                                item_alpha = 10 + int(5 * math.sin(animation_time + item_index * 0.2))
                                pygame.draw.rect(self.screen, (*heading_color, item_alpha), item_rect, border_radius=8)
                                
                                # Add subtle border
                                border_alpha = 20 + int(10 * math.sin(animation_time * 1.5 + item_index * 0.3))
                                pygame.draw.rect(self.screen, (*heading_color, border_alpha), item_rect, 1, border_radius=8)
                        
                        # Draw each line with improved styling - SIMPLIFIED VERSION
                        first_line = True
                        for line in lines:
                            # Determine if this is the feature name (first line when split)
                            is_feature_name = first_line and feature_name and line == feature_name
                            
                            # Choose color based on whether it's a feature name
                            line_color = text_highlight_color if is_feature_name else text_color
                            
                            # Set position based on whether this is first line or continuation
                            x_position = 200 if first_line else 220
                            
                            # HARD LIMIT: Truncate text to fixed maximum width
                            # Calculate available width within content area
                            available_width = content_area.right - x_position - 100
                            
                            # Render text to check its width
                            test_surface = text_font.render(line, True, line_color)
                            
                            # If text is too wide, truncate it
                            if test_surface.get_width() > available_width:
                                # Always truncate if too wide
                                char_ratio = available_width / test_surface.get_width()
                                max_chars = max(5, int(len(line) * char_ratio) - 3)
                                line = line[:max_chars] + "..."
                            
                            # Create final text surface
                            text_surface = text_font.render(line, True, line_color)
                            text_rect = text_surface.get_rect(x=x_position, y=y_pos)
                            
                            # Double-check that text is within content area horizontally
                            if text_rect.right > content_area.right - 20:
                                # If still too wide, skip this line
                                continue
                            
                            # Only draw if at least partially in view vertically
                            # More lenient check - draw if any part of the text is in the content area vertically
                            if (y_pos + text_rect.height > content_area.top - 10 and 
                                y_pos < content_area.bottom + 10):
                                # Draw text with subtle shadow for feature names
                                if is_feature_name:
                                    shadow_surface = text_font.render(line, True, (0, 0, 0, 100))
                                    shadow_rect = shadow_surface.get_rect(x=x_position + 1, y=y_pos + 1)
                                    self.screen.blit(shadow_surface, shadow_rect)
                                
                                # Draw bullet point for first line
                                if first_line:
                                    bullet_color = heading_color
                                    pygame.draw.circle(
                                        self.screen, 
                                        bullet_color,
                                        (x_position - 10, y_pos + text_surface.get_height()//2),
                                        4
                                    )
                                
                                # Draw the text
                                self.screen.blit(text_surface, text_rect)
                            
                            y_pos += text_rect.height + 10  # Increased line spacing
                            content_height += text_rect.height + 10
                            first_line = False
                        
                        y_pos += 20  # Increased spacing between items
                        content_height += 15
                    
                    y_pos += 30  # Increased space between sections from 20 to 30
                    content_height += 30
                
                # Calculate max scroll
                max_scroll = min(0, screen_height - 180 - content_height)
                
                # Restore original clipping region before drawing back button and scrollbar
                self.screen.set_clip(original_clip)
                
                # Draw back button with enhanced styling
                back_color = back_button_hover_color if back_button_hover else back_button_color
                
                # Draw button with gradient and glow
                button_surface = pygame.Surface((back_button_rect.width, back_button_rect.height), pygame.SRCALPHA)
                for i in range(back_button_rect.height):
                    # Create gradient effect
                    factor = i / back_button_rect.height
                    r = int(back_color[0] * (1 + factor * 0.3))
                    g = int(back_color[1] * (1 + factor * 0.3))
                    b = int(back_color[2] * (1 + factor * 0.3))
                    if r > 255: r = 255
                    if g > 255: g = 255
                    if b > 255: b = 255
                    pygame.draw.line(button_surface, (r, g, b), 
                                    (0, i), (back_button_rect.width, i))
                
                # Add button to screen with rounded corners
                button_rect = button_surface.get_rect(topleft=back_button_rect.topleft)
                pygame.draw.rect(self.screen, (0, 0, 0, 0), back_button_rect, border_radius=10)  # Clear area
                self.screen.blit(button_surface, button_rect)
                
                # Draw button border
                pygame.draw.rect(self.screen, (255, 255, 255, 100), back_button_rect, 2, border_radius=10)
                
                # Draw button text with slight shadow for depth
                back_font = pygame.font.SysFont("Arial", text_font_size, bold=True)
                shadow_text = back_font.render("Back", True, (0, 0, 0))
                shadow_rect = shadow_text.get_rect(center=(back_button_rect.center[0] + 2, back_button_rect.center[1] + 2))
                self.screen.blit(shadow_text, shadow_rect)
                
                back_text = back_font.render("Back", True, (255, 255, 255))
                back_text_rect = back_text.get_rect(center=back_button_rect.center)
                self.screen.blit(back_text, back_text_rect)
                
                # Draw scroll indicators if needed
                if max_scroll < 0:
                    # Calculate pulse effect for scroll indicators
                    pulse = (math.sin(animation_time * 3) + 1) / 2  # Value between 0 and 1
                    arrow_alpha = int(150 + 105 * pulse)  # Pulsing transparency
                    
                    if scroll_y < 0:
                        # Draw up arrow with glow effect
                        arrow_color = (200, 220, 255, arrow_alpha)
                        
                        # Draw arrow glow
                        for i in range(3, 0, -1):
                            glow_alpha = int(50 * (4-i) * pulse)
                            glow_color = (200, 220, 255, glow_alpha)
                            pygame.draw.polygon(
                                self.screen, glow_color, 
                                [(screen_width - 30 - i, 120 + i),
                                 (screen_width - 20, 100 - i * 2),
                                 (screen_width - 10 + i, 120 + i)]
                            )
                        
                        # Draw main arrow
                        pygame.draw.polygon(
                            self.screen, arrow_color, 
                            [(screen_width - 30, 120),
                             (screen_width - 20, 100),
                             (screen_width - 10, 120)]
                        )
                    
                    if scroll_y > max_scroll:
                        # Draw down arrow with glow effect
                        arrow_color = (200, 220, 255, arrow_alpha)
                        
                        # Draw arrow glow
                        for i in range(3, 0, -1):
                            glow_alpha = int(50 * (4-i) * pulse)
                            glow_color = (200, 220, 255, glow_alpha)
                            pygame.draw.polygon(
                                self.screen, glow_color, 
                                [(screen_width - 30 - i, screen_height - 120 - i),
                                 (screen_width - 20, screen_height - 100 + i * 2),
                                 (screen_width - 10 + i, screen_height - 120 - i)]
                            )
                        
                        # Draw main arrow
                        pygame.draw.polygon(
                            self.screen, arrow_color, 
                            [(screen_width - 30, screen_height - 120),
                             (screen_width - 20, screen_height - 100),
                             (screen_width - 10, screen_height - 120)]
                        )
                        
                    # Add scroll bar indicator
                    if content_height > 0:
                        
                        # Calculate scroll bar position and size
                        viewport_height = screen_height - 180
                        scroll_bar_height = max(30, viewport_height * (viewport_height / content_height))
                        scroll_position = (abs(scroll_y) / (content_height - viewport_height)) if content_height > viewport_height else 0
                        scroll_y_pos = 100 + scroll_position * (viewport_height - scroll_bar_height)
                        
                        # Draw scroll bar track
                        track_rect = pygame.Rect(screen_width - 15, 100, 5, viewport_height)
                        pygame.draw.rect(self.screen, (100, 100, 100, 50), track_rect, border_radius=2)
                        
                        # Draw scroll bar handle
                        handle_rect = pygame.Rect(screen_width - 15, scroll_y_pos, 5, scroll_bar_height)
                        pygame.draw.rect(self.screen, (200, 220, 255, 150), handle_rect, border_radius=2)
                
                # Update display
                pygame.display.flip()
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_UP:
                            scroll_y += scroll_speed
                            if scroll_y > 0:
                                scroll_y = 0
                        elif event.key == pygame.K_DOWN:
                            scroll_y -= scroll_speed
                            if scroll_y < max_scroll:
                                scroll_y = max_scroll
                                
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            if back_button_rect.collidepoint(event.pos):
                                running = False
                        elif event.button == 4:  # Mouse wheel up
                            scroll_y += scroll_speed
                            if scroll_y > 0:
                                scroll_y = 0
                        elif event.button == 5:  # Mouse wheel down
                            scroll_y -= scroll_speed
                            if scroll_y < max_scroll:
                                scroll_y = max_scroll
                                
                    elif event.type == pygame.MOUSEMOTION:
                        back_button_hover = back_button_rect.collidepoint(event.pos)
                
                clock.tick(60)
            except Exception as e:
                print(f"Error in updates menu: {e}")
                traceback.print_exc()
                return
                
        # Save scroll position for next time
        self.updates_menu_scroll_y = scroll_y
        return
    
    def show_settings_menu(self, background_surface):
        # Global variables that will be updated
        global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_X, SCALE_Y, LANE_WIDTH, LANE_POSITIONS
        
        # Add transition animation
        if hasattr(self, "transition"):
            self.transition.transition_type = "pixelate"
            self.transition.start(direction="in", duration=0.5)
            
        # Get current screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Create settings menu
        # Check if we\'re in fullscreen mode
        is_fullscreen = bool(pygame.display.get_surface().get_flags() & pygame.FULLSCREEN)
        
        # Create settings menu
        settings_menu = SettingsMenu(self.screen, screen_width, screen_height)
        
        # Update fullscreen setting to match current state
        settings_menu.current_values["FULLSCREEN"] = 1 if is_fullscreen else 0

        # Main settings menu loop
        clock = pygame.time.Clock()
        while True:
            try:
                # Restore the background
                self.screen.blit(background_surface, (0, 0))

                # Draw and handle the settings menu
                settings_menu.draw()
                result = settings_menu.handle_input()

                if result == "BACK":
                    # When returning from settings, make sure we have the correct screen
                    self.screen = pygame.display.get_surface()
                    return
                elif result == "EXIT":
                    pygame.quit()
                    sys.exit()
                elif result == "RESIZE" or result == "FULLSCREEN_CHANGED":
                    # Update the stored background after resize or fullscreen change
                    # Get the current screen surface which may have changed
                    self.screen = pygame.display.get_surface()
                    background_surface = self.screen.copy()
                    
                    # Update game dimensions
                    screen_width = self.screen.get_width()
                    screen_height = self.screen.get_height()
                    
                    # Update global variables to match new screen dimensions
                    SCREEN_WIDTH = screen_width
                    SCREEN_HEIGHT = screen_height
                    SCALE_X = SCREEN_WIDTH / BASE_WIDTH
                    SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
                    LANE_WIDTH = SCREEN_WIDTH // 6
                    LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]
                    
                    # Force a redraw of the screen to apply changes
                    pygame.display.flip()
                    
                    # Recreate settings menu with new dimensions
                    settings_menu = SettingsMenu(self.screen, screen_width, screen_height)

                    # Recreate the background surface for the new resolution
                    try:
                        # Try to load the background image
                        background_image = pygame.image.load("bgm.jpg")
                        # Scale the image to fit the new screen size
                        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        # Create a new background surface
                        background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                        background_surface.blit(background_image, (0, 0))
                        # Add semi-transparent overlay
                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 120))
                        background_surface.blit(overlay, (0, 0))
                    except Exception as e:
                        print(f"Error recreating background after resolution change: {e}")

                    LANE_POSITIONS = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(6)]

                clock.tick(30)
            except Exception as e:
                print(f"Error in settings menu: {e}")
                traceback.print_exc()
                return

    def get_sky_color(self, y_position):
        """Get the sky color at the given y position based on time of day"""
        # Calculate the ratio of y position (0 at top, 1 at bottom)
        ratio = y_position / SCREEN_HEIGHT

        # Determine the phase of day/night cycle
        if self.day_phase < 0.25:  # Day
            day_progress = self.day_phase / 0.25
            top_color = DAY_COLOR
            bottom_color = DAY_COLOR_BOTTOM
        elif self.day_phase < 0.5:  # Sunset
            sunset_progress = (self.day_phase - 0.25) / 0.25
            top_color = self.interpolate_color(
                DAY_COLOR, SUNRISE_COLOR, sunset_progress
            )
            bottom_color = self.interpolate_color(
                DAY_COLOR_BOTTOM, SUNRISE_COLOR_BOTTOM, sunset_progress
            )
        elif self.day_phase < 0.75:  # Night
            night_progress = (self.day_phase - 0.5) / 0.25
            top_color = self.interpolate_color(
                SUNRISE_COLOR, NIGHT_COLOR, night_progress
            )
            bottom_color = self.interpolate_color(
                SUNRISE_COLOR_BOTTOM, NIGHT_COLOR_BOTTOM, night_progress
            )
        else:  # Sunrise
            sunrise_progress = (self.day_phase - 0.75) / 0.25
            top_color = self.interpolate_color(NIGHT_COLOR, DAY_COLOR, sunrise_progress)
            bottom_color = self.interpolate_color(
                NIGHT_COLOR_BOTTOM, DAY_COLOR_BOTTOM, sunrise_progress
            )

        # Interpolate between top and bottom colors based on y position
        return self.interpolate_color(top_color, bottom_color, ratio)

    def interpolate_color(self, color1, color2, ratio):
        """Interpolate between two colors"""
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return (r, g, b)

    def draw_road(self):
        """Draw the road with optimized animations and visual effects"""
        # Use cached background if available for better performance
        if not hasattr(self, 'cached_background') or not hasattr(self, 'cached_day_phase') or abs(self.cached_day_phase - self.day_phase) > 0.05:  # Increased threshold from 0.01 to 0.05
            # Only recreate the background when the day phase changes significantly
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Use a more efficient approach with fewer color calculations
            top_color = self.get_sky_color(0)
            bottom_color = self.get_sky_color(SCREEN_HEIGHT)
            
            # Draw gradient with fewer steps
            steps = 10  # Reduced number of gradient steps
            for i in range(steps):
                y_start = i * SCREEN_HEIGHT // steps
                y_end = (i + 1) * SCREEN_HEIGHT // steps
                ratio = (i + 0.5) / steps
                
                # Interpolate color
                r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
                g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
                b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
                color = (r, g, b)
                
                # Fill rectangle instead of drawing individual lines
                pygame.draw.rect(background, color, (0, y_start, SCREEN_WIDTH, y_end - y_start))
            
            # Cache the background and day phase
            self.cached_background = background
            self.cached_day_phase = self.day_phase
        else:
            # Use the cached background
            background = self.cached_background

        self.screen.blit(background, (0, 0))

        # Draw stars if it's night time (between 0.5 and 1.0) - optimized
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
                # Only draw every third star to improve performance
                if i % 3 == 0:  # Changed from every other star to every third star
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
                    
                    # Only draw glow for very bright stars to reduce rendering load
                    if brightness > 0.85:  # Increased threshold from 0.7 to 0.85
                        glow_radius = star["size"] * 2
                        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                        glow_color = (255, 255, 255, int(50 * brightness))
                        pygame.draw.circle(
                            glow_surface,
                            glow_color,
                            (glow_radius, glow_radius),
                            glow_radius
                        )
                        self.screen.blit(
                            glow_surface,
                            (star["x"] - glow_radius, star["y"] - glow_radius)
                        )
                    
                    # Draw the star itself
                    pygame.draw.circle(
                        self.screen, color, (star["x"], star["y"]), star["size"]
                    )
                    
                    # Shooting stars are very rare and expensive to render - reduce frequency
                    if random.random() < 0.00005 and star_visibility > 0.9:  # Reduced from 0.0001 to 0.00005
                        self.create_shooting_star(star["x"], star["y"])

        # Draw lane markings with metallic effect - simplified
        for i in range(9):  # 8 lanes = 9 lines
            x = i * LANE_WIDTH
            pygame.draw.line(
                self.screen, METALLIC_SILVER, (x, 0), (x, SCREEN_HEIGHT), 3
            )

        # Draw dashed lines in the middle of lanes with neon effect
        # Use time-based animation for moving dashed lines
        line_offset = int((time.time() * self.speed * 20) % 80)  # Moving effect based on speed
        
        # Draw fewer dashed lines for better performance
        for i in range(1, 8, 2):  # Draw every other middle line (was 1-8)
            x = i * LANE_WIDTH
            
            # Draw dashed lines with animation - fewer lines
            for y in range(-line_offset, SCREEN_HEIGHT, 160):  # Increased spacing from 80 to 160
                # Simplified glow effect - only one layer instead of multiple
                glow_color = (255, 255, 255, 100)  # Simplified glow color
                
                # Create a surface for the glow
                glow_surface = pygame.Surface((10, 44), pygame.SRCALPHA)
                pygame.draw.rect(
                    glow_surface,
                    glow_color,
                    (0, 0, 10, 44),
                    0,
                    3  # Rounded corners
                )
                
                # Draw the glow
                self.screen.blit(
                    glow_surface,
                    (x - 5, y)
                )
                
                # Draw the main line
                pygame.draw.rect(
                    self.screen,
                    WHITE,
                    (x - 2, y, 4, 40),
                    0,
                    2  # Rounded corners
                )
    
    def create_shooting_star(self, x, y):
        """Create a shooting star animation"""
        if not hasattr(self, 'shooting_stars'):
            self.shooting_stars = []
            
        # Create a new shooting star
        angle = random.uniform(math.pi/4, math.pi/2)  # Angle between 45 and 90 degrees
        if random.random() < 0.5:
            angle = math.pi - angle  # 50% chance to go left instead of right
            
        speed = random.uniform(300, 500)
        length = random.uniform(50, 150)
        
        self.shooting_stars.append({
            'x': x,
            'y': y,
            'angle': angle,
            'speed': speed,
            'length': length,
            'width': random.uniform(1, 3),
            'time': 0,
            'duration': random.uniform(0.5, 1.5)
        })
    
    def update_shooting_stars(self, dt):
        """Update shooting star animations"""
        if not hasattr(self, 'shooting_stars'):
            return
            
        for star in self.shooting_stars[:]:
            star['time'] += dt
            
            # Remove if duration exceeded
            if star['time'] >= star['duration']:
                self.shooting_stars.remove(star)
                continue
                
            # Calculate current position
            progress = star['time'] / star['duration']
            distance = star['speed'] * progress
            
            # Calculate start and end points
            current_x = star['x'] + math.cos(star['angle']) * distance
            current_y = star['y'] + math.sin(star['angle']) * distance
            
            tail_x = current_x - math.cos(star['angle']) * star['length'] * (1 - progress)
            tail_y = current_y - math.sin(star['angle']) * star['length'] * (1 - progress)
            
            # Draw the shooting star
            # Create a surface for the glow
            glow_surface = pygame.Surface((int(star['length']*1.5), int(star['length']*1.5)), pygame.SRCALPHA)
            
            # Draw the tail with gradient
            points = []
            segments = 10
            for i in range(segments + 1):
                seg_progress = i / segments
                seg_x = tail_x + (current_x - tail_x) * seg_progress
                seg_y = tail_y + (current_y - tail_y) * seg_progress
                points.append((seg_x, seg_y))
                
                # Draw glow points
                if i % 2 == 0:  # Only every other point for performance
                    glow_alpha = int(255 * (1 - seg_progress) * (1 - progress))
                    glow_size = star['width'] * 3 * (1 - seg_progress)
                    glow_color = (255, 255, 255, glow_alpha)
                    
                    pygame.draw.circle(
                        self.screen,
                        glow_color,
                        (int(seg_x), int(seg_y)),
                        glow_size
                    )
            
            # Draw the main line
            if len(points) >= 2:
                # Calculate alpha based on progress
                line_alpha = int(255 * (1 - progress))
                line_color = (255, 255, 255, line_alpha)
                
                # Draw with pygame.draw.lines for better performance
                pygame.draw.lines(
                    self.screen,
                    line_color,
                    False,
                    points,
                    int(star['width'] * (1 - progress/2))
                )
    
    def add_road_detail(self):
        """Add a random road detail"""
        if not hasattr(self, 'road_details'):
            self.road_details = []
            
        # Limit the number of details for performance
        if len(self.road_details) >= 10:
            return
            
        # Choose a random lane
        lane = random.randint(0, 7)  # Updated for 8 lanes
        lane_x = lane * LANE_WIDTH
        
        # Choose a random detail type
        detail_type = random.choice(['crack', 'patch'])
        
        if detail_type == 'crack':
            # Create a zigzag crack
            points = []
            x_offset = random.randint(-LANE_WIDTH//3, LANE_WIDTH//3)
            y_start = -50  # Start above screen
            
            # Create zigzag points
            segments = random.randint(3, 7)
            segment_length = random.randint(10, 30)
            
            for i in range(segments):
                x_deviation = random.randint(-10, 10)
                points.append((x_offset + x_deviation, y_start + i * segment_length))
                
            # Add the detail
            self.road_details.append({
                'type': 'crack',
                'x_offset': lane_x,
                'y': y_start,
                'points': points,
                'width': random.randint(1, 3),
                'color': (80, 80, 80)
            })
        else:  # patch
            # Create a road patch
            width = random.randint(LANE_WIDTH//4, LANE_WIDTH//2)
            height = random.randint(20, 50)
            x = lane_x - width//2 + random.randint(-LANE_WIDTH//4, LANE_WIDTH//4)
            
            # Add the detail
            self.road_details.append({
                'type': 'patch',
                'x': x,
                'y': -height,
                'width': width,
                'height': height,
                'color': (70, 70, 70)
            })

    def draw(self):
        try:
            # Draw the road background
            self.draw_road()

            # Draw coins
            for coin in self.coins:
                coin.draw(self.screen)

            # Draw power-ups
            for powerup in self.powerups:
                powerup.draw(self.screen)

            # Draw player car (only if not in crash animation or at the beginning of it)
            if not hasattr(self, "crash_animation_timer") or (
                time.time() - self.crash_animation_timer < 0.3
            ):
                self.player_car.draw(self.screen)

            # Draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

            # Draw other cars
            for car in self.other_cars:
                car.draw(self.screen)

            # Draw particles
            self.particle_system.draw(self.screen)

            # If in crash animation, add special effects
            if hasattr(self, "crash_animation_timer"):
                # Calculate how far into the animation we are
                elapsed = time.time() - self.crash_animation_timer
                progress = elapsed / 2.0  # 2.0 seconds total (changed from 1.5)

                # Add dramatic slow-motion effect
                if progress < 0.8:
                    # Create a red flash overlay that fades out
                    flash_alpha = max(0, int(255 * (0.8 - progress) / 0.8))
                    flash_overlay = pygame.Surface(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                    )
                    flash_overlay.fill((255, 0, 0, flash_alpha))
                    self.screen.blit(flash_overlay, (0, 0))

                    # Add screen shake effect
                    if progress < 0.5:
                        shake_amount = int(10 * (0.5 - progress) / 0.5)
                        shake_x = random.randint(-shake_amount, shake_amount)
                        shake_y = random.randint(-shake_amount, shake_amount)

                        # Create a copy of the screen and shift it
                        screen_copy = self.screen.copy()
                        self.screen.fill(BLACK)
                        self.screen.blit(screen_copy, (shake_x, shake_y))

                # Add time slowdown visual effect
                if progress < 0.7:
                    for i in range(5):
                        y = random.randint(0, SCREEN_HEIGHT)
                        width = random.randint(100, SCREEN_WIDTH)
                        height = random.randint(1, 3)
                        alpha = random.randint(30, 100)
                        distortion = pygame.Surface((width, height), pygame.SRCALPHA)
                        distortion.fill((255, 255, 255, alpha))
                        self.screen.blit(
                            distortion, (random.randint(0, SCREEN_WIDTH - width), y)
                        )

                # Draw "CRASH!" text with animation
                if 0.3 < progress < 0.9:
                    # Calculate text size and alpha based on animation progress
                    text_progress = min(1.0, (progress - 0.3) / 0.3)
                    text_size = int(72 * text_progress)
                    if text_size < 10:
                        text_size = 10

                    crash_font = get_font(text_size, bold=True)
                    crash_text = crash_font.render("CRASH!", True, BRIGHT_RED)
                    text_rect = crash_text.get_rect(
                        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    )

                    # Add glow effect
                    for offset in range(5, 0, -1):
                        glow_rect = text_rect.copy()
                        glow_rect.inflate_ip(offset * 4, offset * 4)
                        pygame.draw.rect(
                            self.screen,
                            (255, offset * 20, 0),
                            glow_rect,
                            2,
                            border_radius=10,
                        )

                    self.screen.blit(crash_text, text_rect)

                # Fade to black at the end of the animation
                if progress > 0.8:
                    fade_progress = min(1.0, (progress - 0.8) / 0.2)
                    fade_alpha = int(255 * fade_progress)
                    fade_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    fade_overlay.fill(BLACK)
                    fade_overlay.set_alpha(fade_alpha)
                    self.screen.blit(fade_overlay, (0, 0))

            # Apply night time overlay if it's night
            if 0.5 <= self.day_phase < 0.75:
                # Calculate darkness level (0 at sunset/sunrise, 1 at full night)
                darkness = 0
                if 0.5 <= self.day_phase < 0.625:
                    darkness = (self.day_phase - 0.5) * 8  # Fade to dark
                elif 0.625 <= self.day_phase < 0.75:
                    darkness = (0.75 - self.day_phase) * 8  # Fade to light

                # Create a semi-transparent dark overlay
                night_overlay = pygame.Surface(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                )
                night_overlay.fill((0, 0, 20, int(100 * darkness)))  # Blue-ish darkness
                self.screen.blit(night_overlay, (0, 0))

            # Create a semi-transparent UI overlay at the top
            ui_height = 80
            ui_surface = pygame.Surface((SCREEN_WIDTH, ui_height), pygame.SRCALPHA)
            ui_surface.fill(
                (MATTE_BLACK[0], MATTE_BLACK[1], MATTE_BLACK[2], 180)
            )  # Semi-transparent
            self.screen.blit(ui_surface, (0, 0))

            # Draw score with electric purple glow
            score_font = get_font(36, bold=True)
            score_text = score_font.render(
                f"SCORE: {self.score}", True, ELECTRIC_PURPLE
            )
            score_shadow = score_font.render(
                f"SCORE: {self.score}",
                True,
                (
                    ELECTRIC_PURPLE[0] // 3,
                    ELECTRIC_PURPLE[1] // 3,
                    ELECTRIC_PURPLE[2] // 3,
                ),
            )
            self.screen.blit(score_shadow, (12, 12))  # Shadow effect
            self.screen.blit(score_text, (10, 10))

            # Draw combo and multiplier if active
            if self.combo_count > 0:
                combo_text = score_font.render(
                    f"COMBO: {self.combo_count} x{self.score_multiplier}",
                    True,
                    NEON_YELLOW,
                )
                combo_shadow = score_font.render(
                    f"COMBO: {self.combo_count} x{self.score_multiplier}",
                    True,
                    (NEON_YELLOW[0] // 3, NEON_YELLOW[1] // 3, NEON_YELLOW[2] // 3),
                )
                self.screen.blit(combo_shadow, (SCREEN_WIDTH - 252, 12))
                self.screen.blit(combo_text, (SCREEN_WIDTH - 250, 10))

            # Draw coins collected
            coin_text = score_font.render(
                f"COINS: {self.coins_collected}", True, COIN_COLOR
            )
            coin_shadow = score_font.render(
                f"COINS: {self.coins_collected}",
                True,
                (COIN_COLOR[0] // 3, COIN_COLOR[1] // 3, COIN_COLOR[2] // 3),
            )
            self.screen.blit(coin_shadow, (12, 52))
            self.screen.blit(coin_text, (10, 50))

            # Draw speed with neon green effect
            # Calculate the actual displayed speed, including boost effect
            if self.player_car.has_boost:
                speed_value = min(int(self.speed * BOOST_MULTIPLIER * 10), 300)  # Cap at 300 km/h
            else:
                speed_value = int(self.speed * 10)
                
            speed_text = score_font.render(
                f"SPEED: {speed_value} km/h", True, NEON_GREEN
            )
            speed_shadow = score_font.render(
                f"SPEED: {speed_value} km/h",
                True,
                (NEON_GREEN[0] // 3, NEON_GREEN[1] // 3, NEON_GREEN[2] // 3),
            )
            self.screen.blit(
                speed_shadow, (SCREEN_WIDTH // 2 - 102, 12)
            )  # Shadow effect
            self.screen.blit(speed_text, (SCREEN_WIDTH // 2 - 100, 10))

            # Draw time of day indicator
            time_of_day_labels = ["DAY", "SUNSET", "NIGHT", "SUNRISE"]
            time_index = int(self.day_phase * 4) % 4
            time_label = time_of_day_labels[time_index]

            # Choose color based on time of day
            if time_index == 0:  # Day
                time_color = NEON_GREEN
            elif time_index == 1:  # Sunset
                time_color = ORANGE
            elif time_index == 2:  # Night
                time_color = (100, 100, 255)  # Light blue
            else:  # Sunrise
                time_color = YELLOW

            time_text = score_font.render(f"TIME: {time_label}", True, time_color)
            time_shadow = score_font.render(
                f"TIME: {time_label}",
                True,
                (time_color[0] // 3, time_color[1] // 3, time_color[2] // 3),
            )
            self.screen.blit(time_shadow, (SCREEN_WIDTH // 2 - 102, 52))
            self.screen.blit(time_text, (SCREEN_WIDTH // 2 - 100, 50))

            # Draw pause button
            pause_button_rect = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)
            pygame.draw.rect(self.screen, DEEP_BLUE, pause_button_rect, border_radius=5)
            pygame.draw.rect(
                self.screen, NEON_YELLOW, pause_button_rect, 2, border_radius=5
            )

            # Draw pause symbol
            pygame.draw.rect(self.screen, NEON_YELLOW, (SCREEN_WIDTH - 40, 18, 8, 24))
            pygame.draw.rect(self.screen, NEON_YELLOW, (SCREEN_WIDTH - 28, 18, 8, 24))

            # Draw game mode specific UI
            if self.game_mode == GAME_MODE_TIME_ATTACK:
                # Draw time remaining
                time_text = score_font.render(
                    f"TIME: {int(self.time_remaining)}s", True, BRIGHT_RED
                )
                time_shadow = score_font.render(
                    f"TIME: {int(self.time_remaining)}s",
                    True,
                    (BRIGHT_RED[0] // 3, BRIGHT_RED[1] // 3, BRIGHT_RED[2] // 3),
                )
                self.screen.blit(time_shadow, (SCREEN_WIDTH - 152, 52))
                self.screen.blit(time_text, (SCREEN_WIDTH - 150, 50))
            elif self.game_mode == GAME_MODE_MISSIONS:
                # Draw mission progress
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
                self.screen.blit(mission_text, (SCREEN_WIDTH // 2 - 200, 50))

            # Draw speed indicator bar
            max_speed = 300  # Maximum expected speed (increased from 150)
            bar_width = 200
            bar_height = 15
            bar_x = SCREEN_WIDTH - bar_width - 20
            bar_y = 50

            # Background bar
            pygame.draw.rect(
                self.screen, SLEEK_SILVER, (bar_x, bar_y, bar_width, bar_height), 0, 5
            )

            # Speed fill - use the same speed_value that includes boost effect
            speed_ratio = min(speed_value / max_speed, 1.0)
            speed_width = int(bar_width * speed_ratio)

            # Gradient color for speed bar based on speed
            if speed_ratio < 0.3:
                bar_color = NEON_GREEN
            elif speed_ratio < 0.7:
                bar_color = NEON_YELLOW
            else:
                bar_color = BRIGHT_RED

            pygame.draw.rect(
                self.screen, bar_color, (bar_x, bar_y, speed_width, bar_height), 0, 5
            )

            # Add a border to the speed bar
            pygame.draw.rect(
                self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1, 5
            )

            # Apply slow motion effect if active
            if self.player_car.has_slow_mo:
                slow_mo_overlay = pygame.Surface(
                    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
                )
                slow_mo_overlay.fill(
                    (SLOW_MO_COLOR[0], SLOW_MO_COLOR[1], SLOW_MO_COLOR[2], 30)
                )
                self.screen.blit(slow_mo_overlay, (0, 0))

                # Add time distortion visual effect
                for i in range(10):
                    y = random.randint(0, SCREEN_HEIGHT)
                    width = random.randint(50, 200)
                    height = random.randint(1, 3)
                    alpha = random.randint(20, 80)
                    distortion = pygame.Surface((width, height), pygame.SRCALPHA)
                    distortion.fill((255, 255, 255, alpha))
                    self.screen.blit(
                        distortion, (random.randint(0, SCREEN_WIDTH - width), y)
                    )

            # Draw prompts if available
            if hasattr(self, "prompt_system"):
                self.prompt_system.draw()
                
            # Draw "AKD" text in the bottom right corner
            akd_font = get_font(16)
            akd_text = akd_font.render("AKD", True, (255, 255, 255, 180))
            akd_rect = akd_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
            self.screen.blit(akd_text, akd_rect)

            # Draw transition effects if active
            if hasattr(self, "transition") and self.transition.running:
                self.transition.draw()

            pygame.display.flip()
        except Exception as e:
            print(f"Error in draw method: {e}")
            traceback.print_exc()

    def update(self):
        try:
            # If game is over and we're showing the crash animation
            if self.game_over and hasattr(self, "crash_animation_timer"):
                current_time = time.time()
                elapsed = current_time - self.crash_animation_timer

                # Stop engine sound if it was playing
                if hasattr(self, "engine_channel") and self.engine_playing:
                    self.engine_channel.stop()
                    self.engine_playing = False

                # Continue showing the crash animation for 2 seconds (changed from 1.5)
                if elapsed < 2.0:
                    # Create additional particles for dramatic effect
                    if random.random() < 0.3:
                        self.particle_system.create_crash(
                            self.crash_position[0] + random.uniform(-20, 20),
                            self.crash_position[1] + random.uniform(-20, 20),
                        )
                    # Update particles
                    self.particle_system.update(0.016)  # ~60fps
                    return
                else:
                    # Animation finished, remove the timer and proceed to menu
                    delattr(self, "crash_animation_timer")
                    return

            # If game is over but no animation is playing, just return
            elif self.game_over:
                # Make sure engine sound is stopped
                if hasattr(self, "engine_channel") and self.engine_playing:
                    self.engine_channel.stop()
                    self.engine_playing = False
                return

            # Calculate delta time
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

            # Handle welcome prompt timer
            if hasattr(self, "welcome_prompt_timer"):
                self.welcome_prompt_timer -= dt
                if self.welcome_prompt_timer <= 0:
                    self.prompt_system.show_prompt("welcome")
                    delattr(self, "welcome_prompt_timer")

            # Play or update engine sound
            if (
                sound_enabled
                and hasattr(self, "engine_channel")
                and hasattr(self, "sound_engine")
            ):
                # Start engine sound if not already playing
                if not self.engine_playing:
                    self.engine_channel.play(
                        self.sound_engine, loops=-1
                    )  # Loop indefinitely
                    self.engine_playing = True

                # Adjust engine sound pitch based on speed
                # Note: This is a simplified version as pygame doesn't directly support pitch shifting
                # In a real implementation, you might use multiple engine sound samples
                # or a more advanced audio library that supports real-time pitch shifting
                speed_ratio = self.speed / 15.0  # Normalized speed (0-1)
                volume = (
                    0.2 + speed_ratio * 0.5
                )  # Volume increases with speed (0.2-0.7)
                if hasattr(self, "sound_engine"):
                    self.sound_engine.set_volume(volume)

            # Update prompt system
            if hasattr(self, "prompt_system"):
                self.prompt_system.update()

            # Update day-night cycle
            self.cycle_time += dt
            self.day_phase = (
                self.cycle_time % DAY_NIGHT_CYCLE_DURATION
            ) / DAY_NIGHT_CYCLE_DURATION

            # Update player car
            self.player_car.update(dt)

            # Update particle system
            self.particle_system.update(dt)

            # Create boost trail if boosting
            if self.player_car.is_boosting:
                boost_x = self.player_car.x
                boost_y = self.player_car.y + self.player_car.height // 2

                # Reduced particle effects for better performance
                if random.random() < 0.4:  # Reduced from 0.7
                    self.particle_system.create_boost_trail(boost_x, boost_y)

                # Add occasional sparks for a more dynamic effect (reduced frequency)
                if random.random() < 0.15:  # Reduced from 0.3
                    self.particle_system.create_spark(
                        boost_x + random.uniform(-10, 10),
                        boost_y + random.uniform(-5, 5),
                        count=3,  # Reduced from 5
                        intensity=0.8,
                    )

            # Apply slow motion if active
            speed_factor = SLOW_MO_FACTOR if self.player_car.has_slow_mo else 1.0

            # Apply boost if active
            if self.player_car.has_boost:
                speed_factor *= BOOST_MULTIPLIER

            # Increase speed over time
            self.speed += SPEED_INCREMENT * speed_factor

            # Cap speed at 30 (which will display as 300 km/h)
            if self.speed > 30:
                self.speed = 30

            # Ensure speed doesn't drop too low when slowing down
            if self.speed < 5:  # Minimum speed of 50 km/h
                self.speed = 5

            # Update distance traveled
            self.distance_traveled += (
                self.speed * dt * 10
            )  # 10 meters per unit of speed

            # Update time remaining for time attack mode
            if self.game_mode == GAME_MODE_TIME_ATTACK:
                self.time_remaining -= dt
                if self.time_remaining <= 0:
                    self.game_over = True
                    self.game_has_been_played = True  # Mark that a game has been played
                    # Play game over sound
                    if sound_enabled and hasattr(self, "sound_game_over"):
                        self.sound_game_over.play()

            # Update mission progress
            self.update_mission_progress()

            # Update combo timer
            if self.combo_timer > 0:
                self.combo_timer -= dt
                if self.combo_timer <= 0:
                    self.combo_count = 0
                    self.score_multiplier = 1

            # Generate new obstacles
            if current_time - self.last_obstacle_time > random.uniform(3.0, 6.0):  # Further increased spawn interval
                # Check if there are too many obstacles already
                if len(self.obstacles) < 2:  # Reduced max obstacles from 3 to 2
                    # Choose a lane that doesn't already have an obstacle or car nearby
                    available_lanes = list(range(8))  # Updated for 8 lanes
                    
                    # Remove lanes that have obstacles
                    for obstacle in self.obstacles:
                        if obstacle.lane in available_lanes:
                            available_lanes.remove(obstacle.lane)
                            # Also remove adjacent lanes for better spacing
                            if obstacle.lane > 0 and obstacle.lane - 1 in available_lanes:
                                available_lanes.remove(obstacle.lane - 1)
                            if obstacle.lane < 7 and obstacle.lane + 1 in available_lanes:  # Updated for 8 lanes
                                available_lanes.remove(obstacle.lane + 1)
                    
                    # Remove lanes that have cars near the top
                    for car in self.other_cars:
                        if car.y < 200:  # Only check cars near the top of the screen
                            if car.lane in available_lanes:
                                available_lanes.remove(car.lane)
                    
                    # If there are available lanes, create an obstacle
                    if available_lanes:
                        lane = random.choice(available_lanes)
                        # Reduced chance of moving obstacles which are more CPU intensive
                        if random.random() < 0.2:  # Reduced from 0.3
                            self.obstacles.append(MovingObstacle(lane))
                        else:
                            self.obstacles.append(Obstacle(lane))
                        self.last_obstacle_time = current_time

            # Generate other cars
            if current_time - self.last_car_time > random.uniform(4.0, 8.0):  # Further increased spawn interval
                # Check if there are too many cars already
                if len(self.other_cars) < 2:  # Reduced max cars from 3 to 2
                    # Choose a lane that doesn't already have a car or obstacle nearby
                    available_lanes = list(range(8))  # Updated for 8 lanes
                    
                    # Remove lanes that have cars
                    for car in self.other_cars:
                        if car.lane in available_lanes:
                            available_lanes.remove(car.lane)
                            # Also remove adjacent lanes for better spacing
                            if car.lane > 0 and car.lane - 1 in available_lanes:
                                available_lanes.remove(car.lane - 1)
                            if car.lane < 7 and car.lane + 1 in available_lanes:  # Updated for 8 lanes
                                available_lanes.remove(car.lane + 1)
                    
                    # Remove lanes that have obstacles near the top
                    for obstacle in self.obstacles:
                        if obstacle.y < 200:  # Only check obstacles near the top of the screen
                            if obstacle.lane in available_lanes:
                                available_lanes.remove(obstacle.lane)
                    
                    # If there are available lanes, create a car
                    if available_lanes:
                        lane = random.choice(available_lanes)
                        # Reduced chance of AI-controlled cars which are more CPU intensive
                        if random.random() < 0.3:  # Reduced from 0.5
                            self.other_cars.append(AIControlledCar(lane))
                        else:
                            self.other_cars.append(OtherCar(lane))
                        self.last_car_time = current_time

            # Generate new power-ups
            if current_time - self.last_powerup_time > random.uniform(5.0, 15.0):
                lane = random.randint(0, 7)  # Updated for 8 lanes
                powerup_type = random.choice(["boost", "shield", "magnet", "slow_mo"])
                self.powerups.append(PowerUp(lane, powerup_type))
                self.last_powerup_time = current_time

            # Generate new coins
            if current_time - self.last_coin_time > random.uniform(1.0, 3.0):  # Increased interval
                # Limit the number of coins on screen
                if len(self.coins) < 6:  # Reduced for performance  # Add a limit to coins
                    lane = random.randint(0, 7)  # Updated for 8 lanes
                    x = LANE_POSITIONS[lane] + random.randint(
                        -LANE_WIDTH // 4, LANE_WIDTH // 4
                    )
                    self.coins.append(Coin(x, -20))
                    self.last_coin_time = current_time

            # Update moving obstacles
            for obstacle in self.obstacles[:]:
                if isinstance(obstacle, MovingObstacle):
                    obstacle.update(dt)

            # Update AI cars
            for car in self.other_cars[:]:
                if isinstance(car, AIControlledCar):
                    car.update(dt, self.player_car.lane, self.obstacles + self.other_cars)

            # Move obstacles
            for obstacle in self.obstacles[:]:
                obstacle.move(self.speed * speed_factor)
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    # Add to combo for avoiding obstacle
                    self.combo_count += 1
                    self.combo_timer = 2.0
                    # Update score multiplier
                    if self.combo_count >= 10:
                        self.score_multiplier = 3
                    elif self.combo_count >= 5:
                        self.score_multiplier = 2

                    # Show combo prompt if it's a significant combo
                    if hasattr(self, "prompt_system") and self.combo_count == 5:
                        self.prompt_system.show_prompt("combo")
                elif obstacle.collides_with(self.player_car):
                    if self.player_car.has_shield:
                        # Shield protects from collision
                        self.obstacles.remove(obstacle)
                        self.score += 2
                        # Add to combo
                        self.combo_count += 2
                        self.combo_timer = 2.0
                        # Create spark effect for shield collision
                        self.particle_system.create_spark(
                            obstacle.x, obstacle.y, count=15
                        )
                        # Play shield sound
                        if sound_enabled and hasattr(self, "sound_shield"):
                            self.sound_shield.play()
                    else:
                        # Store crash position for animation
                        self.crash_position = (self.player_car.x, self.player_car.y)
                        # Create crash effect
                        self.particle_system.create_crash(
                            self.player_car.x, self.player_car.y
                        )
                        # Play crash sound
                        if sound_enabled and hasattr(self, "sound_crash"):
                            self.sound_crash.play()
                        self.game_over = True
                        self.game_has_been_played = True  # Mark that a game has been played
                        # Start crash animation timer
                        self.crash_animation_timer = time.time()
                        # Play game over sound
                        if sound_enabled and hasattr(self, "sound_game_over"):
                            self.sound_game_over.play()

            # Move other cars
            for car in self.other_cars[:]:
                # Apply braking for AI cars
                speed_modifier = (
                    0.5 if isinstance(car, AIControlledCar) and car.is_braking else 0.8
                )
                car.move(self.speed * speed_factor * speed_modifier)

                if car.is_off_screen():
                    self.other_cars.remove(car)
                    self.score += 2 * self.score_multiplier
                    # Add to combo
                    self.combo_count += 1
                    self.combo_timer = 2.0
                elif car.collides_with(self.player_car):
                    if self.player_car.has_shield:
                        # Shield protects from collision
                        self.other_cars.remove(car)
                        self.score += 3
                        # Add to combo
                        self.combo_count += 2
                        self.combo_timer = 2.0
                        # Create spark effect for shield collision
                        self.particle_system.create_spark(car.x, car.y, count=20)
                        # Play shield sound
                        if sound_enabled and hasattr(self, "sound_shield"):
                            self.sound_shield.play()
                    else:
                        # Store crash position for animation
                        self.crash_position = (self.player_car.x, self.player_car.y)
                        # Create crash effect
                        self.particle_system.create_crash(
                            self.player_car.x, self.player_car.y
                        )
                        # Play crash sound
                        if sound_enabled and hasattr(self, "sound_crash"):
                            self.sound_crash.play()
                        self.game_over = True
                        self.game_has_been_played = True  # Mark that a game has been played
                        # Start crash animation timer
                        self.crash_animation_timer = time.time()
                        # Play game over sound
                        if sound_enabled and hasattr(self, "sound_game_over"):
                            self.sound_game_over.play()

            # Move and check power-ups
            for powerup in self.powerups[:]:
                powerup.move(self.speed * speed_factor)
                if powerup.is_off_screen():
                    self.powerups.remove(powerup)
                elif powerup.collides_with(self.player_car):
                    powerup.collect()
                    self.powerups.remove(powerup)

                    # Apply power-up effect
                    if powerup.type == "boost":
                        self.player_car.activate_boost()
                        # Create spark effect for boost activation
                        self.particle_system.create_spark(
                            self.player_car.x,
                            self.player_car.y + self.player_car.height // 2,
                            count=15,
                        )
                        # Play boost sound
                        if sound_enabled and hasattr(self, "sound_boost"):
                            self.sound_boost.play()
                        # Show boost prompt
                        if hasattr(self, "prompt_system"):
                            self.prompt_system.show_prompt("powerup_boost")
                    elif powerup.type == "shield":
                        self.player_car.activate_shield()
                        # Play shield sound
                        if sound_enabled and hasattr(self, "sound_shield"):
                            self.sound_shield.play()
                        # Show shield prompt
                        if hasattr(self, "prompt_system"):
                            self.prompt_system.show_prompt("powerup_shield")
                    elif powerup.type == "magnet":
                        self.player_car.activate_magnet()
                        # Play powerup sound
                        if sound_enabled and hasattr(self, "sound_powerup"):
                            self.sound_powerup.play()
                        # Show magnet prompt
                        if hasattr(self, "prompt_system"):
                            self.prompt_system.show_prompt("powerup_magnet")
                    elif powerup.type == "slow_mo":
                        self.player_car.activate_slow_mo()
                        # Play powerup sound
                        if sound_enabled and hasattr(self, "sound_powerup"):
                            self.sound_powerup.play()
                        # Show slow-mo prompt
                        if hasattr(self, "prompt_system"):
                            self.prompt_system.show_prompt("powerup_slow_mo")

                    # Add points for collecting power-up
                    self.score += 5 * self.score_multiplier
                    # Add to combo
                    self.combo_count += 1
                    self.combo_timer = 2.0
                    # Track power-ups used for missions
                    self.powerups_used += 1

            # Move and check coins
            for coin in self.coins[:]:
                coin.move(self.speed * speed_factor)

                # Check if coin is in magnet range
                if self.player_car.has_magnet:
                    dx = self.player_car.x - coin.x
                    dy = self.player_car.y - coin.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < MAGNET_RANGE:
                        # Move coin towards player
                        angle = math.atan2(dy, dx)
                        coin.x += math.cos(angle) * 5
                        coin.y += math.sin(angle) * 5

                if coin.is_off_screen():
                    self.coins.remove(coin)
                elif coin.collides_with(self.player_car):
                    coin.collect()
                    self.coins.remove(coin)
                    self.coins_collected += 1

                    # Create spark effect for coin collection
                    self.particle_system.create_spark(coin.x, coin.y, count=5)

                    # Play coin sound
                    if sound_enabled and hasattr(self, "sound_coin"):
                        self.sound_coin.play()

                    # Add points for collecting coin with combo multiplier
                    self.score += COIN_VALUE * self.score_multiplier

                    # Increase combo
                    self.combo_count += 1
                    self.combo_timer = 2.0  # Reset combo timer

                    # Update score multiplier
                    if self.combo_count >= 10:
                        self.score_multiplier = 3
                    elif self.combo_count >= 5:
                        self.score_multiplier = 2
                    else:
                        self.score_multiplier = 1

                    # Add boost energy
                    self.player_car.add_boost_energy(5)

                    # Show boost energy prompt when energy is full
                    if (
                        hasattr(self, "prompt_system")
                        and self.player_car.boost_energy
                        >= self.player_car.max_boost_energy
                    ):
                        self.prompt_system.show_prompt("boost_energy")

            # Check if mission is complete and show prompt
            if (
                self.game_mode == GAME_MODE_MISSIONS
                and self.mission_progress >= self.mission_target
            ):
                if hasattr(self, "prompt_system"):
                    self.prompt_system.show_prompt("mission_complete")

        except Exception as e:
            print(f"Error in update method: {e}")
            traceback.print_exc()

    def show_menu(self):
        print("Opening main menu...")

        # Create a fade-in transition effect
        if hasattr(self, "transition"):
            self.transition.transition_type = "fade"
            self.transition.start(direction="in", duration=0.5)

        # Start playing menu music if not already playing
        if (
            sound_enabled
            and music_enabled
            and hasattr(self, "menu_music_channel")
            and not self.menu_music_playing
        ):
            try:
                # Load menu music
                menu_music = pygame.mixer.Sound(self.SOUND_MENU_MUSIC)
                menu_music.set_volume(0.4)  # Set appropriate volume
                self.menu_music_channel.play(menu_music, loops=-1)  # Loop indefinitely
                self.menu_music_playing = True
                print("Menu music started")
            except Exception as e:
                print(f"Error playing menu music: {e}")

        # Load background image
        try:
            # Try to load the background image
            background_image = pygame.image.load("bgm.jpg")
            # Get screen dimensions for proper scaling
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            # Scale the image to fit the screen exactly
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
            print("Background image loaded successfully")
            has_background_image = True
        except Exception as e:
            print(f"Error loading background image: {e}")
            has_background_image = False
            
            # Create gradient background as fallback
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                # Calculate gradient color
                r = int(DEEP_BLUE[0])
                g = int(DEEP_BLUE[1])
                b = int(DEEP_BLUE[2])
                pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Add some decorative elements (even if we have the background image)
        if not has_background_image:
            # Add stars only if using the gradient background
            for i in range(20):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(1, 3)
                pygame.draw.circle(background, SLEEK_SILVER, (x, y), size)

            # Draw some decorative lines
            for i in range(5):
                start_x = random.randint(0, SCREEN_WIDTH)
                end_x = random.randint(0, SCREEN_WIDTH)
                pygame.draw.line(
                    background, NEON_YELLOW, (start_x, 0), (end_x, SCREEN_HEIGHT), 1
                )

        title_font = get_font(min(72, SCREEN_HEIGHT // 12), bold=True)  # Responsive title font
        menu_font = get_font(min(48, SCREEN_HEIGHT // 18))  # Responsive menu font

        # Draw title
        title_text = title_font.render("CAR RACING", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

        # Create menu options
        options = [
            ("GAME MODES", ELECTRIC_PURPLE, -2),
            ("NEW GAME", NEON_YELLOW, -1),
            ("GARAGE", NEON_GREEN, -5),  # Garage option with key code -5
            ("UPDATES", NEON_GREEN, -6),  # New Updates option with key code -6
            ("OPTIONS", NEON_GREEN, -4),
            ("HIGH SCORES", NEON_GREEN, -3),
            ("EXIT", BRIGHT_RED, pygame.K_ESCAPE),
        ]

        # Main menu loop
        running = True
        clock = pygame.time.Clock()

        # Track the last selected option to detect changes
        last_selected = -1

        while running:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Update sparkles
            dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
            self.update_sparkles(dt)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Stop menu music if playing
                    if (
                        sound_enabled
                        and hasattr(self, "menu_music_channel")
                        and self.menu_music_playing
                    ):
                        self.menu_music_channel.stop()
                        self.menu_music_playing = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Stop menu music if playing
                        if (
                            sound_enabled
                            and hasattr(self, "menu_music_channel")
                            and self.menu_music_playing
                        ):
                            self.menu_music_channel.stop()
                            self.menu_music_playing = False
                        return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for i, (rect, key) in enumerate(button_rects):
                            if rect.collidepoint(event.pos):
                                # Play selection sound
                                if sound_enabled and hasattr(self, "sound_menu_select"):
                                    self.sound_menu_select.play()

                                if key == -1:  # New Game (Endless mode)
                                    print("Starting new game in Endless mode")
                                    # Stop menu music when starting game
                                    if (
                                        sound_enabled
                                        and hasattr(self, "menu_music_channel")
                                        and self.menu_music_playing
                                    ):
                                        self.menu_music_channel.stop()
                                        self.menu_music_playing = False
                                    self.game_mode = GAME_MODE_ENDLESS
                                    self.reset_game()
                                    return True
                                elif key == -2:  # Game Modes
                                    print("Opening game modes menu")
                                    return self.show_game_mode_menu()
                                elif key == -3:  # High Scores
                                    print("Opening high scores")
                                    self.show_highscores()
                                    # Continue showing menu after high scores
                                    continue
                                elif key == -4:  # Options
                                    print("Opening options menu")
                                    # Create a background surface for the settings menu
                                    # Instead of using a copy of the current screen, we'll redraw the menu
                                    # when we return from the settings menu
                                    background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                                    if has_background_image:
                                        background_surface.blit(background_image, (0, 0))
                                        # Add semi-transparent overlay
                                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                        overlay.fill((0, 0, 0, 120))
                                        background_surface.blit(overlay, (0, 0))
                                    else:
                                        background_surface.blit(background, (0, 0))
                                    
                                    self.show_settings_menu(background_surface)
                                    # Continue showing menu after options
                                    continue
                                elif key == -5:  # Garage
                                    print("Opening garage")
                                    # Create a background surface for the garage menu
                                    background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                                    if has_background_image:
                                        background_surface.blit(background_image, (0, 0))
                                        # Add semi-transparent overlay
                                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                        overlay.fill((0, 0, 0, 120))
                                        background_surface.blit(overlay, (0, 0))
                                    else:
                                        background_surface.blit(background, (0, 0))
                                    
                                    self.show_garage_menu(background_surface)
                                    # Continue showing menu after garage
                                    continue
                                elif key == -6:  # Updates
                                    print("Opening updates")
                                    # Create a background surface for the updates menu
                                    background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                                    if has_background_image:
                                        background_surface.blit(background_image, (0, 0))
                                        # Add semi-transparent overlay
                                        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                        overlay.fill((0, 0, 0, 120))
                                        background_surface.blit(overlay, (0, 0))
                                    else:
                                        background_surface.blit(background, (0, 0))
                                    
                                    self.show_updates_menu(background_surface)
                                    # Continue showing menu after updates
                                    continue
                                elif key == pygame.K_ESCAPE:
                                    # Stop menu music if playing
                                    if (
                                        sound_enabled
                                        and hasattr(self, "menu_music_channel")
                                        and self.menu_music_playing
                                    ):
                                        self.menu_music_channel.stop()
                                        self.menu_music_playing = False
                                    return False

            # Draw background
            if has_background_image:
                # Use the loaded image as background
                # Get current screen dimensions to ensure proper scaling
                current_width = self.screen.get_width()
                current_height = self.screen.get_height()
                
                # Check if the background image needs to be rescaled
                if background_image.get_width() != current_width or background_image.get_height() != current_height:
                    background_image = pygame.transform.scale(background_image, (current_width, current_height))
                    print(f"Background image rescaled to {current_width}x{current_height}")
                
                self.screen.blit(background_image, (0, 0))
                
                # Add a semi-transparent overlay to make text more readable
                overlay = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))  # Semi-transparent black
                self.screen.blit(overlay, (0, 0))
                
                # Draw sparkles animation
                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
                self.draw_sparkles(self.screen)
                
                # Draw sparkles animation
                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
                self.draw_sparkles(self.screen)
            else:
                # Use the gradient background
                self.screen.blit(background, (0, 0))

            # Draw title - without box/glow effect
            self.screen.blit(title_text, title_rect)

            # Draw game over text if applicable
            if self.game_over and hasattr(self, 'game_has_been_played') and self.game_has_been_played:
                # Add faster blinking effect to game over text
                blink_rate = 1.2  # Faster blink rate (in seconds)
                blink_value = (math.sin(pygame.time.get_ticks() * 0.001 * blink_rate) + 1) / 2  # Value between 0 and 1
                
                # Only show text when blink_value is above threshold (creates blinking effect)
                if blink_value > 0.2:  # Show text most of the time with brief disappearances
                    # Calculate alpha based on blink value for smooth fade in/out
                    text_alpha = int(255 * min(1.0, blink_value * 1.8))
                    
                    # Create game over text with appropriate alpha
                    game_over_surface = pygame.Surface(title_font.size("GAME OVER"), pygame.SRCALPHA)
                    temp_text = title_font.render("GAME OVER", True, BRIGHT_RED)
                    game_over_surface.blit(temp_text, (0, 0))
                    game_over_surface.set_alpha(text_alpha)
                    
                    # Position the text with more space from title
                    game_over_rect = game_over_surface.get_rect(
                        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 20)  # Added 20px more space from title
                    )
                    
                    # Add glow effect to game over text - intensity varies with blink
                    glow_intensity = blink_value * 1.2  # Intensify the glow effect
                    for offset in range(8, 0, -1):
                        glow_rect = game_over_rect.copy()
                        glow_rect.inflate_ip(offset * 3 * glow_intensity, offset * 3 * glow_intensity)
                        glow_color = (
                            min(BRIGHT_RED[0], 255),
                            min(BRIGHT_RED[1] + int(offset * 5 * glow_intensity), 255),
                            min(BRIGHT_RED[2] + int(offset * 5 * glow_intensity), 255),
                        )
                        pygame.draw.rect(
                            self.screen,
                            glow_color,
                            glow_rect,
                            2,
                            border_radius=5,
                        )
                    
                    # Draw the game over text
                    self.screen.blit(game_over_surface, game_over_rect)
                
                # Score text doesn't blink - always visible
                stats_font = get_font(min(36, SCREEN_HEIGHT // 24))  # Smaller font for stats
                score_text = stats_font.render(
                    f"FINAL SCORE: {self.score}", True, NEON_YELLOW
                )
                score_rect = score_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 90)  # Slightly reduced spacing
                )
                self.screen.blit(score_text, score_rect)
                
                # Coin count text - always visible after game over
                coin_text = stats_font.render(
                    f"💰 COINS COLLECTED: {self.coins_collected}", True, COIN_COLOR
                )
                coin_rect = coin_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 125)  # Adjusted spacing
                )
                
                # Add a subtle glow effect to the coin text
                for offset in range(2, 0, -1):  # Reduced glow effect
                    glow_color = (
                        min(COIN_COLOR[0], 255),
                        min(COIN_COLOR[1] + offset * 10, 255),
                        min(COIN_COLOR[2] + offset * 10, 255),
                    )
                    glow_text = stats_font.render(
                        f"💰 COINS COLLECTED: {self.coins_collected}", True, glow_color
                    )
                    glow_rect = coin_rect.copy()
                    glow_rect.inflate_ip(offset * 2, offset * 2)
                    self.screen.blit(glow_text, glow_rect)
                
                self.screen.blit(coin_text, coin_rect)
                
                # Distance traveled text
                distance_text = stats_font.render(
                    f"🏁 DISTANCE: {int(self.distance_traveled)}m", True, NEON_GREEN
                )
                distance_rect = distance_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 160)  # Adjusted spacing
                )
                self.screen.blit(distance_text, distance_rect)

            # Draw menu buttons
            button_rects = []
            currently_selected = -1

            # Calculate starting position for menu buttons to avoid overlap with game over stats
            if self.game_over and hasattr(self, 'game_has_been_played') and self.game_has_been_played:
                # If game over stats are shown, start menu buttons after the stats with minimum spacing
                stats_end_y = SCREEN_HEIGHT // 3 + 160  # After distance text (updated position)
                min_spacing = 60  # Good spacing between stats and menu
                menu_start_y = stats_end_y + min_spacing
            else:
                # Normal menu without game over stats - add more space from title
                menu_start_y = SCREEN_HEIGHT // 2 + 20  # Added 20px more space

            # Ensure menu doesn't go off screen - adjust spacing if needed
            menu_items_count = len(options)
            menu_spacing = 60  # Reduced from 65 to ensure better fit
            total_menu_height = menu_items_count * menu_spacing
            
            if menu_start_y + total_menu_height > SCREEN_HEIGHT - 80:  # Increased bottom margin
                # Reduce spacing if menu would go off screen
                available_height = SCREEN_HEIGHT - 80 - menu_start_y
                menu_spacing = max(40, available_height // menu_items_count)  # Minimum 40px spacing

            for i, (text, color, key) in enumerate(options):
                option_text = menu_font.render(text, True, color)
                option_rect = option_text.get_rect(
                    center=(SCREEN_WIDTH // 2, menu_start_y + menu_spacing * i)
                )

                button_rect = option_rect.copy()
                button_rect.inflate_ip(40, 20)
                button_rects.append((button_rect, key))

                is_hovering = button_rect.collidepoint(mouse_pos)

                if is_hovering:
                    currently_selected = i
                    hover_color = (
                        min(color[0] + 50, 255),
                        min(color[1] + 50, 255),
                        min(color[2] + 50, 255),
                    )

                    # Pulsating effect
                    pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2

                    # Create text with hover color and slight glow effect
                    option_text = menu_font.render(text, True, hover_color)
                    
                    # Add subtle glow effect around text
                    glow_size = int(2 + pulse)
                    for dx in range(-glow_size, glow_size+1, 2):
                        for dy in range(-glow_size, glow_size+1, 2):
                            if dx*dx + dy*dy <= glow_size*glow_size:
                                glow_text = menu_font.render(text, True, (hover_color[0], hover_color[1], hover_color[2], 50))
                                glow_rect = option_rect.copy()
                                glow_rect.x += dx
                                glow_rect.y += dy
                                self.screen.blit(glow_text, glow_rect)
                else:
                    # Create text with original color - no button background or border
                    option_text = menu_font.render(text, True, color)

                self.screen.blit(option_text, option_rect)
                # Add sparkle effect around menu items
                if is_hovering:
                    # Create sparkles around the button when hovering
                    # Reduced from 2 to 1 sparkle per frame
                    if random.random() < 0.5:  # Only 50% chance to create a sparkle each frame
                        # Calculate random position around the button
                        sparkle_x = button_rect.x + random.randint(-10, button_rect.width + 10)
                        sparkle_y = button_rect.y + random.randint(-10, button_rect.height + 10)
                        
                        # Add sparkle with color matching the button
                        self.sparkles.append({
                            "x": sparkle_x,
                            "y": sparkle_y,
                            "direction": random.uniform(0, 2 * math.pi),
                            "speed": random.uniform(0.2, 1.0),
                            "color": hover_color,
                            "size": random.uniform(1, 3),
                            "brightness": random.uniform(0.5, 1.0),
                            "twinkle_speed": random.uniform(3, 8),
                            "twinkle_offset": random.uniform(0, 2 * math.pi),
                        })


            # Play sound if selection changed
            if currently_selected != -1 and currently_selected != last_selected:
                if sound_enabled and hasattr(self, "sound_menu_navigate"):
                    self.sound_menu_navigate.play()
                last_selected = currently_selected
                
            # Draw "AKD" text in the bottom right corner
            akd_font = get_font(16)
            akd_text = akd_font.render("AKD", True, (255, 255, 255, 180))
            akd_rect = akd_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
            self.screen.blit(akd_text, akd_rect)

            pygame.display.flip()
            clock.tick(60)

        return False

    def start_new_game(self, game_mode):
        """Helper method to start a new game with transition effects"""
        try:
            print(f"Starting new game with mode: {game_mode}")
            
            # Create a transition effect based on game mode
            if hasattr(self, "transition"):
                if game_mode == GAME_MODE_ENDLESS:
                    self.transition.transition_type = "fade"
                    self.transition.transition_color = (0, 0, 0)  # Black
                elif game_mode == GAME_MODE_TIME_ATTACK:
                    self.transition.transition_type = "slide_left"
                    self.transition.transition_color = (50, 0, 50)  # Dark purple
                elif game_mode == GAME_MODE_MISSIONS:
                    self.transition.transition_type = "zoom"
                    self.transition.transition_color = (0, 50, 0)  # Dark green
                elif game_mode == GAME_MODE_RACE:
                    self.transition.transition_type = "radial"
                    self.transition.transition_color = (50, 0, 0)  # Dark red
                
                # Start the transition
                self.transition.start(direction="in", duration=0.7)
            
            self.game_mode = game_mode
            self.reset_game()
            return True
        except Exception as e:
            print(f"Error starting new game: {e}")
            traceback.print_exc()
            return False

    def show_items_menu(self, background_surface):
        """Show the items menu for power-ups and collectibles"""
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
        
        # Available items with their stats and descriptions
        items = [
            {
                "name": "BOOST",
                "color": BOOST_COLOR,
                "symbol": "⚡",
                "description": "Increases your speed for a short time.",
                "effect": "Speed x1.5 for 5 seconds"
            },
            {
                "name": "SHIELD",
                "color": SHIELD_COLOR,
                "symbol": "🛡️",
                "description": "Protects your car from crashes.",
                "effect": "Immunity for 7 seconds"
            },
            {
                "name": "MAGNET",
                "color": MAGNET_COLOR,
                "symbol": "🧲",
                "description": "Attracts coins to your car.",
                "effect": "150px attraction radius for 5 seconds"
            },
            {
                "name": "SLOW-MO",
                "color": SLOW_MO_COLOR,
                "symbol": "⏱️",
                "description": "Slows down time for better control.",
                "effect": "50% slower gameplay for 5 seconds"
            },
            {
                "name": "COIN",
                "color": COIN_COLOR,
                "symbol": "💰",
                "description": "Collect to increase your score.",
                "effect": "+10 points per coin"
            }
        ]
        
        # Current item index
        current_item = 0
        
        # Create item images
        item_images = []
        for item in items:
            # Create a surface for the item
            item_width = 80
            item_height = 80
            img = pygame.Surface((item_width, item_height), pygame.SRCALPHA)
            
            # Draw the item with glow effect
            for offset in range(3, 0, -1):
                glow_color = (*item["color"], 100 - offset * 30)
                pygame.draw.circle(
                    img,
                    glow_color,
                    (item_width // 2, item_height // 2),
                    item_width // 2 - offset * 2
                )
            
            # Draw main item
            pygame.draw.circle(
                img,
                item["color"],
                (item_width // 2, item_height // 2),
                item_width // 2 - 6
            )
            
            # Draw symbol
            symbol_font = get_font(30, bold=True)
            symbol_text = symbol_font.render(item["symbol"], True, WHITE)
            symbol_rect = symbol_text.get_rect(center=(item_width // 2, item_height // 2))
            img.blit(symbol_text, symbol_rect)
            
            item_images.append(img)
        
        # Main items menu loop
        clock = pygame.time.Clock()
        running = True
        
        # Create button rectangles
        back_button_rect = pygame.Rect(0, 0, 100, 40)
        back_button_rect.center = (screen_width // 2, screen_height - 100)
        
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
                        # Previous item
                        current_item = (current_item - 1) % len(items)
                        # Play selection sound
                        if sound_enabled and hasattr(self, "sound_menu_navigate"):
                            self.sound_menu_navigate.play()
                    elif event.key == pygame.K_RIGHT:
                        # Next item
                        current_item = (current_item + 1) % len(items)
                        # Play selection sound
                        if sound_enabled and hasattr(self, "sound_menu_navigate"):
                            self.sound_menu_navigate.play()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if back button was clicked
                        if back_button_rect.collidepoint(event.pos):
                            # Play selection sound
                            if sound_enabled and hasattr(self, "sound_menu_select"):
                                self.sound_menu_select.play()
                            return
                        # Check if left arrow was clicked
                        elif left_arrow_rect.collidepoint(event.pos):
                            # Previous item
                            current_item = (current_item - 1) % len(items)
                            # Play selection sound
                            if sound_enabled and hasattr(self, "sound_menu_navigate"):
                                self.sound_menu_navigate.play()
                        # Check if right arrow was clicked
                        elif right_arrow_rect.collidepoint(event.pos):
                            # Next item
                            current_item = (current_item + 1) % len(items)
                            # Play selection sound
                            if sound_enabled and hasattr(self, "sound_menu_navigate"):
                                self.sound_menu_navigate.play()
            
            # Draw background
            self.screen.blit(background_surface, (0, 0))
            
            # Draw sparkles animation
            self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
            self.draw_sparkles(self.screen)
            
            # Draw title
            title_text = title_font.render("ITEMS", True, NEON_YELLOW)
            title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 6))
            self.screen.blit(title_text, title_rect)
            
            # Draw item image
            item_image_rect = item_images[current_item].get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            self.screen.blit(item_images[current_item], item_image_rect)
            
            # Draw item name
            item_name_text = menu_font.render(items[current_item]["name"], True, ELECTRIC_PURPLE)
            item_name_rect = item_name_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            self.screen.blit(item_name_text, item_name_rect)
            
            # Draw item description
            desc_text = info_font.render(items[current_item]["description"], True, WHITE)
            desc_rect = desc_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            self.screen.blit(desc_text, desc_rect)
            
            # Draw item effect
            effect_text = info_font.render(items[current_item]["effect"], True, SLEEK_SILVER)
            effect_rect = effect_text.get_rect(center=(screen_width // 2, screen_height // 2 + 130))
            self.screen.blit(effect_text, effect_rect)
            
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
            
            # Draw back button
            back_text = menu_font.render("BACK", True, BRIGHT_RED)
            back_button_rect = back_text.get_rect(center=(screen_width // 2, screen_height - 100))
            self.screen.blit(back_text, back_button_rect)
            
            # Draw item selection indicators
            indicator_y = screen_height - 50
            for i in range(len(items)):
                if i == current_item:
                    # Current item indicator
                    pygame.draw.circle(self.screen, NEON_YELLOW, 
                                      (screen_width // 2 - (len(items) - 1) * 15 + i * 30, indicator_y), 8)
                else:
                    # Other item indicator
                    pygame.draw.circle(self.screen, SLEEK_SILVER, 
                                      (screen_width // 2 - (len(items) - 1) * 15 + i * 30, indicator_y), 5)
            
            # Update display
            pygame.display.flip()
            clock.tick(60)

    def show_garage_menu(self, background_surface):
        """Show the garage menu for car selection and customization with transition animation"""
        # Add transition animation
        if hasattr(self, "transition"):
            self.transition.transition_type = "zoom"
            self.transition.start(direction="in", duration=0.5)
            
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
        
        # Available cars with their stats - same car design, different colors
        cars = [
            {
                "name": "RED RACER",
                "speed": 8,
                "acceleration": 9,
                "handling": 7,
                "color": (255, 0, 0),  # Red
                "description": "Fast and agile sports car with excellent acceleration."
            },
            {
                "name": "BLUE BOLT",
                "speed": 9,
                "acceleration": 7,
                "handling": 6,
                "color": (0, 0, 255),  # Blue
                "description": "Powerful sports car with high top speed."
            },
            {
                "name": "GREEN MACHINE",
                "speed": 6,
                "acceleration": 6,
                "handling": 9,
                "color": (0, 255, 0),  # Green
                "description": "Nimble sports car with excellent handling."
            },
            {
                "name": "YELLOW FLASH",
                "speed": 7,
                "acceleration": 8,
                "handling": 7,
                "color": (255, 255, 0),  # Yellow
                "description": "Well-balanced sports car with good all-around stats."
            },
            {
                "name": "PURPLE PHANTOM",
                "speed": 8,
                "acceleration": 8,
                "handling": 8,
                "color": (128, 0, 128),  # Purple
                "description": "Premium sports car with balanced performance."
            }
        ]
        
        # Current car index - use selected_car if available
        if hasattr(self, 'selected_car') and self.selected_car is not None:
            current_car = self.selected_car
        else:
            current_car = 0
        
        # Create a background for the car display area
        car_display_bg = pygame.Surface((screen_width * 0.6, screen_height * 0.4), pygame.SRCALPHA)
        car_display_bg.fill((30, 30, 50, 180))  # Semi-transparent dark blue background
        
        # Draw a grid pattern on the background
        grid_spacing = 20
        for x in range(0, int(screen_width * 0.6), grid_spacing):
            pygame.draw.line(car_display_bg, (50, 50, 70, 100), (x, 0), (x, screen_height * 0.4), 1)
        for y in range(0, int(screen_height * 0.4), grid_spacing):
            pygame.draw.line(car_display_bg, (50, 50, 70, 100), (0, y), (screen_width * 0.6, y), 1)
        
        # Create car images - using a completely different approach for better visibility
        car_images = []
        for car in cars:
            # Create a larger surface for the car
            car_width = int(screen_width * 0.4)  # 40% of screen width
            car_height = int(car_width * 0.5)    # Maintain aspect ratio
            img = pygame.Surface((car_width, car_height), pygame.SRCALPHA)
            
            # Draw the car body
            car_body_width = car_width * 0.8
            car_body_height = car_height * 0.5
            car_body_x = (car_width - car_body_width) / 2
            car_body_y = car_height * 0.3
            
            # Car shadow (for depth)
            shadow_offset = car_height * 0.05
            shadow_surface = pygame.Surface((car_body_width, car_body_height), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 100))
            img.blit(shadow_surface, (car_body_x + shadow_offset, car_body_y + shadow_offset))
            
            # Main car body (bottom part)
            pygame.draw.rect(
                img,
                car["color"],
                [car_body_x, car_body_y, car_body_width, car_body_height],
                0,
                int(car_width * 0.05)  # Rounded corners
            )
            
            # Add metallic effect with gradient
            highlight_color = (
                min(car["color"][0] + 60, 255),
                min(car["color"][1] + 60, 255),
                min(car["color"][2] + 60, 255),
            )
            
            # Top part of car (hood, roof, trunk)
            top_height = car_height * 0.2
            top_y = car_body_y - top_height
            
            # Hood
            hood_width = car_body_width * 0.8
            hood_x = car_body_x + (car_body_width - hood_width) / 2
            pygame.draw.rect(
                img,
                highlight_color,
                [hood_x, top_y, hood_width, top_height],
                0,
                int(car_width * 0.03)  # Rounded corners
            )
            
            # Windshield (angled)
            windshield_points = [
                (hood_x + hood_width * 0.1, top_y + top_height),  # Bottom left
                (hood_x + hood_width * 0.3, top_y),               # Top left
                (hood_x + hood_width * 0.7, top_y),               # Top right
                (hood_x + hood_width * 0.9, top_y + top_height)   # Bottom right
            ]
            pygame.draw.polygon(
                img,
                (100, 200, 255),  # Blue windshield
                windshield_points
            )
            
            # Windows (side)
            window_height = car_body_height * 0.3
            window_y = car_body_y + car_body_height * 0.1
            
            # Left window
            pygame.draw.rect(
                img,
                (150, 230, 255),  # Light blue window
                [car_body_x, window_y, car_body_width * 0.15, window_height],
                0,
                int(car_width * 0.01)  # Rounded corners
            )
            
            # Right window
            pygame.draw.rect(
                img,
                (150, 230, 255),  # Light blue window
                [car_body_x + car_body_width * 0.85, window_y, car_body_width * 0.15, window_height],
                0,
                int(car_width * 0.01)  # Rounded corners
            )
            
            # Wheels - larger and more detailed
            wheel_radius = car_height * 0.15
            wheel_y = car_body_y + car_body_height - wheel_radius * 0.7
            
            wheel_positions = [
                # Front wheel
                car_body_x + car_body_width * 0.2,
                # Rear wheel
                car_body_x + car_body_width * 0.8
            ]
            
            # Draw wheels with rims
            for wheel_x in wheel_positions:
                # Tire
                pygame.draw.circle(
                    img,
                    BLACK,
                    (int(wheel_x), int(wheel_y)),
                    int(wheel_radius)
                )
                
                # Rim
                pygame.draw.circle(
                    img,
                    SLEEK_SILVER,
                    (int(wheel_x), int(wheel_y)),
                    int(wheel_radius * 0.6)
                )
                
                # Hub
                pygame.draw.circle(
                    img,
                    (100, 100, 100),
                    (int(wheel_x), int(wheel_y)),
                    int(wheel_radius * 0.2)
                )
                
                # Spokes
                for angle in range(0, 360, 45):
                    spoke_x = wheel_x + math.cos(math.radians(angle)) * wheel_radius * 0.5
                    spoke_y = wheel_y + math.sin(math.radians(angle)) * wheel_radius * 0.5
                    pygame.draw.line(
                        img,
                        SLEEK_SILVER,
                        (int(wheel_x), int(wheel_y)),
                        (int(spoke_x), int(spoke_y)),
                        int(wheel_radius * 0.1)
                    )
            
            # Headlights with glow effect
            headlight_radius = car_height * 0.08
            headlight_y = car_body_y + car_body_height * 0.2
            
            headlight_positions = [
                # Left headlight
                car_body_x + car_body_width * 0.1,
                # Right headlight
                car_body_x + car_body_width * 0.9
            ]
            
            for headlight_x in headlight_positions:
                # Headlight glow
                for offset in range(3, 0, -1):
                    glow_radius = headlight_radius + offset * 2
                    glow_alpha = 150 - offset * 40
                    glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(
                        glow_surface,
                        (255, 255, 150, glow_alpha),
                        (glow_radius, glow_radius),
                        glow_radius
                    )
                    img.blit(
                        glow_surface,
                        (int(headlight_x - glow_radius), int(headlight_y - glow_radius))
                    )
                
                # Headlight
                pygame.draw.circle(
                    img,
                    NEON_YELLOW,
                    (int(headlight_x), int(headlight_y)),
                    int(headlight_radius)
                )
            
            # Taillights
            taillight_radius = car_height * 0.06
            taillight_y = car_body_y + car_body_height * 0.2
            
            taillight_positions = [
                # Left taillight
                car_body_x + car_body_width * 0.05,
                # Right taillight
                car_body_x + car_body_width * 0.95
            ]
            
            for taillight_x in taillight_positions:
                # Taillight glow
                for offset in range(2, 0, -1):
                    glow_radius = taillight_radius + offset * 2
                    glow_alpha = 100 - offset * 30
                    glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(
                        glow_surface,
                        (255, 50, 50, glow_alpha),
                        (glow_radius, glow_radius),
                        glow_radius
                    )
                    img.blit(
                        glow_surface,
                        (int(taillight_x - glow_radius), int(taillight_y + car_body_height * 0.6 - glow_radius))
                    )
                
                # Taillight
                pygame.draw.circle(
                    img,
                    BRIGHT_RED,
                    (int(taillight_x), int(taillight_y + car_body_height * 0.6)),
                    int(taillight_radius)
                )
            
            # Add details - door lines
            door_y = car_body_y + car_body_height * 0.4
            pygame.draw.line(
                img,
                (car["color"][0] * 0.7, car["color"][1] * 0.7, car["color"][2] * 0.7),
                (int(car_body_x + car_body_width * 0.4), int(door_y)),
                (int(car_body_x + car_body_width * 0.4), int(door_y + car_body_height * 0.4)),
                2
            )
            
            # Add details - door handles
            handle_width = car_body_width * 0.05
            handle_height = car_body_height * 0.03
            handle_y = car_body_y + car_body_height * 0.35
            
            # Left door handle
            pygame.draw.rect(
                img,
                SLEEK_SILVER,
                [car_body_x + car_body_width * 0.25, handle_y, handle_width, handle_height],
                0,
                int(handle_height * 0.5)  # Rounded corners
            )
            
            # Right door handle
            pygame.draw.rect(
                img,
                SLEEK_SILVER,
                [car_body_x + car_body_width * 0.65, handle_y, handle_width, handle_height],
                0,
                int(handle_height * 0.5)  # Rounded corners
            )
            
            # Add car name on the side
            name_font = get_font(int(car_height * 0.1))
            name_text = name_font.render(car["name"].split()[0], True, (255, 255, 255, 150))
            name_rect = name_text.get_rect(center=(car_body_x + car_body_width * 0.5, car_body_y + car_body_height * 0.7))
            img.blit(name_text, name_rect)
            
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
            
            # Draw car display background
            car_display_rect = car_display_bg.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            self.screen.blit(car_display_bg, car_display_rect)
            
            # Draw car image
            car_image_rect = car_images[current_car].get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            self.screen.blit(car_images[current_car], car_image_rect)
            
            # Draw car name
            car_name_text = menu_font.render(cars[current_car]["name"], True, ELECTRIC_PURPLE)
            car_name_rect = car_name_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            self.screen.blit(car_name_text, car_name_rect)
            
            # Draw car stats
            stats_y = screen_height // 2 + 150
            stats_spacing = 30
            
            # Speed stat
            speed_text = info_font.render(f"Speed: {cars[current_car]['speed']}/10", True, WHITE)
            speed_rect = speed_text.get_rect(center=(screen_width // 2, stats_y))
            self.screen.blit(speed_text, speed_rect)
            
            # Speed bar
            bar_width = 200
            bar_height = 10
            bar_x = screen_width // 2 - bar_width // 2
            bar_y = stats_y + 15
            
            # Background bar
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), 0, 5)
            
            # Filled bar
            fill_width = int(bar_width * cars[current_car]['speed'] / 10)
            pygame.draw.rect(self.screen, NEON_GREEN, (bar_x, bar_y, fill_width, bar_height), 0, 5)
            
            # Acceleration stat
            accel_text = info_font.render(f"Acceleration: {cars[current_car]['acceleration']}/10", True, WHITE)
            accel_rect = accel_text.get_rect(center=(screen_width // 2, stats_y + stats_spacing))
            self.screen.blit(accel_text, accel_rect)
            
            # Acceleration bar
            bar_y = stats_y + stats_spacing + 15
            
            # Background bar
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), 0, 5)
            
            # Filled bar
            fill_width = int(bar_width * cars[current_car]['acceleration'] / 10)
            pygame.draw.rect(self.screen, NEON_YELLOW, (bar_x, bar_y, fill_width, bar_height), 0, 5)
            
            # Handling stat
            handling_text = info_font.render(f"Handling: {cars[current_car]['handling']}/10", True, WHITE)
            handling_rect = handling_text.get_rect(center=(screen_width // 2, stats_y + 2 * stats_spacing))
            self.screen.blit(handling_text, handling_rect)
            
            # Handling bar
            bar_y = stats_y + 2 * stats_spacing + 15
            
            # Background bar
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), 0, 5)
            
            # Filled bar
            fill_width = int(bar_width * cars[current_car]['handling'] / 10)
            pygame.draw.rect(self.screen, ELECTRIC_PURPLE, (bar_x, bar_y, fill_width, bar_height), 0, 5)
            
            # Draw car description
            desc_text = info_font.render(cars[current_car]["description"], True, SLEEK_SILVER)
            desc_rect = desc_text.get_rect(center=(screen_width // 2, stats_y + 3 * stats_spacing + 10))
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

    def show_game_mode_menu(self):
        """Show the game mode selection menu with transition animation"""
        print("Opening game mode menu...")

        # Create a slide transition effect
        if hasattr(self, "transition"):
            self.transition.transition_type = "slide_left"
            self.transition.start(direction="in", duration=0.4)

        # Ensure menu music is playing
        if (
            sound_enabled
            and music_enabled
            and hasattr(self, "menu_music_channel")
            and not self.menu_music_playing
        ):
            try:
                # Load menu music
                menu_music = pygame.mixer.Sound(self.SOUND_MENU_MUSIC)
                menu_music.set_volume(0.4)  # Set appropriate volume
                self.menu_music_channel.play(menu_music, loops=-1)  # Loop indefinitely
                self.menu_music_playing = True
                print("Menu music started")
            except Exception as e:
                print(f"Error playing menu music: {e}")

        # Try to load the background image
        try:
            background_image = pygame.image.load("bgm.jpg")
            background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            has_background_image = True
        except Exception as e:
            print(f"Error loading background image for game mode menu: {e}")
            has_background_image = False
            
            # Create background with gradient as fallback
            background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            for y in range(SCREEN_HEIGHT):
                # Calculate gradient color - slightly different from main menu
                r = int(DEEP_BLUE[0] * 1.2)
                g = int(DEEP_BLUE[1] * 1.2)
                b = int(DEEP_BLUE[2] * 1.2)
                pygame.draw.line(
                    background,
                    (min(r, 255), min(g, 255), min(b, 255)),
                    (0, y),
                    (SCREEN_WIDTH, y),
                )

        # Add decorative elements (only if using gradient background)
        if not has_background_image:
            for i in range(30):  # More stars than main menu
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(1, 4)
                pygame.draw.circle(background, SLEEK_SILVER, (x, y), size)

        title_font = get_font(72, bold=True)
        menu_font = get_font(48)

        # Draw title
        title_text = title_font.render("SELECT GAME MODE", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))

        # Game mode options
        options = [
            ("ENDLESS", NEON_GREEN, GAME_MODE_ENDLESS),
            ("TIME ATTACK", ELECTRIC_PURPLE, GAME_MODE_TIME_ATTACK),
            ("MISSIONS", NEON_YELLOW, GAME_MODE_MISSIONS),
            ("BACK", BRIGHT_RED, -1),
        ]

        button_rects = []

        # Track the last selected option to detect changes
        last_selected = -1

        # Main game mode menu loop
        running = True
        clock = pygame.time.Clock()

        while running:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Update sparkles
            dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
            self.update_sparkles(dt)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Stop menu music if playing
                    if (
                        sound_enabled
                        and hasattr(self, "menu_music_channel")
                        and self.menu_music_playing
                    ):
                        self.menu_music_channel.stop()
                        self.menu_music_playing = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Play menu sound
                        if sound_enabled and hasattr(self, "sound_menu_select"):
                            self.sound_menu_select.play()
                        print("Returning to main menu from game mode menu")
                        return self.show_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for rect, mode in button_rects:
                            if rect.collidepoint(event.pos):
                                # Play selection sound
                                if sound_enabled and hasattr(self, "sound_menu_select"):
                                    self.sound_menu_select.play()

                                if mode == -1:
                                    print("Returning to main menu from game mode menu")
                                    return self.show_menu()
                                else:
                                    print(f"Selected game mode: {mode}")
                                    # Stop menu music when starting game
                                    if (
                                        sound_enabled
                                        and hasattr(self, "menu_music_channel")
                                        and self.menu_music_playing
                                    ):
                                        self.menu_music_channel.stop()
                                        self.menu_music_playing = False
                                    return self.start_new_game(mode)

            # Draw background
            if has_background_image:
                # Use the loaded image as background
                self.screen.blit(background_image, (0, 0))
                
                # Add a semi-transparent overlay to make text more readable
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))  # Semi-transparent black
                self.screen.blit(overlay, (0, 0))
                
                # Draw sparkles animation
                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
                self.draw_sparkles(self.screen)
                
                # Draw sparkles animation
                self.update_sparkles(0.016)  # Use a fixed time step for consistent animation
                self.draw_sparkles(self.screen)
            else:
                # Use the gradient background
                self.screen.blit(background, (0, 0))

            # Draw title
            self.screen.blit(title_text, title_rect)

            # Draw options
            button_rects = []  # Clear previous buttons
            currently_selected = -1

            for i, (text, color, mode) in enumerate(options):
                option_text = menu_font.render(text, True, color)
                option_rect = option_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 70 * i)
                )

                button_rect = option_rect.copy()
                button_rect.inflate_ip(40, 20)
                button_rects.append((button_rect, mode))

                is_hovering = button_rect.collidepoint(mouse_pos)

                if is_hovering:
                    currently_selected = i
                    hover_color = (
                        min(color[0] + 50, 255),
                        min(color[1] + 50, 255),
                        min(color[2] + 50, 255),
                    )

                    # Pulsating effect
                    pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 2

                    # Create text with hover color and slight glow effect
                    option_text = menu_font.render(text, True, hover_color)
                    
                    # Add subtle glow effect around text
                    glow_size = int(2 + pulse)
                    for dx in range(-glow_size, glow_size+1, 2):
                        for dy in range(-glow_size, glow_size+1, 2):
                            if dx*dx + dy*dy <= glow_size*glow_size:
                                glow_text = menu_font.render(text, True, (hover_color[0], hover_color[1], hover_color[2], 50))
                                glow_rect = option_rect.copy()
                                glow_rect.x += dx
                                glow_rect.y += dy
                                self.screen.blit(glow_text, glow_rect)
                    
                    # Add sparkle effect around menu items when hovering
                    if random.random() < 0.5:  # Only 50% chance to create a sparkle each frame
                        # Calculate random position around the button
                        sparkle_x = button_rect.x + random.randint(-10, button_rect.width + 10)
                        sparkle_y = button_rect.y + random.randint(-10, button_rect.height + 10)
                        
                        # Add sparkle with color matching the button
                        self.sparkles.append({
                            "x": sparkle_x,
                            "y": sparkle_y,
                            "direction": random.uniform(0, 2 * math.pi),
                            "speed": random.uniform(0.2, 1.0),
                            "color": hover_color,
                            "size": random.uniform(1, 3),
                            "brightness": random.uniform(0.5, 1.0),
                            "twinkle_speed": random.uniform(3, 8),
                            "twinkle_offset": random.uniform(0, 2 * math.pi),
                        })
                else:
                    # Create text with original color - no button background or border
                    option_text = menu_font.render(text, True, color)

                self.screen.blit(option_text, option_rect)

            # Play sound if selection changed
            if currently_selected != -1 and currently_selected != last_selected:
                if sound_enabled and hasattr(self, "sound_menu_navigate"):
                    self.sound_menu_navigate.play()
                last_selected = currently_selected

            # Draw instructions
            instructions_text = get_font(24).render(
                "Click on a game mode to start or BACK to return to the main menu",
                True,
                SLEEK_SILVER,
            )
            instructions_rect = instructions_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8)
            )
            self.screen.blit(instructions_text, instructions_rect)
            
            # Draw "AKD" text in the bottom right corner
            akd_font = get_font(16)
            akd_text = akd_font.render("AKD", True, (255, 255, 255, 180))
            akd_rect = akd_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
            self.screen.blit(akd_text, akd_rect)

            pygame.display.flip()
            clock.tick(60)

        return False

    def run(self):
        try:
            # Set target FPS to 30 instead of default 60 for better performance
            target_fps = 30
            clock = pygame.time.Clock()
            
            running = True
            in_menu = True  # Start in menu first
            last_frame_time = time.time()

            # Don't start background music in menu - only during gameplay

            # Create initial fade-in transition for game start
            if hasattr(self, "transition"):
                self.transition.transition_type = "fade"
                self.transition.start(direction="in", duration=0.8)

            while running:
                # Calculate delta time for frame-rate independent animations
                current_time = time.time()
                dt = current_time - last_frame_time
                last_frame_time = current_time
                
                # Handle all events in a single pass
                events = pygame.event.get()
                for event in events:
                    # First priority: Handle music events
                    if event.type == pygame.USEREVENT + 1:
                        print("Music end event detected, restarting track_01.mp3")
                        # Restart the background music
                        self.play_background_music()
                        continue
                        
                    # Second priority: Handle quit events
                    if event.type == pygame.QUIT:
                        # Stop background music
                        self.stop_background_music()
                        pygame.quit()
                        sys.exit()
                        
                    # For all other events, re-post them for normal game handling
                    pygame.event.post(event)

                # Cap delta time to avoid large jumps
                dt = min(dt, 0.1)

                if in_menu:
                    print("Showing menu...")
                    menu_result = self.show_menu()
                    print(f"Menu result: {menu_result}")

                    if menu_result is True:
                        # Start the game
                        in_menu = False
                        print("Starting game with mode:", self.game_mode)

                        # Start background music for gameplay
                        self.play_background_music()

                        # Start a transition effect
                        self.transition.start(direction="in", duration=0.5)

                        # Stop menu music if it's playing
                        if (
                            sound_enabled
                            and hasattr(self, "menu_music_channel")
                            and self.menu_music_playing
                        ):
                            self.menu_music_channel.stop()
                            self.menu_music_playing = False
                    elif menu_result is False:
                        # Exit the game
                        running = False

                        # Stop menu music if it's playing
                        if (
                            sound_enabled
                            and hasattr(self, "menu_music_channel")
                            and self.menu_music_playing
                        ):
                            self.menu_music_channel.stop()
                            self.menu_music_playing = False
                    else:
                        # Likely returned from game mode menu or other submenu
                        # Continue the loop to process the result
                        continue
                else:
                    running = self.handle_events()

                    # Update transition effects
                    if self.transition.running:
                        self.transition.update(dt)

                    # Update and draw the game
                    self.update()
                    self.draw()

                    # Check if game is over and crash animation is complete
                    if self.game_over and not hasattr(self, "crash_animation_timer"):
                        # Check for high score when game is over
                        if self.highscore_manager.is_high_score(
                            self.game_mode, self.score
                        ):
                            print(f"New high score: {self.score}!")
                            # Get player name
                            player_name = self.show_name_input()
                            # Save high score
                            self.highscore_manager.add_score(
                                self.game_mode,
                                player_name,
                                self.score,
                                distance=int(self.distance_traveled),
                                coins=self.coins_collected,
                            )
                            # Show high scores
                            self.show_highscores(player_name)

                        # Start transition out
                        self.transition.start(direction="out", duration=0.5)

                        # Start menu music for the menu
                        if (
                            sound_enabled
                            and music_enabled
                            and hasattr(self, "menu_music_channel")
                            and not self.menu_music_playing
                        ):
                            try:
                                # Load menu music
                                menu_music = pygame.mixer.Sound(self.SOUND_MENU_MUSIC)
                                menu_music.set_volume(0.4)  # Set appropriate volume
                                self.menu_music_channel.play(
                                    menu_music, loops=-1
                                )  # Loop indefinitely
                                self.menu_music_playing = True
                                print("Menu music started")
                            except Exception as e:
                                print(f"Error playing menu music: {e}")

                        # Game over, return to menu
                        in_menu = True
                        print("Game over, returning to menu")
                        
                        # Stop background music when returning to menu
                        self.stop_background_music()

                # Maintain consistent frame rate - use target_fps variable
                self.clock.tick(target_fps)  # Fixed at 30 FPS for better performance
        except Exception as e:
            print(f"Error in game loop: {e}")
            traceback.print_exc()
        finally:
            # Make sure to stop all sounds before quitting
            if (
                sound_enabled
                and hasattr(self, "menu_music_channel")
                and self.menu_music_playing
            ):
                self.menu_music_channel.stop()
            if (
                sound_enabled
                and hasattr(self, "engine_channel")
                and self.engine_playing
            ):
                self.engine_channel.stop()
                
            # Stop background music if playing
            self.stop_background_music()
                
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    try:
        print("Starting game...")
        game = Game()
        # Make sure we start with the menu, not the game
        game.game_over = True  # This ensures we go to the menu first
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
    finally:
        print("Game exited")
        pygame.quit()
        sys.exit()

    def generate_stars(self):
        """Generate random stars for the night sky"""
        self.stars = []
        for _ in range(STAR_COUNT):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT // 2)  # Stars only in top half of sky
            size = random.uniform(0.5, 2)
            brightness = random.uniform(0.5, 1.0)
            twinkle_speed = random.uniform(1.0, 3.0)
            self.stars.append(
                {
                    "x": x,
                    "y": y,
                    "size": size,
                    "brightness": brightness,
                    "twinkle_speed": twinkle_speed,
                    "twinkle_offset": random.uniform(0, 2 * math.pi),
                }
            )

    def get_sky_color(self, y_position):
        """Get the sky color at the given y position based on time of day"""
        # Calculate the ratio of y position (0 at top, 1 at bottom)
        ratio = y_position / SCREEN_HEIGHT

        # Determine the phase of day/night cycle
        if self.day_phase < 0.25:  # Day
            day_progress = self.day_phase / 0.25
            top_color = DAY_COLOR
            bottom_color = DAY_COLOR_BOTTOM
        elif self.day_phase < 0.5:  # Sunset
            sunset_progress = (self.day_phase - 0.25) / 0.25
            top_color = self.interpolate_color(
                DAY_COLOR, SUNRISE_COLOR, sunset_progress
            )
            bottom_color = self.interpolate_color(
                DAY_COLOR_BOTTOM, SUNRISE_COLOR_BOTTOM, sunset_progress
            )
        elif self.day_phase < 0.75:  # Night
            night_progress = (self.day_phase - 0.5) / 0.25
            top_color = self.interpolate_color(
                SUNRISE_COLOR, NIGHT_COLOR, night_progress
            )
            bottom_color = self.interpolate_color(
                SUNRISE_COLOR_BOTTOM, NIGHT_COLOR_BOTTOM, night_progress
            )
        else:  # Sunrise
            sunrise_progress = (self.day_phase - 0.75) / 0.25
            top_color = self.interpolate_color(NIGHT_COLOR, DAY_COLOR, sunrise_progress)
            bottom_color = self.interpolate_color(
                NIGHT_COLOR_BOTTOM, DAY_COLOR_BOTTOM, sunrise_progress
            )

        # Interpolate between top and bottom colors based on y position
        return self.interpolate_color(top_color, bottom_color, ratio)

    def interpolate_color(self, color1, color2, ratio):
        """Interpolate between two colors"""
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        return (r, g, b)

    def draw_headlights(self):
        """Draw headlight effects for cars during night time"""
        # Player car headlights
        self.draw_car_headlights(self.player_car, is_player=True)

        # Other cars headlights
        for car in self.other_cars:
            self.draw_car_headlights(car)

    def draw_car_headlights(self, car, is_player=False):
        """Draw headlight effect for a specific car"""
        # Skip if car is off screen
        if hasattr(car, "y") and car.y < 0:
            return

        # Calculate actual x position with swerve offset for player car
        actual_x = car.x + (
            car.swerve_offset if is_player and hasattr(car, "swerve_offset") else 0
        )

        # Headlight positions
        left_headlight_x = actual_x - car.width // 3
        right_headlight_x = actual_x + car.width // 3
        headlight_y = car.y - car.height // 2 + 10

        # Create headlight surfaces
        headlight_length = 200 if is_player else 150
        headlight_width = 40 if is_player else 30

        for headlight_x in [left_headlight_x, right_headlight_x]:
            # Create a cone-shaped light beam
            for i in range(5):  # Multiple layers for better effect
                alpha = 30 - i * 5  # Decreasing alpha for each layer
                beam_surface = pygame.Surface(
                    (headlight_width + i * 20, headlight_length), pygame.SRCALPHA
                )

                # Create gradient from bright to transparent
                for y in range(headlight_length):
                    # Calculate alpha based on distance from source
                    y_alpha = max(0, alpha * (1 - y / headlight_length))
                    color = (255, 255, 200, int(y_alpha))
                    pygame.draw.line(
                        beam_surface,
                        color,
                        ((headlight_width + i * 20) // 2, 0),
                        ((headlight_width + i * 20) // 2, y),
                        headlight_width - i * 5,
                    )

                # Rotate and position the beam
                if is_player:
                    # Player car headlights point up
                    rotated_beam = pygame.transform.rotate(beam_surface, 180)
                    self.screen.blit(
                        rotated_beam,
                        (headlight_x - rotated_beam.get_width() // 2, headlight_y),
                    )
                else:
                    # Other cars' headlights point down
                    self.screen.blit(
                        beam_surface,
                        (headlight_x - beam_surface.get_width() // 2, headlight_y),
                    )

    def draw_car_headlights(self, car, is_player=False):
        """Draw headlight effect for a specific car"""
        # Skip if car is off screen
        if hasattr(car, "y") and car.y < 0:
            return

        # Calculate actual x position with swerve offset for player car
        actual_x = car.x + (
            car.swerve_offset if is_player and hasattr(car, "swerve_offset") else 0
        )

        # Headlight positions
        left_headlight_x = actual_x - car.width // 3
        right_headlight_x = actual_x + car.width // 3
        headlight_y = car.y - car.height // 2 + 10

        # Create headlight surfaces
        headlight_length = 200 if is_player else 150
        headlight_width = 40 if is_player else 30

        for headlight_x in [left_headlight_x, right_headlight_x]:
            # Create a cone-shaped light beam
            for i in range(5):  # Multiple layers for better effect
                alpha = 30 - i * 5  # Decreasing alpha for each layer
                beam_surface = pygame.Surface(
                    (headlight_width + i * 20, headlight_length), pygame.SRCALPHA
                )

                # Create gradient from bright to transparent
                for y in range(headlight_length):
                    # Calculate alpha based on distance from source
                    y_alpha = max(0, alpha * (1 - y / headlight_length))
                    color = (255, 255, 200, int(y_alpha))
                    pygame.draw.line(
                        beam_surface,
                        color,
                        ((headlight_width + i * 20) // 2, 0),
                        ((headlight_width + i * 20) // 2, y),
                        headlight_width - i * 5,
                    )

                # Rotate and position the beam
                if is_player:
                    # Player car headlights point up
                    rotated_beam = pygame.transform.rotate(beam_surface, 180)
                    self.screen.blit(
                        rotated_beam,
                        (headlight_x - rotated_beam.get_width() // 2, headlight_y),
                    )
                else:
                    # Other cars' headlights point down
                    self.screen.blit(
                        beam_surface,
                        (headlight_x - beam_surface.get_width() // 2, headlight_y),
                    )


# Add the update method with prompt system integration
def update(self):
    try:
        if self.game_over:
            return

        # Calculate delta time
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        # Handle welcome prompt timer
        if hasattr(self, "welcome_prompt_timer"):
            self.welcome_prompt_timer -= dt
            if self.welcome_prompt_timer <= 0:
                self.prompt_system.show_prompt("welcome")
                delattr(self, "welcome_prompt_timer")

        # Update prompt system
        if hasattr(self, "prompt_system"):
            self.prompt_system.update()

        # Update day-night cycle
        self.cycle_time += dt
        self.day_phase = (
            self.cycle_time % DAY_NIGHT_CYCLE_DURATION
        ) / DAY_NIGHT_CYCLE_DURATION

        # Update player car
        self.player_car.update(dt)

        # Update particle system
        self.particle_system.update(dt)

        # Create boost trail if boosting
        if self.player_car.is_boosting:
            boost_x = self.player_car.x
            boost_y = self.player_car.y + self.player_car.height // 2

            # Create boost trail more frequently for a more continuous effect
            if random.random() < 0.3:  # Reduced for performance
                self.particle_system.create_boost_trail(boost_x, boost_y)

            # Add occasional sparks for a more dynamic effect
            if random.random() < 0.3:
                self.particle_system.create_spark(
                    boost_x + random.uniform(-10, 10),
                    boost_y + random.uniform(-5, 5),
                    count=5,
                    intensity=0.8,
                )

        # Apply slow motion if active
        speed_factor = SLOW_MO_FACTOR if self.player_car.has_slow_mo else 1.0

        # Apply boost if active
        if self.player_car.has_boost:
            speed_factor *= BOOST_MULTIPLIER

        # Increase speed over time
        self.speed += SPEED_INCREMENT * speed_factor

        # Cap speed at 15 (which will display as 150 km/h)
        if self.speed > 15:
            self.speed = 15

        # Update distance traveled
        self.distance_traveled += self.speed * dt * 10  # 10 meters per unit of speed

        # Update time remaining for time attack mode
        if self.game_mode == GAME_MODE_TIME_ATTACK:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.game_over = True
                self.game_has_been_played = True  # Mark that a game has been played
                # Play game over sound
                if sound_enabled:
                    sound_game_over.play()

        # Update mission progress
        self.update_mission_progress()

        # Update combo timer
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.combo_count = 0
                self.score_multiplier = 1

        # Generate new obstacles
        if current_time - self.last_obstacle_time > random.uniform(3.0, 6.0):  # Further increased spawn interval
            # Check if there are too many obstacles already
            if len(self.obstacles) < 2:  # Reduced max obstacles from 3 to 2
                # Choose a lane that doesn't already have an obstacle or car nearby
                available_lanes = list(range(6))
                
                # Remove lanes that have obstacles
                for obstacle in self.obstacles:
                    if obstacle.lane in available_lanes:
                        available_lanes.remove(obstacle.lane)
                        # Also remove adjacent lanes for better spacing
                        if obstacle.lane > 0 and obstacle.lane - 1 in available_lanes:
                            available_lanes.remove(obstacle.lane - 1)
                        if obstacle.lane < 5 and obstacle.lane + 1 in available_lanes:
                            available_lanes.remove(obstacle.lane + 1)
                
                # Remove lanes that have cars near the top
                for car in self.other_cars:
                    if car.y < 200:  # Only check cars near the top of the screen
                        if car.lane in available_lanes:
                            available_lanes.remove(car.lane)
                
                # If there are available lanes, create an obstacle
                if available_lanes:
                    lane = random.choice(available_lanes)
                    # Reduced chance of moving obstacles which are more CPU intensive
                    if random.random() < 0.2:  # Reduced from 0.3
                        self.obstacles.append(MovingObstacle(lane))
                    else:
                        self.obstacles.append(Obstacle(lane))
                    self.last_obstacle_time = current_time

        # Generate other cars
        if current_time - self.last_car_time > random.uniform(4.0, 8.0):  # Further increased spawn interval
            # Check if there are too many cars already
            if len(self.other_cars) < 2:  # Reduced max cars from 3 to 2
                # Choose a lane that doesn't already have a car or obstacle nearby
                available_lanes = list(range(6))
                
                # Remove lanes that have cars
                for car in self.other_cars:
                    if car.lane in available_lanes:
                        available_lanes.remove(car.lane)
                        # Also remove adjacent lanes for better spacing
                        if car.lane > 0 and car.lane - 1 in available_lanes:
                            available_lanes.remove(car.lane - 1)
                        if car.lane < 5 and car.lane + 1 in available_lanes:
                            available_lanes.remove(car.lane + 1)
                
                # Remove lanes that have obstacles near the top
                for obstacle in self.obstacles:
                    if obstacle.y < 200:  # Only check obstacles near the top of the screen
                        if obstacle.lane in available_lanes:
                            available_lanes.remove(obstacle.lane)
                
                # If there are available lanes, create a car
                if available_lanes:
                    lane = random.choice(available_lanes)
                    # Reduced chance of AI-controlled cars which are more CPU intensive
                    if random.random() < 0.3:  # Reduced from 0.5
                        self.other_cars.append(AIControlledCar(lane))
                    else:
                        self.other_cars.append(OtherCar(lane))
                    self.last_car_time = current_time

        # Generate new power-ups
        if current_time - self.last_powerup_time > random.uniform(5.0, 15.0):
            lane = random.randint(0, 5)  # Changed from 0-3 to 0-5 for 6 lanes
            powerup_type = random.choice(["boost", "shield", "magnet", "slow_mo"])
            self.powerups.append(PowerUp(lane, powerup_type))
            self.last_powerup_time = current_time

        # Generate new coins
        if current_time - self.last_coin_time > random.uniform(1.0, 3.0):  # Increased interval
            # Limit the number of coins on screen
            if len(self.coins) < 6:  # Reduced for performance  # Add a limit to coins
                lane = random.randint(0, 5)  # Changed from 0-3 to 0-5 for 6 lanes
                x = LANE_POSITIONS[lane] + random.randint(-LANE_WIDTH // 4, LANE_WIDTH // 4)
                self.coins.append(Coin(x, -20))
                self.last_coin_time = current_time

        # Update moving obstacles
        for obstacle in self.obstacles[:]:
            if isinstance(obstacle, MovingObstacle):
                obstacle.update(dt)

        # Update AI cars
        for car in self.other_cars[:]:
            if isinstance(car, AIControlledCar):
                car.update(dt, self.player_car.lane, self.obstacles + self.other_cars)

        # Move obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move(self.speed * speed_factor)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 1
                # Add to combo for avoiding obstacle
                self.combo_count += 1
                self.combo_timer = 2.0
                # Update score multiplier
                if self.combo_count >= 10:
                    self.score_multiplier = 3
                elif self.combo_count >= 5:
                    self.score_multiplier = 2

                # Show combo prompt if it's a significant combo
                if hasattr(self, "prompt_system") and self.combo_count == 5:
                    self.prompt_system.show_prompt("combo")
            elif obstacle.collides_with(self.player_car):
                if self.player_car.has_shield:
                    # Shield protects from collision
                    self.obstacles.remove(obstacle)
                    self.score += 2
                    # Add to combo
                    self.combo_count += 2
                    self.combo_timer = 2.0
                    # Create spark effect for shield collision
                    self.particle_system.create_spark(obstacle.x, obstacle.y, count=15)
                    # Play shield sound
                    if sound_enabled:
                        sound_shield.play()
                else:
                    # Create crash effect
                    self.particle_system.create_crash(
                        self.player_car.x, self.player_car.y
                    )
                    # Play crash sound
                    if sound_enabled:
                        sound_crash.play()
                    self.game_over = True
                    self.game_has_been_played = True  # Mark that a game has been played
                    # Play game over sound
                    if sound_enabled:
                        sound_game_over.play()

        # Move other cars
        for car in self.other_cars[:]:
            # Apply braking for AI cars
            speed_modifier = (
                0.5 if isinstance(car, AIControlledCar) and car.is_braking else 0.8
            )
            car.move(self.speed * speed_factor * speed_modifier)

            if car.is_off_screen():
                self.other_cars.remove(car)
                self.score += 2 * self.score_multiplier
                # Add to combo
                self.combo_count += 1
                self.combo_timer = 2.0
            elif car.collides_with(self.player_car):
                if self.player_car.has_shield:
                    # Shield protects from collision
                    self.other_cars.remove(car)
                    self.score += 3
                    # Add to combo
                    self.combo_count += 2
                    self.combo_timer = 2.0
                    # Create spark effect for shield collision
                    self.particle_system.create_spark(car.x, car.y, count=20)
                    # Play shield sound
                    if sound_enabled:
                        sound_shield.play()
                else:
                    # Create crash effect
                    self.particle_system.create_crash(
                        self.player_car.x, self.player_car.y
                    )
                    # Play crash sound
                    if sound_enabled:
                        sound_crash.play()
                    self.game_over = True
                    self.game_has_been_played = True  # Mark that a game has been played
                    # Play game over sound
                    if sound_enabled:
                        sound_game_over.play()

        # Move and check power-ups
        for powerup in self.powerups[:]:
            powerup.move(self.speed * speed_factor)
            if powerup.is_off_screen():
                self.powerups.remove(powerup)
            elif powerup.collides_with(self.player_car):
                powerup.collect()
                self.powerups.remove(powerup)

                # Apply power-up effect
                if powerup.type == "boost":
                    self.player_car.activate_boost()
                    # Create spark effect for boost activation
                    self.particle_system.create_spark(
                        self.player_car.x,
                        self.player_car.y + self.player_car.height // 2,
                        count=15,
                    )
                    # Play boost sound
                    if sound_enabled:
                        sound_boost.play()
                    # Show boost prompt
                    if hasattr(self, "prompt_system"):
                        self.prompt_system.show_prompt("powerup_boost")
                elif powerup.type == "shield":
                    self.player_car.activate_shield()
                    # Play shield sound
                    if sound_enabled:
                        sound_shield.play()
                    # Show shield prompt
                    if hasattr(self, "prompt_system"):
                        self.prompt_system.show_prompt("powerup_shield")
                elif powerup.type == "magnet":
                    self.player_car.activate_magnet()
                    # Play powerup sound
                    if sound_enabled:
                        sound_powerup.play()
                    # Show magnet prompt
                    if hasattr(self, "prompt_system"):
                        self.prompt_system.show_prompt("powerup_magnet")
                elif powerup.type == "slow_mo":
                    self.player_car.activate_slow_mo()
                    # Play powerup sound
                    if sound_enabled:
                        sound_powerup.play()
                    # Show slow-mo prompt
                    if hasattr(self, "prompt_system"):
                        self.prompt_system.show_prompt("powerup_slow_mo")

                # Add points for collecting power-up
                self.score += 5 * self.score_multiplier
                # Add to combo
                self.combo_count += 1
                self.combo_timer = 2.0
                # Track power-ups used for missions
                self.powerups_used += 1

        # Move and check coins
        for coin in self.coins[:]:
            coin.move(self.speed * speed_factor)

            # Check if coin is in magnet range
            if self.player_car.has_magnet:
                dx = self.player_car.x - coin.x
                dy = self.player_car.y - coin.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < MAGNET_RANGE:
                    # Move coin towards player
                    angle = math.atan2(dy, dx)
                    coin.x += math.cos(angle) * 5
                    coin.y += math.sin(angle) * 5

            if coin.is_off_screen():
                self.coins.remove(coin)
            elif coin.collides_with(self.player_car):
                coin.collect()
                self.coins.remove(coin)
                self.coins_collected += 1

                # Create spark effect for coin collection
                self.particle_system.create_spark(coin.x, coin.y, count=5)

                # Play coin sound
                if sound_enabled:
                    sound_coin.play()

                # Add points for collecting coin with combo multiplier
                self.score += COIN_VALUE * self.score_multiplier

                # Increase combo
                self.combo_count += 1
                self.combo_timer = 2.0  # Reset combo timer

                # Update score multiplier
                if self.combo_count >= 10:
                    self.score_multiplier = 3
                elif self.combo_count >= 5:
                    self.score_multiplier = 2
                else:
                    self.score_multiplier = 1

                # Add boost energy
                self.player_car.add_boost_energy(5)

                # Show boost energy prompt when energy is full
                if (
                    hasattr(self, "prompt_system")
                    and self.player_car.boost_energy >= self.player_car.max_boost_energy
                ):
                    self.prompt_system.show_prompt("boost_energy")

        # Check if mission is complete and show prompt
        if (
            self.game_mode == GAME_MODE_MISSIONS
            and self.mission_progress >= self.mission_target
        ):
            if hasattr(self, "prompt_system"):
                self.prompt_system.show_prompt("mission_complete")

    except Exception as e:
        print(f"Error in update method: {e}")
        traceback.print_exc()


# Attach the update method to the Game class
Game.update = update
def update_sparkles(self, dt):
    """Update sparkle positions and properties"""
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
    """Draw sparkles on the given surface"""
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
    def handle_music_end_event(self, event):
        """Handle music end event to play the next song"""
        if event.type == pygame.USEREVENT + 1:
            if hasattr(self, "_advance_playlist"):
                self._advance_playlist()
                return True
        return False
