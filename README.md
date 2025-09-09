# Snake Game - Pixel Art Edition

A classic Snake game built with Python and Pygame, featuring pixel-perfect sprite extraction from a single tileset PNG file, complete with music, sound effects, and a beautiful retro aesthetic.

## 🎮 Features

### Core Gameplay

- **Classic Snake mechanics** with smooth movement and collision detection
- **Progressive difficulty** - game speed increases as you score more points
- **Score system** with high score tracking
- **Multiple food types**:
  - Normal food (10 points) - grows snake by 1 segment
  - Cookie (20 points) - grows snake by 2 segments, expires after 4 seconds
- **Dynamic food spawning** with 15% chance for special cookies

### Visual & Audio

- **Pixel-perfect sprite rendering** with 4x scaling for crisp graphics
- **Custom pixel art tileset** with animated snake sprites
- **Background music** for different game states (title, gameplay, game over)
- **Sound effects** for food consumption and pause/resume
- **Custom pixel fonts** (PixelifySans) for authentic retro feel
- **Fullscreen gameplay** with responsive grid scaling

### Technical Features

- **Modular architecture** with clean separation of concerns
- **Tileset-based asset management** - all sprites from single PNG file
- **Configurable game settings** easily adjustable in `config.py`
- **Fallback rendering** if tileset fails to load
- **Cross-platform compatibility** (Windows, macOS, Linux)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the setup script** (optional but recommended):
   ```bash
   python setup.py
   ```
4. **Test your tileset** (optional):
   ```bash
   python test_tileset.py
   ```

### Manual Setup

1. Install Python 3.8+
2. Install pygame:
   ```bash
   pip install pygame
   ```
3. Place your tileset PNG file in `assets/tileset.png`
4. Update sprite coordinates in `src/config.py` if needed

## 🎯 Usage

### Starting the Game

```bash
python src/main.py
```

### Game States

- **Main Menu**: Press SPACE to start, ESC to quit
- **Playing**: Use arrow keys to move, SPACE to pause, ESC for menu
- **Paused**: Press SPACE to resume, ESC for menu
- **Game Over**: Press R to restart, ESC for menu

## 🎮 Controls

| Key            | Action                             |
| -------------- | ---------------------------------- |
| **Arrow Keys** | Move snake (Up, Down, Left, Right) |
| **WASD**       | Alternative movement controls      |
| **SPACE**      | Pause/Resume game                  |
| **ESC**        | Quit to menu/Exit game             |
| **R**          | Restart game (when game over)      |

## ⚙️ Configuration

### Game Settings (`src/config.py`)

- **Speed progression**: Adjust `INITIAL_FPS`, `MAX_FPS`, `SPEED_INCREASE_INTERVAL`
- **Food settings**: Modify `COOKIE_SPAWN_CHANCE`, `COOKIE_LIFETIME`, food values
- **Grid size**: Change `GRID_WIDTH`, `GRID_HEIGHT` for different play areas
- **Visual settings**: Adjust `CELL_SIZE`, `SCALE_FACTOR` for different resolutions

### Tileset Configuration

Update `SPRITE_COORDS` in `config.py` to match your tileset layout:

```python
SPRITE_COORDS = {
    'snake_head_up': (1, 3),
    'snake_head_left': (2, 3),
    # ... more sprite coordinates
}
```

## 📁 Project Structure

```
snake/
├── assets/
│   ├── tileset.png              # Main pixel art tileset
│   ├── fonts/                   # Custom pixel fonts
│   │   ├── PixelifySans-Bold.ttf
│   │   ├── PixelifySans-Medium.ttf
│   │   ├── PixelifySans-Regular.ttf
│   │   └── PixelifySans-SemiBold.ttf
│   ├── music/                   # Background music
│   │   ├── title.wav
│   │   ├── main.wav
│   │   └── game_over.wav
│   └── sound_effects/           # Game sound effects
│       ├── food.wav
│       └── pause.wav
├── src/
│   ├── main.py                  # Game entry point
│   ├── game.py                  # Main game loop and state management
│   ├── snake.py                 # Snake class and movement logic
│   ├── food.py                  # Food generation and management
│   ├── tileset_manager.py       # Pixel-perfect sprite extraction
│   ├── config.py                # Game configuration and constants
│   └── utils.py                 # Utility functions
├── test_tileset.py              # Tileset testing utility
├── setup.py                     # Development environment setup
├── requirements.txt             # Python dependencies
├── links.txt                    # Asset source links
└── README.md                    # This file
```

## 🎨 Asset Credits

This project uses the following assets:

- **Sound Effects**: [RetroSounds by dagurasusk](https://dagurasusk.itch.io/retrosounds)
- **Music**: [Creator Pack by jonathan-so](https://jonathan-so.itch.io/creatorpack)
- **Pixel Art**: [Snake Game Assets by cosme](https://cosme.itch.io/snake)

## 🛠️ Development

### Testing

- **Test tileset extraction**: `python test_tileset.py`
- **View tileset**: Run the test script and choose to view the tileset
- **Setup development environment**: `python setup.py`

### Customization

- **Add new sprites**: Update `SPRITE_COORDS` in `config.py`
- **Modify gameplay**: Adjust constants in `config.py`
- **Add new food types**: Extend the `Food` class in `food.py`
- **Change music**: Replace files in `assets/music/` directory

## 🐛 Troubleshooting

### Common Issues

1. **"Tileset not found"**: Ensure `assets/tileset.png` exists
2. **"pygame not found"**: Run `pip install pygame`
3. **"Font not found"**: Check that font files are in `assets/fonts/`
4. **Sprites not displaying**: Verify sprite coordinates in `config.py`

### Getting Help

- Check that all dependencies are installed: `pip install -r requirements.txt`
- Run the test script to verify tileset: `python test_tileset.py`
- Ensure your tileset PNG matches the expected layout in `config.py`

## 📄 License

This project is open source. Please respect the licenses of the included assets (see Asset Credits section).

---

**Enjoy playing Snake Game - Pixel Art Edition!** 🐍✨
