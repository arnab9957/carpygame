# Car Racing Game 🏎️

A feature-rich 2D car racing game built with Python and Pygame, featuring multiple game modes, customizable cars, and dynamic environments.

## 🎮 Features

### Game Modes
- **Endless Mode**: Drive as far as possible while avoiding obstacles
- **Time Attack**: Race against the clock to achieve high scores
- **Mission Mode**: Complete specific objectives for rewards
- **Race Mode**: Competitive racing with enhanced AI opponents

### Gameplay Features
- **8-lane highway** with dynamic traffic
- **Boost system** - Build energy by driving distance and collecting coins
- **Power-ups**: Shield, Magnet, Slow-Mo effects
- **AI-controlled traffic** with 3 behavior types (normal, aggressive, cautious)
- **Smart lane-changing AI** that reacts to player and obstacles
- **Animated backgrounds** with buildings, trees, and sea
- **Combo system** for bonus points
- **Collision detection** with realistic physics
- **Road surface details** (cracks, patches) for visual realism

### Customization
- **Car Garage**: Choose from multiple car colors and styles
- **Persistent car selection** - Your choice is saved between sessions
- **Settings menu** with sound/music controls

### Visual Effects
- **Particle systems** for explosions and effects
- **Smooth transitions** between screens
- **Animated UI elements** with glow effects
- **Dynamic backgrounds** with buildings, trees, and sea
- **Headlight effects** for night driving
- **Enhanced glowing moon** with pulsing effects and orbital stars
- **Screen flash effects** for power-up activation/deactivation
- **Transition effects** (fade, slide, iris, mosaic) between screens
- **In-game prompt system** for tutorials and notifications
- **Taillights with brake animation** on all vehicles
- **Enhanced city background** with multi-level road networks and street lighting

## 🎯 Controls

- **Arrow Keys**: Move left/right between lanes
- **Space Bar**: Use boost (when energy is available)
- **ESC**: Pause game / Return to menu
- **Enter**: Select menu options

## 📁 Project Structure

```
carpygame/
├── car_game.py              # Main game executable
├── requirements.txt         # Python dependencies  
├── README.md               # This file
├── .gitignore             # Git ignore rules
├── assets/                 # Game assets
│   ├── fonts/             # Font files (TTF/OTF)
│   ├── images/            # Background images and sprites
│   ├── music/             # Background music tracks (MP3)
│   └── sounds/            # Sound effects (WAV/MP3)
├── data/                  # Persistent game data
│   ├── highscores.json    # High score records
│   ├── settings.json      # Game settings
│   ├── total_coins.json   # Total coins collected
│   └── selected_car.json  # Currently selected car
├── docs/                  # Documentation and development notes
│   ├── PROJECT_STRUCTURE.md
│   ├── BOOST_SYSTEM_ADDED.md
│   ├── MAGNET_SYSTEM_ADDED.md
│   ├── ENHANCED_CITY_BACKGROUND.md
│   ├── MOON_ENHANCEMENT_SUMMARY.md
│   └── other feature documentation
└── scripts/               # Utility scripts and tools
    ├── create_background.py  # Background image generation
    ├── test_moon.py         # Moon animation testing
    └── car_game_backup.py   # Backup version of main game
```

## 🚀 Installation & Setup

1. **Install Python 3.7+**
2. **Install dependencies**:
   ```bash
   pip install pygame
   ```
3. **Run the game**:
   ```bash
   python car_game.py
   ```

**Note**: The game will automatically create `fonts/` and `sounds/` directories if needed during runtime.

## 🎵 Audio Setup

The game supports background music and sound effects:
- Place music files (MP3) in `assets/music/`
- Place sound effects in `assets/sounds/`
- Audio will be automatically detected and loaded

## 🏆 Scoring System

- **Distance**: Points for meters traveled
- **Coins**: Bonus points for collection
- **Combos**: Multiplier for consecutive coin collection
- **Missions**: Extra rewards for completing objectives
- **Boost usage**: Strategic boost timing for higher scores

## 🔧 Technical Features

