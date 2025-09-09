"""
Main game class for the Snake game.
Handles game state, main loop, and rendering.
"""

import pygame
import sys
from typing import Optional
from config import *
from tileset_manager import TilesetManager
from snake import Snake
from food import Food
from utils import draw_centered_text, create_button, get_direction_from_keys


class GameState:
    """Enumeration of possible game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class SnakeGame:
    """
    Main game class that manages the game loop, state, and rendering.
    """
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        
        # Get screen dimensions for fullscreen
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        
        # Calculate cell size to fit 30x15 grid on screen with symmetric background border
        # We need 2 extra cells for walls on each side, plus 4 extra for symmetric background border
        # So total grid is 38x22 (30+2 walls+5 background border for better vertical balance)
        cell_width = self.screen_width // 38
        cell_height = self.screen_height // 22
        self.cell_size = min(cell_width, cell_height)
        
        # Calculate actual grid dimensions
        self.grid_width = 38  # 30 + 2 for walls + 6 for symmetric background border
        self.grid_height = 22  # 15 + 2 for walls + 5 for better vertical balance
        
        # Define playable area boundaries (inside walls)
        self.playable_width = 30
        self.playable_height = 15
        self.wall_start_x = 4  # Background tiles start at 0, walls start at 4
        self.wall_start_y = 3  # Adjusted for better vertical balance
        self.playable_start_x = 5  # Playable area starts at 5 (after wall)
        self.playable_start_y = 4  # Adjusted for better vertical balance
        
        # Calculate centered gameplay area offset
        total_grid_width = self.grid_width * self.cell_size
        total_grid_height = self.grid_height * self.cell_size
        self.grid_offset_x = (self.screen_width - total_grid_width) // 2
        self.grid_offset_y = (self.screen_height - total_grid_height) // 2
        
        # Set up display with fullscreen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Set up clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.tileset_manager = TilesetManager()
        self.snake = Snake(self.tileset_manager, self.cell_size, self.grid_width, self.grid_height, self.grid_offset_x, self.grid_offset_y, self.playable_start_x, self.playable_start_y, self.playable_width, self.playable_height)
        self.food = Food(self.tileset_manager, self.cell_size, self.grid_width, self.grid_height, self.grid_offset_x, self.grid_offset_y, self.playable_start_x, self.playable_start_y, self.playable_width, self.playable_height)
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.high_score = 0
        
        # Load pixel fonts
        try:
            self.font_large = pygame.font.Font("assets/fonts/PixelifySans-Bold.ttf", 72)
            self.font_medium = pygame.font.Font("assets/fonts/PixelifySans-SemiBold.ttf", 32)
            self.font_small = pygame.font.Font("assets/fonts/PixelifySans-Medium.ttf", 24)
        except pygame.error:
            # Fallback to default fonts if custom fonts fail to load
            self.font_large = pygame.font.Font(None, 72)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
        
        # Speed progression
        self.current_fps = INITIAL_FPS
        
        # Initialize music and sound effects
        self.current_music = None
        self._load_music()
        self._load_sound_effects()
        
        # Generate initial food
        self._generate_food()
        
        # Start with title music
        self._play_music('title')
    
    def _load_music(self) -> None:
        """Load music files."""
        try:
            pygame.mixer.init()
            self.music_files = {
                'title': "assets/music/title.wav",
                'game': "assets/music/main.wav", 
                'game_over': "assets/music/game_over.wav"
            }
        except pygame.error:
            self.music_files = None
    
    def _load_sound_effects(self) -> None:
        """Load sound effect files."""
        try:
            self.sound_effects = {
                'pause': pygame.mixer.Sound("assets/sound_effects/pause.wav"),
                'food': pygame.mixer.Sound("assets/sound_effects/food.wav")
            }
        except pygame.error:
            self.sound_effects = None
    
    def _play_music(self, music_type: str) -> None:
        """Play music for the specified game state."""
        if not self.music_files or music_type not in self.music_files:
            return
        
        # Stop current music if playing
        if self.current_music == music_type:
            return  # Already playing the right music
        
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(self.music_files[music_type])
            # Game over music plays only once, others loop
            if music_type == 'game_over':
                pygame.mixer.music.play(0)  # Play once
            else:
                pygame.mixer.music.play(-1)  # Loop indefinitely
            self.current_music = music_type
        except pygame.error:
            pass  # Silently fail if music can't be loaded
    
    def _play_sound(self, sound_type: str) -> None:
        """Play a sound effect."""
        if not self.sound_effects or sound_type not in self.sound_effects:
            return
        
        try:
            self.sound_effects[sound_type].play()
        except pygame.error:
            pass  # Silently fail if sound can't be played
    
    def run(self) -> None:
        """Run the main game loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_keydown(event.key)
            
            # Update game state
            self._update()
            
            # Render everything
            self._render()
            
            # Control frame rate with dynamic speed
            self.clock.tick(self.current_fps)
        
        pygame.quit()
        sys.exit()
    
    def _handle_keydown(self, key: int) -> None:
        """Handle key press events."""
        if self.state == GameState.MENU:
            if key == pygame.K_SPACE or key == pygame.K_RETURN:
                self._start_game()
            elif key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        elif self.state == GameState.PLAYING:
            if key == pygame.K_SPACE:
                self._pause_game()
            elif key == pygame.K_ESCAPE:
                self._return_to_menu()
            else:
                self._handle_movement_key(key)
        
        elif self.state == GameState.PAUSED:
            if key == pygame.K_SPACE:
                self._resume_game()
            elif key == pygame.K_ESCAPE:
                self._return_to_menu()
        
        elif self.state == GameState.GAME_OVER:
            if key == pygame.K_r:
                self._restart_game()
            elif key == pygame.K_ESCAPE:
                self._return_to_menu()
    
    def _handle_movement_key(self, key: int) -> None:
        """Handle movement key presses."""
        direction_map = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_d: (1, 0)
        }
        
        if key in direction_map:
            self.snake.update_direction(direction_map[key])
    
    def _update(self) -> None:
        """Update game logic based on current state."""
        if self.state == GameState.PLAYING:
            self._update_game()
    
    def _update_game(self) -> None:
        """Update the game during play state."""
        # Update food (handle cookie expiration)
        self.food.update()
        
        # Check if food expired
        if self.food.is_expired:
            self._generate_food()
        
        # Move snake
        if not self.snake.move():
            self._game_over()
            return
        
        # Check for food collision
        if self.food.is_eaten(self.snake.get_head_position()):
            self._eat_food()
            self._generate_food()
    
    def _start_game(self) -> None:
        """Start a new game."""
        self.state = GameState.PLAYING
        self.score = 0
        self.current_fps = INITIAL_FPS
        self.snake.reset()
        self._generate_food()
        self._play_music('game')
    
    def _pause_game(self) -> None:
        """Pause the game."""
        self.state = GameState.PAUSED
        self._play_sound('pause')
    
    def _resume_game(self) -> None:
        """Resume the paused game."""
        self.state = GameState.PLAYING
        self._play_sound('pause')  # Use same sound for resume
    
    def _game_over(self) -> None:
        """Handle game over."""
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
        self._play_music('game_over')
    
    def _restart_game(self) -> None:
        """Restart the current game."""
        self._start_game()
    
    def _return_to_menu(self) -> None:
        """Return to the main menu."""
        self.state = GameState.MENU
        self.snake.reset()
        self.score = 0
        self.current_fps = INITIAL_FPS
        self._play_music('title')
    
    def _eat_food(self) -> None:
        """Handle food consumption."""
        self.score += self.food.get_value()
        self._play_sound('food')  # Play food eating sound
        
        # Handle different growth amounts based on food type
        if self.food.is_cookie():
            # Cookie gives 2x length increase
            self.snake.grow()
            self.snake.grow()
        else:
            # Normal food gives 1x length increase
            self.snake.grow()
        
        self._update_speed()
    
    def _generate_food(self) -> None:
        """Generate new food at a random position."""
        snake_positions = self.snake.get_body_positions()
        self.food.generate(snake_positions, self.current_fps)
    
    def _update_speed(self) -> None:
        """Update the game speed based on current score."""
        # Calculate how many speed increases should have occurred
        speed_increases = self.score // SPEED_INCREASE_INTERVAL
        
        # Calculate new FPS
        new_fps = INITIAL_FPS + (speed_increases * SPEED_INCREASE_AMOUNT)
        
        # Cap at maximum FPS
        self.current_fps = min(new_fps, MAX_FPS)
    
    def _render(self) -> None:
        """Render the current game state."""
        if self.state == GameState.MENU:
            self.screen.fill(BLACK)
            self._render_menu()
        elif self.state == GameState.PLAYING:
            self._render_game()
        elif self.state == GameState.PAUSED:
            self._render_game()
            self._render_pause_overlay()
        elif self.state == GameState.GAME_OVER:
            self._render_game()
            self._render_game_over_overlay()
        
        pygame.display.flip()
    
    def _render_menu(self) -> None:
        """Render the main menu with vertically centered text."""
        # Calculate total height of all text elements for vertical centering
        title_height = self.font_large.get_height()  # Rainbow title height
        subtitle_height = self.font_medium.get_height()  # "Pixel Art Edition" height
        instruction_height = self.font_small.get_height()  # Instruction text height
        button_height = self.font_medium.get_height() + 24  # Button height (text + vertical padding)
        highscore_height = self.font_small.get_height()  # High score height
        
        # Calculate spacing between elements
        title_spacing = 20  # Space between title and subtitle
        subtitle_spacing = 40  # Space between subtitle and instructions
        instruction_spacing = 15  # Space between instruction lines (reduced from 30)
        instruction_button_spacing = 80  # Space between instructions and button (increased from 50)
        button_highscore_spacing = 10  # Space between button and high score (further reduced for better visual balance)
        
        # Calculate total content height - always include high score space for consistent centering
        total_content_height = (
            title_height + title_spacing +  # Title + spacing
            subtitle_height + subtitle_spacing +  # Subtitle + spacing
            instruction_height * 3 + instruction_spacing * 2 +  # 3 instruction lines + 2 spacings
            instruction_button_spacing +  # Space to button
            button_height + button_highscore_spacing +  # Button + spacing
            highscore_height  # High score (always reserved)
        )
        
        # Calculate starting Y position to center everything vertically
        # Add extra space at top to balance visual weight of large title
        visual_balance_offset = 40  # Extra space at top for visual balance (increased)
        start_y = (self.screen_height - total_content_height) // 2 + visual_balance_offset
        
        
        # Position each element
        current_y = start_y
        
        # Title with each letter in different color
        self._render_rainbow_title("SNAKE GAME", current_y)
        current_y += title_height + title_spacing
        
        # Subtitle
        draw_centered_text(self.screen, "Pixel Art Edition", self.font_medium, WHITE, current_y)
        current_y += subtitle_height + subtitle_spacing
        
        # Instructions
        draw_centered_text(self.screen, "Use arrow keys to move", self.font_small, (200, 200, 200), current_y)
        current_y += instruction_height + instruction_spacing
        draw_centered_text(self.screen, "Space to pause", self.font_small, (200, 200, 200), current_y)
        current_y += instruction_height + instruction_spacing
        draw_centered_text(self.screen, "ESC to quit", self.font_small, (200, 200, 200), current_y)
        current_y += instruction_height + instruction_button_spacing
        
        # Start button with white rounded background
        self._render_start_button("Press SPACE to start", current_y)
        current_y += button_height + button_highscore_spacing
        
        # High score - position it in the center of the reserved space for better visual balance
        highscore_center_y = current_y + highscore_height // 2
        
        if self.high_score > 0:
            draw_centered_text(self.screen, f"High Score: {self.high_score}", 
                             self.font_small, WHITE, highscore_center_y)
        # Note: Space is always reserved for high score to maintain consistent vertical centering
    
    def _render_rainbow_title(self, text: str, y_pos: int) -> None:
        """Render title text with each letter in a different color."""
        # Define a rainbow color palette
        colors = [
            (255, 0, 0),      # Red
            (255, 165, 0),    # Orange
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (0, 0, 255),      # Blue
            (75, 0, 130),     # Indigo
            (238, 130, 238),  # Violet
            (255, 192, 203),  # Pink
            (0, 255, 255),    # Cyan
            (255, 20, 147)    # Deep Pink
        ]
        
        # Use the EXACT same method as draw_centered_text
        text_surface = self.font_large.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, y_pos))
        base_x = text_rect.x
        
        
        # Now render each letter individually starting from the base position
        current_x = base_x
        for i, letter in enumerate(text):
            if letter == ' ':
                # Add space width
                space_width = self.font_large.size(' ')[0]
                current_x += space_width
            else:
                color = colors[i % len(colors)]
                letter_surface = self.font_large.render(letter, True, color)
                self.screen.blit(letter_surface, (current_x, y_pos))
                current_x += letter_surface.get_width()
    
    def _render_start_button(self, text: str, y_pos: int) -> None:
        """Render start button with white rounded rectangle background and black text."""
        # Render text to get dimensions
        text_surface = self.font_medium.render(text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect()
        
        # Add padding around the text
        padding_horizontal = 24  # Increased horizontal padding
        padding_vertical = 12    # Keep vertical padding the same
        button_width = text_rect.width + (padding_horizontal * 2)
        button_height = text_rect.height + (padding_vertical * 2)
        
        # Center the button horizontally (exactly matching draw_centered_text)
        # Use the text surface rect for perfect alignment, then adjust for button padding
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 0))
        button_x = text_rect.x - padding_horizontal  # Adjust for button padding
        
        button_y = y_pos - (button_height // 2)
        
        # Create rounded rectangle background
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=100)
        
        # Draw a subtle border
        pygame.draw.rect(self.screen, (100, 100, 100), button_rect, width=2, border_radius=100)
        
        # Center text on the button
        text_x = button_x + padding_horizontal
        text_y = button_y + padding_vertical
        self.screen.blit(text_surface, (text_x, text_y))
    
    def _render_game(self) -> None:
        """Render the game during play state."""
        # Render background
        self._render_background()
        
        # Render food
        self.food.render(self.screen)
        
        # Render snake
        self.snake.render(self.screen)
        
        # Render UI
        self._render_ui()
    
    def _render_background(self) -> None:
        """Render the game background and walls."""
        # Fill entire screen with black background
        self.screen.fill(BLACK)
        
        if self.tileset_manager.is_loaded():
            background_sprite = self.tileset_manager.get_background_sprite()
            if background_sprite:
                # Scale background sprite to cell size
                scaled_background = pygame.transform.scale(background_sprite, (self.cell_size, self.cell_size))
                
                # Fill entire grid with background tiles (including border around walls)
                for x in range(self.grid_width):
                    for y in range(self.grid_height):
                        pixel_pos = (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + y * self.cell_size)
                        self.screen.blit(scaled_background, pixel_pos)
                
                # Render walls around the border
                self._render_walls()
                return
        
        # Fallback: simple grid background
        for x in range(0, self.screen_width, self.cell_size):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.cell_size):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (self.screen_width, y))
    
    def _render_walls(self) -> None:
        """Render wall tiles around the game border using your specific wall layout."""
        if not self.tileset_manager.is_loaded():
            return
        
        # Get wall sprites and scale them
        wall_top_corner = self.tileset_manager.get_sprite('wall_top_corner')
        wall_bottom_corner = self.tileset_manager.get_sprite('wall_bottom_corner')
        wall_left = self.tileset_manager.get_sprite('wall_left')
        wall_right = self.tileset_manager.get_sprite('wall_right')
        wall_top = self.tileset_manager.get_sprite('wall_top')
        wall_bottom = self.tileset_manager.get_sprite('wall_bottom')
        wall_inside = self.tileset_manager.get_sprite('wall_inside')
        
        # Scale sprites to cell size
        if wall_top_corner:
            wall_top_corner = pygame.transform.scale(wall_top_corner, (self.cell_size, self.cell_size))
        if wall_bottom_corner:
            wall_bottom_corner = pygame.transform.scale(wall_bottom_corner, (self.cell_size, self.cell_size))
        if wall_left:
            wall_left = pygame.transform.scale(wall_left, (self.cell_size, self.cell_size))
        if wall_right:
            wall_right = pygame.transform.scale(wall_right, (self.cell_size, self.cell_size))
        if wall_top:
            wall_top = pygame.transform.scale(wall_top, (self.cell_size, self.cell_size))
        if wall_bottom:
            wall_bottom = pygame.transform.scale(wall_bottom, (self.cell_size, self.cell_size))
        
        # Render top corners (left and right) - walls start at position 2
        if wall_top_corner:
            self.screen.blit(wall_top_corner, (self.grid_offset_x + self.wall_start_x * self.cell_size, self.grid_offset_y + self.wall_start_y * self.cell_size))  # Top-left
            self.screen.blit(wall_top_corner, (self.grid_offset_x + (self.wall_start_x + self.playable_width + 1) * self.cell_size, self.grid_offset_y + self.wall_start_y * self.cell_size))  # Top-right
        
        # Render bottom corners (left and right)
        if wall_bottom_corner:
            self.screen.blit(wall_bottom_corner, (self.grid_offset_x + self.wall_start_x * self.cell_size, self.grid_offset_y + (self.wall_start_y + self.playable_height + 1) * self.cell_size))  # Bottom-left
            self.screen.blit(wall_bottom_corner, (self.grid_offset_x + (self.wall_start_x + self.playable_width + 1) * self.cell_size, self.grid_offset_y + (self.wall_start_y + self.playable_height + 1) * self.cell_size))  # Bottom-right
        
        # Render left side border
        if wall_left:
            for y in range(self.wall_start_y + 1, self.wall_start_y + self.playable_height + 1):
                self.screen.blit(wall_left, (self.grid_offset_x + self.wall_start_x * self.cell_size, self.grid_offset_y + y * self.cell_size))
        
        # Render right side border
        if wall_right:
            for y in range(self.wall_start_y + 1, self.wall_start_y + self.playable_height + 1):
                self.screen.blit(wall_right, (self.grid_offset_x + (self.wall_start_x + self.playable_width + 1) * self.cell_size, self.grid_offset_y + y * self.cell_size))
        
        # Render top side border
        if wall_top:
            for x in range(self.wall_start_x + 1, self.wall_start_x + self.playable_width + 1):
                self.screen.blit(wall_top, (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + self.wall_start_y * self.cell_size))
        
        # Render bottom side border
        if wall_bottom:
            for x in range(self.wall_start_x + 1, self.wall_start_x + self.playable_width + 1):
                self.screen.blit(wall_bottom, (self.grid_offset_x + x * self.cell_size, self.grid_offset_y + (self.wall_start_y + self.playable_height + 1) * self.cell_size))
        
        # Note: Removed wall_inside overlay to show proper wall tiles
    
    def _render_ui(self) -> None:
        """Render the game UI (score only) in the black border area."""
        # Score in top-left corner of black border
        score_text = f"Score: {self.score}"
        score_surface = self.font_medium.render(score_text, True, WHITE)
        self.screen.blit(score_surface, (10, 10))
        
        # High score in top-right corner of black border
        if self.high_score > 0:
            high_score_text = f"High: {self.high_score}"
            high_score_surface = self.font_small.render(high_score_text, True, WHITE)
            # Position in top-right corner
            high_score_x = self.screen_width - high_score_surface.get_width() - 10
            self.screen.blit(high_score_surface, (high_score_x, 10))
    
    def _render_pause_overlay(self) -> None:
        """Render the pause overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        draw_centered_text(self.screen, "PAUSED", self.font_large, WHITE, self.screen_height // 2 - 50)
        draw_centered_text(self.screen, "Press SPACE to resume", self.font_medium, WHITE, self.screen_height // 2 + 20)
        draw_centered_text(self.screen, "Press ESC for menu", self.font_small, WHITE, self.screen_height // 2 + 60)
    
    def _render_game_over_overlay(self) -> None:
        """Render the game over overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        draw_centered_text(self.screen, "GAME OVER", self.font_large, RED, self.screen_height // 2 - 120)
        draw_centered_text(self.screen, f"Final Score: {self.score}", self.font_medium, WHITE, self.screen_height // 2 - 40)
        
        if self.score == self.high_score and self.score > 0:
            draw_centered_text(self.screen, "NEW HIGH SCORE!", self.font_medium, GREEN, self.screen_height // 2 - 10)
        
        draw_centered_text(self.screen, "Press R to restart", self.font_medium, WHITE, self.screen_height // 2 + 30)
        draw_centered_text(self.screen, "Press ESC for menu", self.font_small, WHITE, self.screen_height // 2 + 70)
