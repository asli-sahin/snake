"""
Main entry point for the Snake game.
This is the file you run to start the game.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import SnakeGame


def main():
    """Main function to start the game."""
    print("🐍 Starting Snake Game - Pixel Art Edition")
    print("=" * 50)
    
    try:
        # Create and run the game
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\n👋 Game interrupted by user")
    except Exception as e:
        print(f"❌ Error running game: {e}")
        print("Make sure you have pygame installed: pip install pygame")
        print("And that your tileset.png file is in the assets/ folder")
    finally:
        print("🎮 Thanks for playing!")


if __name__ == "__main__":
    main()