- **Fullscreen support** with window management
- **Persistent data storage** (scores, settings, progress)
- **Modular code structure** with separate classes
- **Error handling** for missing assets
- **Performance optimization** with efficient rendering
- **Cross-platform compatibility**
- **AI-controlled traffic** with intelligent lane-changing behavior
- **Advanced transition system** with multiple effect types (fade, slide, iris, mosaic)
- **In-game tutorial system** with contextual prompts
- **Dynamic road surface generation** with realistic details
- **Screen flash effects** for enhanced visual feedback
- **Multi-layered particle systems** for realistic effects

## 🤖 AI & Advanced Systems

### AI Traffic System
- **3 AI Behavior Types**: Normal, Aggressive, and Cautious drivers
- **Smart Lane Changing**: AI cars react to obstacles and player position
- **Dynamic Braking**: AI cars brake when encountering obstacles
- **Collision Avoidance**: Intelligent pathfinding around obstacles
- **Realistic Traffic Patterns**: Varied speeds and behaviors

### Transition & Effects System
- **4 Transition Types**: Fade, Slide, Iris, and Mosaic effects
- **Screen Flash Effects**: Visual feedback for power-up activation/deactivation
- **Particle Systems**: Boost trails, explosions, and environmental effects
- **Dynamic Lighting**: Enhanced lighting effects and visual atmosphere

### Tutorial & Prompt System
- **Contextual Tutorials**: In-game prompts that guide new players
- **Progressive Disclosure**: Tips appear based on game progress
- **Non-intrusive Design**: Prompts fade automatically and don't block gameplay

### Enhanced Visual Details
- **Road Surface Realism**: Dynamic cracks, patches, and wear patterns
- **Vehicle Lighting**: Taillights with brake animation on all vehicles
- **Enhanced Moon**: Pulsing glow effects with orbital stars
- **Multi-level City Background**: Layered road networks and street lighting

## 🎨 Customization

### Adding New Cars
Edit the car colors array in the garage system to add new vehicle options.

### Creating Custom Backgrounds
Use `scripts/create_background.py` to generate new background images with different themes.

### Adding Music
Drop MP3 files into `assets/music/` - they'll be automatically included in the playlist.

## 🐛 Troubleshooting

- **No sound**: Check if audio files exist in `assets/sounds/`
- **Missing fonts**: Ensure font files are in `assets/fonts/`
- **Performance issues**: Try running in windowed mode
- **Save data issues**: Check `data/` directory permissions

## 📈 Recent Updates & Improvements

### Latest Features Added
- **Enhanced AI Traffic System**: Smart AI cars with 3 behavior types and intelligent lane-changing
- **Advanced Transition Effects**: 4 different transition types (fade, slide, iris, mosaic) between screens
- **Screen Flash Effects**: Visual feedback system for power-up activation/deactivation
- **In-Game Tutorial System**: Contextual prompts and tutorials for new players
- **Enhanced Moon Animation**: Pulsing glow effects with orbital twinkling stars
- **Multi-Level City Background**: Layered road networks with realistic street lighting
- **Road Surface Details**: Dynamic generation of cracks, patches, and wear patterns
- **Vehicle Brake Lights**: Realistic taillights with brake animation on all vehicles
- **Improved Sound System**: Enhanced audio handling with better error management
- **Race Mode**: New competitive game mode with enhanced AI opponents

### Performance Optimizations
- **Efficient Particle Systems**: Optimized rendering for boost trails and effects
- **Smart Asset Loading**: Better error handling for missing fonts and sounds
- **Frame Rate Management**: Consistent 30 FPS for better performance
- **Memory Management**: Improved cleanup and resource management

### Visual Enhancements
- **Enhanced Lighting**: Improved lighting effects and visual atmosphere
- **Better UI Animations**: Smooth transitions and glow effects throughout the interface
- **Atmospheric Effects**: Enhanced weather and environmental details
- **Improved Color Schemes**: Better contrast and visual hierarchy

## 📈 Future Updates

See `docs/` folder for planned features and development roadmap.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the game!

---

**Enjoy the race! 🏁**
