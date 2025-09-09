"""
Game configuration and constants.
All game settings can be modified here for easy customization.
"""

# Window settings (16:9 aspect ratio)
WINDOW_WIDTH = 1024  # 16:9 ratio
WINDOW_HEIGHT = 576  # 16:9 ratio
WINDOW_TITLE = "Snake Game - Pixel Art Edition"

# Grid settings (30x15 wall tiles)
GRID_WIDTH = 30  # 30 tiles wide
GRID_HEIGHT = 15  # 15 tiles tall
CELL_SIZE = 32  # Size of each grid cell in pixels (8x8 tiles scaled 4x)
SCALE_FACTOR = 4  # Scale factor for pixel-perfect upscaling

# Game settings
FPS = 10  # Frames per second (game speed)
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_POSITION = (20, 11)  # Starting position (x, y) - centered in 30x15 grid (with balanced vertical spacing)

# Speed progression settings
INITIAL_FPS = 4  # Starting speed (much slower)
MAX_FPS = 15  # Maximum speed the snake can reach
SPEED_INCREASE_INTERVAL = 30  # Increase speed every 10 food items eaten
SPEED_INCREASE_AMOUNT = 1  # How much to increase FPS each time

# Food settings
NORMAL_FOOD_VALUE = 10
COOKIE_FOOD_VALUE = 20  # 2x normal food value
COOKIE_SPAWN_CHANCE = 0.15  # 15% chance to spawn cookie instead of normal food
COOKIE_LIFETIME = 4  # Cookie disappears after 4 seconds (will be multiplied by FPS in game)

# Colors (RGB values)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Tileset configuration
# You'll need to update these coordinates based on your tileset layout
TILESET_PATH = "assets/tileset.png"
TILE_WIDTH = 8  # Width of each tile in the tileset
TILE_HEIGHT = 8  # Height of each tile in the tileset

# Sprite coordinates in the tileset (x, y positions)
# Based on your actual tileset layout
SPRITE_COORDS = {
    # Snake sprites (4th row, left to right)
    'snake_head_up': (1, 3),      # 4th row, 2nd tile
    'snake_head_left': (2, 3),    # 4th row, 3rd tile
    'snake_head_down': (3, 3),    # 4th row, 4th tile
    'snake_head_right': (4, 3),   # 4th row, 5th tile
    'snake_body_horizontal': (5, 3),  # 4th row, 6th tile (snake body)
    'snake_body_vertical': (5, 3),    # Same as horizontal for now
    'snake_body_corner_tl': (5, 3),   # Using body sprite for corners
    'snake_body_corner_tr': (5, 3),
    'snake_body_corner_bl': (5, 3),
    'snake_body_corner_br': (5, 3),
    'snake_tail_up': (5, 3),      # Using head sprites for tail
    'snake_tail_down': (5, 3),
    'snake_tail_left': (5, 3),
    'snake_tail_right': (5, 3),
    
    # Food sprites (4th row)
    'food': (6, 3),               # 4th row, 7th tile (cherry)
    'food_cookie': (7, 3),        # 4th row, 8th tile (cookie)
    
    # Background sprites
    'background': (0, 3),         # 4th row, 1st tile (empty)
    
    # Wall sprites
    'wall_top_corner': (12, 0),    # Top corners (left and right)
    'wall_bottom_corner': (13, 0), # Bottom corners (left and right)
    'wall_left': (8, 2),           # Left side border
    'wall_right': (9, 2),          # Right side border
    'wall_top': (7, 2),            # Top side border
    'wall_bottom': (10, 2),        # Bottom side border
    'wall_inside': (0, 1),         # Inside wall area
    'wall': (0, 1),                # Default wall (inside)
}

# Movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Direction mapping for sprite selection
DIRECTION_TO_SPRITE = {
    UP: 'snake_head_up',
    DOWN: 'snake_head_down',
    LEFT: 'snake_head_left',
    RIGHT: 'snake_head_right'
}
