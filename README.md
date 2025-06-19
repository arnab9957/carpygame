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

## Requirements

- Python 3.6+
- Pygame 2.5.2+

## Installation

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the game:
   ```
   python car_game.py
   ```

## Controls

- **Arrow Keys**: Navigate your car left and right
- **Space**: Use boost (when boost meter is full)
- **ESC/P**: Pause game
- **F11**: Toggle fullscreen

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
