"""
Setup script for the Snake Game project.
This script helps set up the development environment.
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required Python packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def check_tileset():
    """Check if tileset file exists."""
    tileset_path = "assets/tileset.png"
    if os.path.exists(tileset_path):
        print(f"✅ Tileset found: {tileset_path}")
        return True
    else:
        print(f"⚠️  Tileset not found: {tileset_path}")
        print("   Please place your tileset PNG file in the assets/ folder")
        return False


def main():
    """Main setup function."""
    print("🐍 Snake Game Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check for tileset
    tileset_exists = check_tileset()
    
    print("\n🎮 Setup Complete!")
    print("=" * 20)
    
    if tileset_exists:
        print("✅ Ready to play!")
        print("   Run: python src/main.py")
        print("   Test: python test_tileset.py")
    else:
        print("⚠️  Almost ready!")
        print("   1. Place your tileset.png in the assets/ folder")
        print("   2. Update sprite coordinates in src/config.py if needed")
        print("   3. Run: python test_tileset.py")
        print("   4. Run: python src/main.py")
    
    return True


if __name__ == "__main__":
    main()


