"""
Tileset Manager for pixel-perfect sprite extraction.
Handles loading and extracting individual sprites from a single tileset PNG file.
"""

import pygame
from typing import Dict, Tuple, Optional
from config import TILESET_PATH, TILE_WIDTH, TILE_HEIGHT, SPRITE_COORDS


class TilesetManager:
    """
    Manages sprite extraction from a single tileset PNG file.
    Provides pixel-perfect sprite rendering with caching for performance.
    """
    
    def __init__(self):
        """Initialize the tileset manager and load the tileset."""
        self.tileset: Optional[pygame.Surface] = None
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.tile_width = TILE_WIDTH
        self.tile_height = TILE_HEIGHT
        
        self._load_tileset()
    
    def _load_tileset(self) -> None:
        """Load the tileset PNG file."""
        try:
            self.tileset = pygame.image.load(TILESET_PATH)
            print(f"✓ Tileset loaded successfully: {TILESET_PATH}")
            print(f"  Tileset dimensions: {self.tileset.get_width()}x{self.tileset.get_height()}")
        except pygame.error as e:
            print(f"✗ Error loading tileset: {e}")
            print(f"  Make sure '{TILESET_PATH}' exists and is a valid PNG file")
            self.tileset = None
    
    def extract_sprite(self, x: int, y: int, width: int = None, height: int = None) -> Optional[pygame.Surface]:
        """
        Extract a sprite from the tileset at the specified coordinates.
        
        Args:
            x: X coordinate in the tileset (in tiles, not pixels)
            y: Y coordinate in the tileset (in tiles, not pixels)
            width: Width of the sprite in pixels (defaults to TILE_WIDTH)
            height: Height of the sprite in pixels (defaults to TILE_HEIGHT)
            
        Returns:
            pygame.Surface containing the extracted sprite, or None if extraction fails
        """
        if self.tileset is None:
            return None
            
        if width is None:
            width = self.tile_width
        if height is None:
            height = self.tile_height
        
        # Convert tile coordinates to pixel coordinates
        pixel_x = x * self.tile_width
        pixel_y = y * self.tile_height
        
        # Check if the sprite coordinates are within the tileset bounds
        if (pixel_x + width > self.tileset.get_width() or 
            pixel_y + height > self.tileset.get_height()):
            print(f"⚠ Warning: Sprite at ({x}, {y}) extends beyond tileset bounds")
            return None
        
        # Create a new surface for the sprite
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Extract the sprite from the tileset
        sprite.blit(self.tileset, (0, 0), (pixel_x, pixel_y, width, height))
        
        return sprite
    
    def get_sprite(self, sprite_name: str) -> Optional[pygame.Surface]:
        """
        Get a sprite by name from the sprite coordinates configuration.
        Uses caching to improve performance and automatically scales sprites.
        
        Args:
            sprite_name: Name of the sprite as defined in SPRITE_COORDS
            
        Returns:
            pygame.Surface containing the scaled sprite, or None if not found
        """
        # Check cache first
        if sprite_name in self.sprite_cache:
            return self.sprite_cache[sprite_name]
        
        # Check if sprite name exists in configuration
        if sprite_name not in SPRITE_COORDS:
            print(f"⚠ Warning: Sprite '{sprite_name}' not found in SPRITE_COORDS")
            return None
        
        # Extract sprite from tileset
        x, y = SPRITE_COORDS[sprite_name]
        sprite = self.extract_sprite(x, y)
        
        if sprite is not None:
            # Scale the sprite for pixel-perfect rendering
            from config import SCALE_FACTOR
            scaled_sprite = self.scale_sprite(sprite, SCALE_FACTOR)
            
            # Cache the scaled sprite for future use
            self.sprite_cache[sprite_name] = scaled_sprite
            print(f"✓ Loaded sprite: {sprite_name} at ({x}, {y}) - scaled {SCALE_FACTOR}x")
        else:
            print(f"✗ Failed to load sprite: {sprite_name}")
        
        return scaled_sprite if sprite is not None else None
    
    def get_snake_head_sprite(self, direction: Tuple[int, int]) -> Optional[pygame.Surface]:
        """
        Get the appropriate snake head sprite based on movement direction.
        
        Args:
            direction: Tuple representing direction (x, y)
            
        Returns:
            pygame.Surface containing the snake head sprite
        """
        from config import DIRECTION_TO_SPRITE
        
        sprite_name = DIRECTION_TO_SPRITE.get(direction)
        if sprite_name:
            return self.get_sprite(sprite_name)
        else:
            print(f"⚠ Warning: Unknown direction {direction}")
            return self.get_sprite('snake_head_right')  # Default fallback
    
    def get_snake_body_sprite(self, body_type: str) -> Optional[pygame.Surface]:
        """
        Get snake body sprite based on body segment type.
        
        Args:
            body_type: Type of body segment ('horizontal', 'vertical', 'corner_tl', etc.)
            
        Returns:
            pygame.Surface containing the body sprite
        """
        sprite_name = f'snake_body_{body_type}'
        return self.get_sprite(sprite_name)
    
    def get_snake_tail_sprite(self, direction: Tuple[int, int]) -> Optional[pygame.Surface]:
        """
        Get snake tail sprite based on movement direction.
        
        Args:
            direction: Tuple representing direction (x, y)
            
        Returns:
            pygame.Surface containing the tail sprite
        """
        from config import DIRECTION_TO_SPRITE
        
        sprite_name = DIRECTION_TO_SPRITE.get(direction)
        if sprite_name:
            tail_sprite_name = sprite_name.replace('head', 'tail')
            return self.get_sprite(tail_sprite_name)
        else:
            return self.get_sprite('snake_tail_right')  # Default fallback
    
    def get_food_sprite(self) -> Optional[pygame.Surface]:
        """Get the food sprite."""
        return self.get_sprite('food')
    
    def get_background_sprite(self) -> Optional[pygame.Surface]:
        """Get the background sprite."""
        return self.get_sprite('background')
    
    def get_wall_sprite(self) -> Optional[pygame.Surface]:
        """Get the wall sprite."""
        return self.get_sprite('wall')
    
    def scale_sprite(self, sprite: pygame.Surface, scale_factor: int) -> pygame.Surface:
        """
        Scale a sprite by an integer factor for pixel-perfect scaling.
        Uses nearest neighbor scaling to maintain crisp pixel art.
        
        Args:
            sprite: The sprite to scale
            scale_factor: Integer scaling factor (2 = 2x, 3 = 3x, etc.)
            
        Returns:
            Scaled sprite surface
        """
        if scale_factor <= 0:
            return sprite
        
        original_width = sprite.get_width()
        original_height = sprite.get_height()
        
        new_width = original_width * scale_factor
        new_height = original_height * scale_factor
        
        # Use nearest neighbor scaling for pixel-perfect results
        # This maintains the crisp, pixelated look
        scaled_sprite = pygame.transform.scale(sprite, (new_width, new_height))
        
        # Set the scaled sprite to use nearest neighbor filtering
        scaled_sprite.set_colorkey(sprite.get_colorkey() if sprite.get_colorkey() else None)
        
        return scaled_sprite
    
    def is_loaded(self) -> bool:
        """Check if the tileset is successfully loaded."""
        return self.tileset is not None
    
    def get_tileset_info(self) -> Dict[str, int]:
        """Get information about the loaded tileset."""
        if self.tileset is None:
            return {}
        
        return {
            'width': self.tileset.get_width(),
            'height': self.tileset.get_height(),
            'tile_width': self.tile_width,
            'tile_height': self.tile_height,
            'tiles_x': self.tileset.get_width() // self.tile_width,
            'tiles_y': self.tileset.get_height() // self.tile_height
        }
