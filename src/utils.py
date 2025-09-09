"""
Utility functions for the Snake game.
Contains helper functions for common operations.
"""

import pygame
from typing import Tuple, List
from config import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE


def grid_to_pixel(grid_pos: Tuple[int, int]) -> Tuple[int, int]:
    """
    Convert grid coordinates to pixel coordinates.
    
    Args:
        grid_pos: Position in grid coordinates (x, y)
        
    Returns:
        Position in pixel coordinates (x, y)
    """
    x, y = grid_pos
    pixel_x = x * CELL_SIZE
    pixel_y = y * CELL_SIZE
    return (pixel_x, pixel_y)


def pixel_to_grid(pixel_pos: Tuple[int, int]) -> Tuple[int, int]:
    """
    Convert pixel coordinates to grid coordinates.
    
    Args:
        pixel_pos: Position in pixel coordinates (x, y)
        
    Returns:
        Position in grid coordinates (x, y)
    """
    x, y = pixel_pos
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    return (grid_x, grid_y)


def is_valid_position(pos: Tuple[int, int]) -> bool:
    """
    Check if a position is within the playable area (excluding walls).
    
    Args:
        pos: Position to check (x, y)
        
    Returns:
        True if position is valid, False otherwise
    """
    x, y = pos
    # Exclude border walls (positions 0, GRID_WIDTH-1, 0, GRID_HEIGHT-1)
    return 1 <= x < GRID_WIDTH - 1 and 1 <= y < GRID_HEIGHT - 1


def clamp_position(pos: Tuple[int, int]) -> Tuple[int, int]:
    """
    Clamp a position to stay within the game grid bounds.
    
    Args:
        pos: Position to clamp (x, y)
        
    Returns:
        Clamped position within grid bounds
    """
    x, y = pos
    x = max(0, min(x, GRID_WIDTH - 1))
    y = max(0, min(y, GRID_HEIGHT - 1))
    return (x, y)


def get_random_position(exclude_positions: List[Tuple[int, int]] = None) -> Tuple[int, int]:
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
    
    while True:
        # Only generate positions within the playable area (excluding walls)
        x = random.randint(1, GRID_WIDTH - 2)
        y = random.randint(1, GRID_HEIGHT - 2)
        pos = (x, y)
        
        if pos not in exclude_positions:
            return pos


def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font, 
              color: Tuple[int, int, int], pos: Tuple[int, int], 
              center: bool = False) -> None:
    """
    Draw text on a surface with optional centering.
    
    Args:
        surface: Surface to draw on
        text: Text to draw
        font: Font to use
        color: Text color (R, G, B)
        pos: Position to draw at (x, y)
        center: Whether to center the text at the position
    """
    text_surface = font.render(text, True, color)
    
    if center:
        text_rect = text_surface.get_rect(center=pos)
        surface.blit(text_surface, text_rect)
    else:
        surface.blit(text_surface, pos)


def draw_centered_text(surface: pygame.Surface, text: str, font: pygame.font.Font, 
                      color: Tuple[int, int, int], y: int) -> None:
    """
    Draw centered text on a surface.
    
    Args:
        surface: Surface to draw on
        text: Text to draw
        font: Font to use
        color: Text color (R, G, B)
        y: Y position for the text
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(text_surface, text_rect)


def create_button(surface: pygame.Surface, text: str, font: pygame.font.Font,
                 color: Tuple[int, int, int], bg_color: Tuple[int, int, int],
                 rect: pygame.Rect, border_color: Tuple[int, int, int] = None,
                 border_width: int = 2) -> pygame.Rect:
    """
    Create a button with text on a surface.
    
    Args:
        surface: Surface to draw on
        text: Button text
        font: Font to use
        color: Text color (R, G, B)
        bg_color: Background color (R, G, B)
        rect: Button rectangle
        border_color: Border color (R, G, B), optional
        border_width: Border width in pixels
        
    Returns:
        The button rectangle
    """
    # Draw background
    pygame.draw.rect(surface, bg_color, rect)
    
    # Draw border if specified
    if border_color:
        pygame.draw.rect(surface, border_color, rect, border_width)
    
    # Draw text centered in button
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)
    
    return rect


def get_direction_from_keys() -> Tuple[int, int]:
    """
    Get movement direction based on currently pressed keys.
    
    Returns:
        Direction tuple (x, y) or (0, 0) if no movement keys pressed
    """
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        return (0, -1)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        return (0, 1)
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        return (-1, 0)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        return (1, 0)
    
    return (0, 0)
