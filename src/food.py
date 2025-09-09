"""
Food class for the Snake game.
Handles food generation, positioning, and rendering with pixel-perfect sprites.
"""

import pygame
import random
from typing import Tuple, List, Optional
from tileset_manager import TilesetManager
from utils import get_random_position, is_valid_position
from config import NORMAL_FOOD_VALUE, COOKIE_FOOD_VALUE, COOKIE_SPAWN_CHANCE, COOKIE_LIFETIME


class Food:
    """
    Represents the food in the game.
    Handles food generation, positioning, and rendering.
    """
    
    def __init__(self, tileset_manager: TilesetManager, cell_size: int, grid_width: int, grid_height: int, grid_offset_x: int, grid_offset_y: int, playable_start_x: int, playable_start_y: int, playable_width: int, playable_height: int):
        """
        Initialize the food.
        
        Args:
            tileset_manager: TilesetManager instance for sprite rendering
            cell_size: Size of each cell in pixels
            grid_width: Width of the game grid
            grid_height: Height of the game grid
            grid_offset_x: X offset for centering the grid
            grid_offset_y: Y offset for centering the grid
            playable_start_x: X coordinate where playable area starts
            playable_start_y: Y coordinate where playable area starts
            playable_width: Width of the playable area
            playable_height: Height of the playable area
        """
        self.tileset_manager = tileset_manager
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid_offset_x = grid_offset_x
        self.grid_offset_y = grid_offset_y
        self.playable_start_x = playable_start_x
        self.playable_start_y = playable_start_y
        self.playable_width = playable_width
        self.playable_height = playable_height
        self.position: Optional[Tuple[int, int]] = None
        self.food_type: str = "normal"  # "normal" or "cookie"
        self.value: int = NORMAL_FOOD_VALUE
        self.lifetime: int = 0  # Frames remaining before expiration
        self.is_expired: bool = False
        
    def generate(self, exclude_positions: List[Tuple[int, int]] = None, current_fps: int = 10) -> Tuple[int, int]:
        """
        Generate food at a random position, excluding specified positions.
        
        Args:
            exclude_positions: List of positions to exclude (e.g., snake body)
            current_fps: Current game FPS to calculate cookie lifetime
            
        Returns:
            Position where food was placed (x, y)
        """
        if exclude_positions is None:
            exclude_positions = []
        
        # Determine food type based on spawn chance
        if random.random() < COOKIE_SPAWN_CHANCE:
            self.food_type = "cookie"
            self.value = COOKIE_FOOD_VALUE
            self.lifetime = COOKIE_LIFETIME * current_fps  # Convert seconds to frames
        else:
            self.food_type = "normal"
            self.value = NORMAL_FOOD_VALUE
            self.lifetime = 0  # Normal food doesn't expire
            self.is_expired = False
        
        # Find a valid position
        attempts = 0
        max_attempts = 1000  # Prevent infinite loop
        
        while attempts < max_attempts:
            new_position = self._get_random_position(exclude_positions)
            
            if self._is_valid_position(new_position) and new_position not in exclude_positions:
                self.position = new_position
                return new_position
            
            attempts += 1
        
        # Fallback: place at a safe position if random generation fails
        self.position = (5, 5)  # Safe fallback position
        return self.position
    
    def get_position(self) -> Optional[Tuple[int, int]]:
        """Get the current food position."""
        return self.position
    
    def get_value(self) -> int:
        """Get the points value of this food."""
        return self.value
    
    def get_food_type(self) -> str:
        """Get the type of this food."""
        return self.food_type
    
    def is_cookie(self) -> bool:
        """Check if this is a cookie food."""
        return self.food_type == "cookie"
    
    def update(self) -> None:
        """Update the food (handle expiration for cookies)."""
        if self.food_type == "cookie" and self.lifetime > 0:
            self.lifetime -= 1
            if self.lifetime <= 0:
                self.is_expired = True
                self.position = None
    
    def is_eaten(self, snake_head_position: Tuple[int, int]) -> bool:
        """
        Check if the food has been eaten by the snake.
        
        Args:
            snake_head_position: Current snake head position (x, y)
            
        Returns:
            True if food was eaten, False otherwise
        """
        if self.position is None:
            return False
        
        return snake_head_position == self.position
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the food on the given surface.
        
        Args:
            surface: Surface to render on
        """
        if self.position is None:
            return
        
        x, y = self.position
        
        if self.tileset_manager.is_loaded():
            self._render_with_sprite(surface, x, y)
        else:
            self._render_fallback(surface, x, y)
    
    def _render_with_sprite(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Render food using sprite from tileset."""
        if self.food_type == "cookie":
            sprite = self.tileset_manager.get_sprite('food_cookie')
        else:
            sprite = self.tileset_manager.get_food_sprite()
            
        if sprite:
            # Scale sprite to cell size
            scaled_sprite = pygame.transform.scale(sprite, (self.cell_size, self.cell_size))
            pixel_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size)
            surface.blit(scaled_sprite, pixel_pos)
        else:
            # Fallback to colored rectangle if sprite not found
            self._render_fallback(surface, x, y)
    
    def _render_fallback(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Render food using simple colored rectangle as fallback."""
        rect = pygame.Rect(self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size, self.cell_size, self.cell_size)
        
        if self.food_type == "cookie":
            # Brown rectangle for cookie
            pygame.draw.rect(surface, (139, 69, 19), rect)
            # Add a small inner circle for better visibility
            center = (self.grid_offset_x + x * self.cell_size + self.cell_size // 2, self.grid_offset_y + y * self.cell_size + self.cell_size // 2)
            pygame.draw.circle(surface, (160, 82, 45), center, self.cell_size // 4)
        else:
            # Red rectangle for normal food
            pygame.draw.rect(surface, (255, 0, 0), rect)
            # Add a small inner circle for better visibility
            center = (self.grid_offset_x + x * self.cell_size + self.cell_size // 2, self.grid_offset_y + y * self.cell_size + self.cell_size // 2)
            pygame.draw.circle(surface, (255, 255, 255), center, self.cell_size // 4)
    
    def _is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """
        Check if a position is within the playable area (excluding walls).
        
        Args:
            pos: Position to check (x, y)
            
        Returns:
            True if position is valid, False otherwise
        """
        x, y = pos
        # Check if position is within the playable area boundaries
        return (self.playable_start_x <= x < self.playable_start_x + self.playable_width and 
                self.playable_start_y <= y < self.playable_start_y + self.playable_height)
    
    def _get_random_position(self, exclude_positions: List[Tuple[int, int]] = None) -> Tuple[int, int]:
        """
        Get a random position within the game grid, excluding specified positions.
        
        Args:
            exclude_positions: List of positions to exclude
            
        Returns:
            Random valid position (x, y)
        """
        import random
        
        if exclude_positions is None:
            exclude_positions = []
        
        # Only generate positions within the playable area
        x = random.randint(self.playable_start_x, self.playable_start_x + self.playable_width - 1)
        y = random.randint(self.playable_start_y, self.playable_start_y + self.playable_height - 1)
        return (x, y)
    
    def reset(self) -> None:
        """Reset the food (remove it from the game)."""
        self.position = None
        self.food_type = "normal"
        self.value = NORMAL_FOOD_VALUE
        self.lifetime = 0
        self.is_expired = False
