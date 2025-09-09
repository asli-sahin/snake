"""
Test script to verify tileset extraction works correctly.
Run this to test your tileset before running the main game.
"""

import pygame
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Import with absolute imports
from tileset_manager import TilesetManager
from config import SPRITE_COORDS, TILE_WIDTH, TILE_HEIGHT


def test_tileset():
    """Test the tileset manager and display all extracted sprites."""
    print("🧪 Testing Tileset Extraction")
    print("=" * 40)
    
    # Initialize Pygame
    pygame.init()
    
    # Create tileset manager
    tileset_manager = TilesetManager()
    
    if not tileset_manager.is_loaded():
        print("❌ Tileset not loaded. Make sure 'assets/tileset.png' exists.")
        return False
    
    # Get tileset info
    info = tileset_manager.get_tileset_info()
    print(f"✓ Tileset loaded: {info['width']}x{info['height']} pixels")
    print(f"✓ Tile size: {info['tile_width']}x{info['tile_height']} pixels")
    print(f"✓ Grid size: {info['tiles_x']}x{info['tiles_y']} tiles")
    print()
    
    # Test sprite extraction
    print("🔍 Testing sprite extraction...")
    success_count = 0
    total_sprites = len(SPRITE_COORDS)
    
    for sprite_name, (x, y) in SPRITE_COORDS.items():
        sprite = tileset_manager.get_sprite(sprite_name)
        if sprite:
            print(f"✓ {sprite_name} at ({x}, {y}) - {sprite.get_width()}x{sprite.get_height()}")
            success_count += 1
        else:
            print(f"❌ {sprite_name} at ({x}, {y}) - FAILED")
    
    print(f"\n📊 Results: {success_count}/{total_sprites} sprites loaded successfully")
    
    if success_count == total_sprites:
        print("🎉 All sprites loaded successfully! Your tileset is ready.")
        return True
    else:
        print("⚠️  Some sprites failed to load. Check your tileset layout and coordinates.")
        return False


def display_tileset():
    """Display the tileset in a window for visual inspection."""
    print("\n🖼️  Opening tileset viewer...")
    
    # Initialize Pygame
    pygame.init()
    
    # Create tileset manager
    tileset_manager = TilesetManager()
    
    if not tileset_manager.is_loaded():
        print("❌ Cannot display tileset - file not loaded.")
        return
    
    # Load the tileset
    tileset = pygame.image.load("assets/tileset.png")
    
    # Create window
    screen = pygame.display.set_mode((tileset.get_width(), tileset.get_height()))
    pygame.display.set_caption("Tileset Viewer - Press ESC to close")
    
    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        # Draw tileset
        screen.fill((0, 0, 0))
        screen.blit(tileset, (0, 0))
        
        # Draw grid overlay
        for x in range(0, tileset.get_width(), TILE_WIDTH):
            pygame.draw.line(screen, (255, 255, 255, 100), (x, 0), (x, tileset.get_height()))
        for y in range(0, tileset.get_height(), TILE_HEIGHT):
            pygame.draw.line(screen, (255, 255, 255, 100), (0, y), (tileset.get_width(), y))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    print("🐍 Snake Game - Tileset Tester")
    print("=" * 50)
    
    # Test tileset extraction
    if test_tileset():
        print("\nWould you like to view the tileset? (y/n): ", end="")
        try:
            response = input().lower().strip()
            if response in ['y', 'yes']:
                display_tileset()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    
    print("\n🎮 Ready to play! Run 'python src/main.py' to start the game.")
