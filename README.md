# Car Racing Game 🏎️

A feature-rich 2D car racing game built with Python and Pygame, featuring multiple game modes, customizable cars, and dynamic environments.

## 🎮 Features

### Game Modes
- **Endless Mode**: Drive as far as possible while avoiding obstacles
- **Time Attack**: Race against the clock to achieve high scores
- **Mission Mode**: Complete specific objectives for rewards

### Gameplay Features
- **8-lane highway** with dynamic traffic
- **Boost system** - Build energy by driving distance and collecting coins
- **Power-ups**: Shield, Magnet, Slow-Mo effects
- **Day/Night cycle** with dynamic lighting
- **Weather effects** and animated backgrounds
- **Combo system** for bonus points
- **Collision detection** with realistic physics

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

## 🎯 Controls

- **Arrow Keys**: Move left/right between lanes
- **Space Bar**: Use boost (when energy is available)
- **ESC**: Pause game / Return to menu
- **Enter**: Select menu options
- **T**: Toggle time of day (debug)

## 📁 Project Structure

```
carpygame/
├── car_game.py              # Main game file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── assets/                 # Game assets
│   ├── fonts/             # Font files
│   ├── images/            # Background images
│   ├── music/             # Background music tracks
│   └── sounds/            # Sound effects
├── data/                  # Game data files
│   ├── highscores.json    # High score records
│   ├── settings.json      # Game settings
│   ├── total_coins.json   # Persistent coin count
│   └── selected_car.json  # Saved car selection
├── docs/                  # Documentation
│   ├── PROJECT_STRUCTURE.md
│   ├── BOOST_SYSTEM_ADDED.md
│   ├── MAGNET_SYSTEM_ADDED.md
│   └── other feature docs
└── scripts/               # Utility scripts
    ├── create_background.py  # Background generation
    ├── test_moon.py         # Moon animation test
    └── car_game_backup.py   # Backup version
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

## 📈 Future Updates

See `docs/` folder for planned features and development roadmap.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the game!

---

**Enjoy the race! 🏁**
