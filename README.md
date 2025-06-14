# Car Racing Game

A fast-paced, arcade-style car racing game built with Pygame. Navigate through traffic, collect power-ups, and achieve high scores across multiple game modes.

## Features

- **Multiple Game Modes**:
  - Endless: Race as far as you can while avoiding obstacles
  - Time Attack: Complete objectives before time runs out
  - Missions: Complete specific challenges to progress

- **Dynamic Gameplay**:
  - Day-night cycle with visual effects
  - Multiple power-ups (Boost, Shield, Magnet, Slow-Mo)
  - Combo system for scoring
  - Collectible coins
  - AI-controlled traffic

- **Visual Effects**:
  - Particle systems for crashes, boosts, and effects
  - Dynamic lighting based on time of day
  - Smooth animations and transitions
  - **NEW**: Animated option toggling in settings menu

- **Customization**:
  - Multiple car options with different stats
  - Adjustable settings (sound, music, fullscreen)

- **Game Features**:
  - High score tracking with persistent storage
  - In-game tutorials and prompts
  - Responsive controls

## Requirements

- Python 3.6+
- Pygame 2.5.2+
- typing 3.7.4.3+

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/car-racing-game.git
   cd car-racing-game
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python car_game.py
   ```

## Controls

- **Arrow Keys**: Navigate your car left and right
- **Space**: Use boost (when boost meter is full)
- **ESC/P**: Pause game
- **F11**: Toggle fullscreen
- **X**: Dismiss tutorial prompts

## Directory Structure

```
car_game_/
├── car_game.py          # Main game file
├── README.md            # This file
├── requirements.txt     # Dependencies
├── highscores.json      # High score data
├── bgm.jpg              # Background image
├── fonts/               # Font files
│   └── PixelifySans-*.ttf
└── sounds/              # Sound files
    ├── engine.wav
    ├── crash.wav
    ├── powerup.wav
    └── ...
```

## Credits

- Developed by AKD
- Built with Pygame (https://www.pygame.org)
- Font: Pixelify Sans

## License

This project is licensed under the MIT License - see the LICENSE file for details.
