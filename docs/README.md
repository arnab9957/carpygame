# Car Racing Game

A fast-paced, arcade-style car racing game built with Pygame. Navigate through traffic, collect power-ups, and achieve high scores across multiple game modes with stunning visual effects and dynamic gameplay.

## Features

- **Multiple Game Modes**:
  - **Endless Mode**: Race as far as you can while avoiding obstacles and collecting coins
  - **Time Attack Mode**: Start with 60 seconds, gain +5 seconds from power-ups
  - **Missions Mode**: Complete specific challenges (collect coins, survive time, use power-ups)
  - **Race Mode**: Competitive racing with AI opponents

- **Dynamic Gameplay**:
  - Day-night cycle (60-second full cycle) with smooth visual transitions
  - 8-lane highway with dynamic traffic patterns
  - AI-controlled cars with intelligent lane-changing behavior
  - Particle effects and visual feedback
  - Combo system for enhanced scoring
  - Progressive difficulty scaling (speed increases by 0.005 per frame)

- **Power-ups & Collectibles**:
  - **Boost**: 1.8x speed multiplier for 5 seconds
  - **Shield**: Protection from crashes for 7 seconds
  - **Magnet**: Attracts coins within 150 pixels for 5 seconds
  - **Slow-Mo**: Slows time to 50% speed for 5 seconds
  - **Coins**: Worth 10 points each, persistent storage across games

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
- **Left/Right Arrow Keys**: Navigate your car between 8 lanes
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
- Speed gradually increases over time (starts at 5, increases by 0.005/frame)
- No time limit - play until you crash

### Time Attack Mode
- Start with 60 seconds on the clock
- Collect power-ups to gain +5 seconds bonus time
- Race against the clock to achieve high scores
- Warning effects start when 10 seconds remain
- Game ends when time runs out

### Missions Mode
- Complete specific objectives to progress
- Mission types include:
  - **Collect Coins**: Gather a specific number of coins
  - **Distance**: Travel a certain distance
  - **Survival**: Survive for a specific time
  - **Power-up Usage**: Use a certain number of power-ups
- Each mission has randomized targets and rewards

### Race Mode
- Competitive racing against AI opponents
- Advanced AI with intelligent lane-changing behavior
- Position-based scoring system

## Game Mechanics

### Scoring System
- **Distance**: Points for distance traveled
- **Coins**: 10 points per coin collected
- **Power-ups**: Bonus points for collecting power-ups
- **Combo System**: Multiplier for consecutive actions (2-second timer)
- **Survival Bonus**: Extra points for longer survival times

### Power-up Details
- **Boost**: 1.8x speed multiplier, 5-second duration
- **Shield**: Crash protection, 7-second duration
- **Magnet**: Auto-collect coins within 150 pixels, 5-second duration
- **Slow-Mo**: 50% time slowdown, 5-second duration
- Power-ups spawn every 5-15 seconds randomly

### Traffic System
- Maximum 2 obstacles and 2 AI cars on screen simultaneously
- AI cars have intelligent lane-changing to avoid collisions
- Dynamic lane selection prevents clustering

## Directory Structure

```
carpygame/
├── car_game.py              # Main game file (439KB)
├── car_game_backup.py       # Backup version
├── menu_animations.py       # Menu animation system
├── README.md                # This documentation
├── requirements.txt         # Python dependencies (pygame>=2.5.2)
├── bgm.jpg                  # Background image (1.2MB)
├── highscores.json          # High score data storage
├── total_coins.json         # Persistent coin storage
├── settings.json            # Game settings
├── coins.json               # Additional coin data
├── fonts/                   # Font files
│   ├── PixelifySans-Regular.ttf (93KB)
│   ├── PixelifySans-Bold.ttf (95KB)
│   └── Orbitron-Bold.ttf (0KB - placeholder)
└── sounds/                  # Audio files
    ├── engine.wav           # Engine sound effects (176KB)
    ├── engine_*.wav         # Various engine states
    ├── crash.wav            # Collision sounds (44KB)
    ├── collision.wav        # Alternative crash sound
    ├── powerup.wav          # Power-up collection (26KB)
    ├── coin.wav             # Coin collection (17KB)
    ├── shield.wav           # Shield activation (26KB)
    ├── boost.wav            # Boost activation (35KB)
    ├── menu_select.wav      # Menu selection (17KB)
    ├── menu_navigate.wav    # Menu navigation (8KB)
    ├── game_over.wav        # Game over sound (88KB)
    ├── background_music.mp3 # Gameplay music (2.9MB)
    ├── menu_music.mp3       # Menu background music (4.4MB)
    └── music/               # Additional music tracks
```

## Technical Specifications

### Performance Features
- **Responsive Design**: Scales from base resolution 1280x720 to any screen size
- **Object Culling**: Only renders objects within screen bounds
- **Memory Management**: Automatic cache cleanup (backgrounds, fonts)
- **Frame Rate**: Optimized for 60 FPS gameplay
- **Sound System**: Fallback to generated sounds if files missing

### Architecture
- **Modular Design**: Separate classes for Game, Car, PowerUp, Obstacle, etc.
- **State Management**: Clean separation between menu and gameplay states
- **Event System**: Comprehensive input handling and game events
- **Settings System**: Persistent configuration storage

### Visual Effects
- **Particle System**: Custom particle effects for boosts and crashes
- **Day-Night Cycle**: Smooth color transitions over 60-second cycles
- **UI Scaling**: Responsive interface elements
- **Transition Effects**: Smooth screen transitions between modes

## Development Notes

- Built with object-oriented design principles
- Extensive use of Pygame's advanced features
- Custom particle system for visual effects
- Sophisticated AI system for traffic simulation
- Comprehensive error handling and fallback systems
- Cross-platform compatibility (Windows, macOS, Linux)

## Credits

- **Developer**: AKD
- **Engine**: Pygame (https://www.pygame.org)
- **Fonts**: Pixelify Sans, Orbitron
- **Audio**: Custom sound effects and music tracks
- **Graphics**: Custom particle effects and visual systems

## Version History

- **Current Version**: Advanced multi-mode racing game with full feature set
- **Features**: 4 game modes, 8-lane highway, power-up system, AI traffic, visual effects
- **Performance**: Optimized for smooth 60 FPS gameplay with responsive scaling
