# Car Racing Game

A fast-paced, arcade-style car racing game built with Pygame. Navigate through traffic, collect power-ups, and achieve high scores across multiple game modes with stunning visual effects and dynamic gameplay.

## Features

- **Multiple Game Modes**:
  - **Endless Mode**: Race as far as you can while avoiding obstacles and collecting coins
  - **Time Attack Mode**: Race against time with bonus time from power-ups
  - **Missions Mode**: Complete specific challenges (collect coins, survive time, use power-ups)
  - **Race Mode**: Competitive racing with AI opponents

- **Dynamic Gameplay**:
  - Day-night cycle with smooth visual transitions
  - Weather effects and atmospheric lighting
  - 8-lane highway with dynamic traffic patterns
  - AI-controlled cars with intelligent movement
  - Particle effects and visual feedback
  - Combo system for enhanced scoring
  - Progressive difficulty scaling

- **Power-ups & Collectibles**:
  - **Boost**: Increases speed temporarily
  - **Shield**: Protection from crashes
  - **Magnet**: Attracts nearby coins automatically
  - **Slow-Mo**: Slows down time for easier navigation
  - **Coins**: Collectible currency system with persistent storage

- **Advanced Features**:
  - Fullscreen support with responsive UI scaling
  - High score system with separate leaderboards per game mode
  - Settings menu with customizable options
  - Pause menu with resume/restart/quit options
  - Smooth transition effects between screens
  - In-game tutorial prompts and hints
  - Background music and sound effects
  - Crash animations and visual feedback

## Requirements

- Python 3.6+
- Pygame 2.5.2+

## Installation

1. Clone or download the game files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python car_game.py
   ```

## Controls

### Gameplay Controls
- **Left/Right Arrow Keys**: Navigate your car between lanes
- **Space**: Use boost (when boost energy is available)
- **ESC** or **P**: Pause game
- **F11**: Toggle fullscreen mode
- **T**: Debug - Toggle time of day (development feature)

### Menu Navigation
- **Arrow Keys**: Navigate menu options
- **Enter**: Select menu option
- **ESC**: Go back/Exit menus
- **X**: Dismiss tutorial prompts

## Game Modes Explained

### Endless Mode
- Survive as long as possible while avoiding traffic
- Collect coins and power-ups to increase your score
- Speed gradually increases over time
- No time limit - play until you crash

### Time Attack Mode
- Start with limited time (60 seconds)
- Collect power-ups to gain bonus time (+5 seconds)
- Race against the clock to achieve high scores
- Game ends when time runs out

### Missions Mode
- Complete specific objectives to progress
- Mission types include:
  - **Distance**: Travel a certain distance
  - **Survival**: Survive for a specific time
  - **Power-up Collection**: Use a certain number of power-ups
- Each mission has different targets and rewards

### Race Mode
- Competitive racing against AI opponents
- Advanced AI with lane-changing behavior
- Position-based scoring system

## Scoring System

- **Distance**: Points for distance traveled
- **Coins**: Bonus points for coin collection
- **Power-ups**: Points for collecting power-ups
- **Combo System**: Multiplier for consecutive actions
- **Survival Bonus**: Extra points for longer survival times

## Directory Structure

```
carpygame/
├── car_game.py              # Main game file (439KB)
├── README.md                # This documentation
├── requirements.txt         # Python dependencies
├── bgm.jpg                  # Background image (1.2MB)
├── highscores.json          # High score data storage
├── total_coins.json         # Persistent coin storage
├── settings.json            # Game settings
├── fonts/                   # Font files
│   ├── PixelifySans-Regular.ttf
│   ├── PixelifySans-Bold.ttf
│   └── Orbitron-Bold.ttf
└── sounds/                  # Audio files
    ├── engine.wav           # Engine sound effects
    ├── crash.wav            # Collision sounds
    ├── powerup.wav          # Power-up collection
    ├── coin.wav             # Coin collection
    ├── shield.wav           # Shield activation
    ├── boost.wav            # Boost activation
    ├── menu_select.wav      # Menu navigation
    ├── menu_navigate.wav    # Menu selection
    ├── game_over.wav        # Game over sound
    ├── background_music.mp3 # Gameplay music
    ├── menu_music.mp3       # Menu background music
    └── music/               # Additional music tracks
```

## Technical Features

- **Responsive Design**: Automatically scales to different screen resolutions
- **Performance Optimized**: Efficient rendering with object culling
- **Memory Management**: Automatic cache cleanup and resource management
- **Error Handling**: Graceful fallbacks for missing assets
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Modular Architecture**: Clean separation of game systems

## Development Notes

- Built with object-oriented design principles
- Extensive use of Pygame's advanced features
- Custom particle system for visual effects
- Sophisticated AI system for traffic simulation
- Comprehensive settings and configuration system

## Credits

- **Developer**: AKD
- **Engine**: Pygame (https://www.pygame.org)
- **Fonts**: Pixelify Sans, Orbitron
- **Audio**: Custom sound effects and music tracks
- **Graphics**: Custom particle effects and visual systems

## Version History

- **Current Version**: Advanced multi-mode racing game with full feature set
- **Features Added**: 4 game modes, power-up system, AI traffic, visual effects, persistent storage
- **Performance**: Optimized for smooth 60 FPS gameplay
