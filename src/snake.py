"""
Snake class for the Snake game.
Handles snake movement, growth, and rendering with pixel-perfect sprites.
"""

import pygame
from typing import List, Tuple, Optional
from config import INITIAL_SNAKE_LENGTH, INITIAL_SNAKE_POSITION, UP, DOWN, LEFT, RIGHT
from tileset_manager import TilesetManager
from utils import is_valid_position


class Snake:
    """
    Represents the snake in the game.
    Handles movement, growth, collision detection, and rendering.
    """
    
    def __init__(self, tileset_manager: TilesetManager, cell_size: int, grid_width: int, grid_height: int, grid_offset_x: int, grid_offset_y: int, playable_start_x: int, playable_start_y: int, playable_width: int, playable_height: int):
        """
        Initialize the snake.
        
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
        self.body: List[Tuple[int, int]] = []
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Tuple[int, int] = RIGHT
        self.grow_pending: bool = False
        
        self._initialize_body()
    
    def _initialize_body(self) -> None:
        """Initialize the snake body with the starting position and length."""
        start_x, start_y = INITIAL_SNAKE_POSITION
        
        # Create initial body segments
        for i in range(INITIAL_SNAKE_LENGTH):
            segment_x = start_x - i  # Snake grows to the right initially
            segment_y = start_y
            self.body.append((segment_x, segment_y))
    
    def update_direction(self, new_direction: Tuple[int, int]) -> None:
        """
        Update the snake's direction for the next move.
        Prevents the snake from moving backwards into itself.
        
        Args:
            new_direction: New direction to move (x, y)
        """
        # Don't allow moving backwards into the body
        if len(self.body) > 1:
            opposite_direction = (-self.direction[0], -self.direction[1])
            if new_direction == opposite_direction:
                return
        
        self.next_direction = new_direction
    
    def move(self) -> bool:
        """
        Move the snake one step in the current direction.
        
        Returns:
            True if move was successful, False if collision occurred
        """
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check for wall collision using dynamic grid dimensions
        if not self._is_valid_position(new_head):
            return False
        
        # Check for self collision
        if new_head in self.body:
            return False
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False
        
        return True
    
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
    
    def grow(self) -> None:
        """Mark the snake to grow on the next move."""
        self.grow_pending = True
    
    def get_head_position(self) -> Tuple[int, int]:
        """Get the current head position."""
        return self.body[0]
    
    def get_body_positions(self) -> List[Tuple[int, int]]:
        """Get all body positions."""
        return self.body.copy()
    
    def get_length(self) -> int:
        """Get the current snake length."""
        return len(self.body)
    
    def reset(self) -> None:
        """Reset the snake to initial state."""
        self.body.clear()
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_pending = False
        self._initialize_body()
    
    def render(self, surface: pygame.Surface) -> None:
        """
        Render the snake on the given surface.
        
        Args:
            surface: Surface to render on
        """
        if not self.tileset_manager.is_loaded():
            self._render_fallback(surface)
            return
        
        for i, (x, y) in enumerate(self.body):
            if i == 0:  # Head
                self._render_head(surface, x, y)
            elif i == len(self.body) - 1:  # Tail
                self._render_tail(surface, x, y, i)
            else:  # Body segment
                self._render_body_segment(surface, x, y, i)
    
    def _render_head(self, surface: pygame.Surface, x: int, y: int) -> None:
        """Render the snake head."""
        sprite = self.tileset_manager.get_snake_head_sprite(self.direction)
        if sprite:
            # Scale sprite to cell size
            scaled_sprite = pygame.transform.scale(sprite, (self.cell_size, self.cell_size))
            pixel_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size)
            surface.blit(scaled_sprite, pixel_pos)
        else:
            # Fallback rendering
            rect = pygame.Rect(self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(surface, (0, 255, 0), rect)
    
    def _render_tail(self, surface: pygame.Surface, x: int, y: int, segment_index: int) -> None:
        """Render the snake tail."""
        # Calculate tail direction based on previous segment
        if segment_index > 0:
            prev_x, prev_y = self.body[segment_index - 1]
            tail_direction = (x - prev_x, y - prev_y)
        else:
            tail_direction = self.direction
        
        sprite = self.tileset_manager.get_snake_tail_sprite(tail_direction)
        if sprite:
            # Scale sprite to cell size
            scaled_sprite = pygame.transform.scale(sprite, (self.cell_size, self.cell_size))
            pixel_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size)
            surface.blit(scaled_sprite, pixel_pos)
        else:
            # Fallback rendering
            rect = pygame.Rect(self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(surface, (0, 200, 0), rect)
    
    def _render_body_segment(self, surface: pygame.Surface, x: int, y: int, segment_index: int) -> None:
        """Render a body segment."""
        # Determine body segment type based on adjacent segments
        body_type = self._get_body_segment_type(segment_index)
        
        sprite = self.tileset_manager.get_snake_body_sprite(body_type)
        if sprite:
            # Scale sprite to cell size
            scaled_sprite = pygame.transform.scale(sprite, (self.cell_size, self.cell_size))
            pixel_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size)
            surface.blit(scaled_sprite, pixel_pos)
        else:
            # Fallback rendering
            rect = pygame.Rect(self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(surface, (0, 150, 0), rect)
    
    def _get_body_segment_type(self, segment_index: int) -> str:
        """
        Determine the type of body segment based on adjacent segments.
        
        Args:
            segment_index: Index of the body segment
            
        Returns:
            Body segment type string
        """
        if segment_index == 0 or segment_index >= len(self.body) - 1:
            return 'horizontal'  # Default fallback
        
        # Get current, previous, and next segment positions
        current = self.body[segment_index]
        prev = self.body[segment_index - 1]
        next_seg = self.body[segment_index + 1]
        
        # Calculate directions
        from_prev = (current[0] - prev[0], current[1] - prev[1])
        to_next = (next_seg[0] - current[0], next_seg[1] - current[1])
        
        # Determine segment type
        if from_prev == to_next:
            # Straight segment
            if from_prev[0] != 0:  # Horizontal
                return 'horizontal'
            else:  # Vertical
                return 'vertical'
        else:
            # Corner segment
            # This is a simplified corner detection
            # You might want to implement more sophisticated corner detection
            return 'horizontal'  # Default to horizontal for now
    
    def _render_fallback(self, surface: pygame.Surface) -> None:
        """Render snake using simple colored rectangles as fallback."""
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size, self.cell_size, self.cell_size)
            
            if i == 0:  # Head
                pygame.draw.rect(surface, (0, 255, 0), rect)
            elif i == len(self.body) - 1:  # Tail
                pygame.draw.rect(surface, (0, 200, 0), rect)
            else:  # Body
                pygame.draw.rect(surface, (0, 150, 0), rect)
