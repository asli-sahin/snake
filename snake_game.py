import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 8
SCALE = 4
SCALED_TILE_SIZE = TILE_SIZE * SCALE

# Get screen dimensions
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Calculate grid size to fit screen with padding and sidebar
PADDING_TILES = 4  # 2 tiles padding on each side
SIDEBAR_WIDTH = 8  # 8 tiles for sidebar on the right
PADDING_OFFSET = 2 * SCALED_TILE_SIZE  # 2 tiles padding in pixels
SIDEBAR_WIDTH_PX = SIDEBAR_WIDTH * SCALED_TILE_SIZE  # Sidebar width in pixels
GRID_WIDTH = (SCREEN_WIDTH // SCALED_TILE_SIZE) - PADDING_TILES - SIDEBAR_WIDTH
GRID_HEIGHT = (SCREEN_HEIGHT // SCALED_TILE_SIZE) - PADDING_TILES

# Ensure minimum grid size
GRID_WIDTH = max(GRID_WIDTH, 20)
GRID_HEIGHT = max(GRID_HEIGHT, 15)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
GREY = (128, 128, 128)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Load tileset
        self.tileset = pygame.image.load("assets/tileset.png")
        
        # Extract sprites from tileset (8x8 pixels each)
        self.sprites = self.extract_sprites()
        
        # Game state
        self.snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food = Food(self.snake.body)
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.paused = True  # Start in paused state
        self.game_started = False  # Track if game has been started
        
        # Dynamic FPS system
        self.base_fps = 3  # Starting FPS
        self.max_fps = 12  # Maximum FPS
        self.fps_increment = 1  # FPS increase per level
        self.food_count = 0  # Track food eaten
        self.food_per_level = 3  # Food needed to increase FPS
        self.current_fps = self.base_fps
        
        # Load sound effects
        try:
            self.food_sound = pygame.mixer.Sound("assets/sound_effects/food.wav")
            self.pause_sound = pygame.mixer.Sound("assets/sound_effects/pause.wav")
        except:
            self.food_sound = None
            self.pause_sound = None
        
        # Load fonts
        try:
            self.font_large = pygame.font.Font("assets/fonts/PixelifySans-Bold.ttf", 48)
            self.font_medium = pygame.font.Font("assets/fonts/PixelifySans-SemiBold.ttf", 36)
            self.font_small = pygame.font.Font("assets/fonts/PixelifySans-Medium.ttf", 24)
            self.font_tiny = pygame.font.Font("assets/fonts/PixelifySans-Regular.ttf", 18)
            self.font_huge = pygame.font.Font("assets/fonts/PixelifySans-Bold.ttf", 72)  # Extra large for game over
        except:
            # Fallback to default fonts if custom fonts fail to load
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
            self.font_tiny = pygame.font.Font(None, 18)
            self.font_huge = pygame.font.Font(None, 72)
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open("high_score.txt", "r") as f:
                return int(f.read().strip())
        except:
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def extract_sprites(self):
        """Extract individual sprites from the tileset"""
        sprites = {}
        
        # Snake sprites (4th row)
        sprites['snake_head_up'] = self.get_sprite(1, 3)      # 2nd column
        sprites['snake_head_left'] = self.get_sprite(2, 3)     # 3rd column
        sprites['snake_head_down'] = self.get_sprite(3, 3)     # 4th column
        sprites['snake_head_right'] = self.get_sprite(4, 3)    # 5th column
        sprites['snake_body'] = self.get_sprite(5, 3)          # 6th column
        sprites['cherry'] = self.get_sprite(6, 3)              # 7th column
        sprites['cookie'] = self.get_sprite(7, 3)              # 8th column
        
        # Wall sprites (1st row)
        sprites['wall_tl'] = self.get_sprite(13, 0)            # 13th column
        sprites['wall_tr'] = self.get_sprite(12, 0)            # 14th column
        
        # Wall sprites (3rd row)
        sprites['wall_bottom'] = self.get_sprite(7, 2)         # 8th column
        sprites['wall_right'] = self.get_sprite(8, 2)          # 9th column
        sprites['wall_left'] = self.get_sprite(9, 2)           # 10th column
        sprites['wall_top'] = self.get_sprite(10, 2)           # 11th column
        
        return sprites
    
    def get_sprite(self, col, row):
        """Extract a sprite from the tileset at given column and row"""
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sprite.blit(self.tileset, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
        sprite = pygame.transform.scale(sprite, (SCALED_TILE_SIZE, SCALED_TILE_SIZE))
        sprite.set_colorkey((0, 0, 0))  # Make black transparent
        return sprite
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_F11:
                    # Toggle fullscreen
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    else:
                        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.restart_game()
                    elif not self.game_started:
                        # Start the game for the first time
                        self.game_started = True
                        self.paused = False
                    else:
                        # Toggle pause during gameplay
                        self.paused = not self.paused
                        if self.pause_sound:
                            self.pause_sound.play()
                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_UP:
                        self.snake.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.set_direction(Direction.RIGHT)
        return True
    
    def update(self):
        """Update game logic"""
        if self.game_over or self.paused:
            return
        
        # Move snake
        self.snake.move()
        
        # Check wall collision
        head = self.snake.body[0]
        if (head[0] < 1 or head[0] >= GRID_WIDTH - 1 or 
            head[1] < 1 or head[1] > GRID_HEIGHT - 1):
            self.game_over = True
            return
        
        # Check self collision
        if head in self.snake.body[1:]:
            self.game_over = True
            return
        
        # Check food collision
        if head == self.food.position:
            self.snake.grow()
            self.score += self.food.points
            self.food_count += 1
            
            # Increase FPS every 3 food intakes
            if self.food_count % self.food_per_level == 0 and self.current_fps < self.max_fps:
                self.current_fps = min(self.current_fps + self.fps_increment, self.max_fps)
            
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            if self.food_sound:
                self.food_sound.play()
            self.food = Food(self.snake.body)
    
    def draw_walls(self):
        """Draw the wall boundaries"""
        offset_x = PADDING_OFFSET
        offset_y = PADDING_OFFSET
        
        # Top wall
        for x in range(1, GRID_WIDTH - 1):
            self.screen.blit(self.sprites['wall_top'], (offset_x + x * SCALED_TILE_SIZE, offset_y))
        
        # Bottom wall
        for x in range(1, GRID_WIDTH - 1):
            self.screen.blit(self.sprites['wall_bottom'], (offset_x + x * SCALED_TILE_SIZE, offset_y + GRID_HEIGHT * SCALED_TILE_SIZE))
        
        # Left wall
        for y in range(1, GRID_HEIGHT):
            self.screen.blit(self.sprites['wall_left'], (offset_x, offset_y + y * SCALED_TILE_SIZE))
        
        # Right wall
        for y in range(1, GRID_HEIGHT):
            self.screen.blit(self.sprites['wall_right'], (offset_x + (GRID_WIDTH - 1) * SCALED_TILE_SIZE, offset_y + y * SCALED_TILE_SIZE))
        
        # Corners
        self.screen.blit(self.sprites['wall_tl'], (offset_x, offset_y))
        self.screen.blit(self.sprites['wall_tr'], (offset_x + (GRID_WIDTH - 1) * SCALED_TILE_SIZE, offset_y))
        self.screen.blit(self.sprites['wall_tl'], (offset_x, offset_y + GRID_HEIGHT * SCALED_TILE_SIZE))
        self.screen.blit(self.sprites['wall_tr'], (offset_x + (GRID_WIDTH - 1) * SCALED_TILE_SIZE, offset_y + GRID_HEIGHT * SCALED_TILE_SIZE))
    
    def draw_sidebar(self):
        """Draw the sidebar with game information"""
        sidebar_x = (2 + GRID_WIDTH + 2) * SCALED_TILE_SIZE  # Start after game area with 2 tiles gap (same as left padding)
        sidebar_y = 2 * SCALED_TILE_SIZE  # Same as game area top
        sidebar_height = (GRID_HEIGHT + 1) * SCALED_TILE_SIZE  # Same height as walls (from top padding to bottom wall)
        
        # Draw sidebar background
        sidebar_rect = pygame.Rect(sidebar_x, sidebar_y, SIDEBAR_WIDTH_PX, sidebar_height)
        pygame.draw.rect(self.screen, BLACK, sidebar_rect)
        pygame.draw.rect(self.screen, WHITE, sidebar_rect, 2)
        
        # Draw game information
        y_offset = 60  # Increased from 40 to add more space above SNAKE title
        
        # Title - each letter in different color
        title_colors = [RED, BLUE, GREEN, PURPLE, CYAN]
        title_letters = ["S", "N", "A", "K", "E"]
        letter_spacing = 32  # Increased spacing between letters
        total_width = (len(title_letters) - 1) * letter_spacing
        title_x = sidebar_x + (SIDEBAR_WIDTH_PX) // 2 - total_width // 2  # Center the word
        
        for i, (letter, color) in enumerate(zip(title_letters, title_colors)):
            letter_text = self.font_large.render(letter, True, color)
            letter_rect = letter_text.get_rect(center=(title_x + i * letter_spacing, sidebar_y + y_offset))
            self.screen.blit(letter_text, letter_rect)
        y_offset += 60
        
        # Current Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH_PX) // 2, sidebar_y + y_offset))
        self.screen.blit(score_text, score_rect)
        y_offset += 40
        
        # High Score
        high_score_text = self.font_medium.render(f"High: {self.high_score}", True, YELLOW)
        high_score_rect = high_score_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH_PX) // 2, sidebar_y + y_offset))
        self.screen.blit(high_score_text, high_score_rect)
        y_offset += 60
        
        # Snake Length
        length_text = self.font_small.render(f"Length: {len(self.snake.body)}", True, WHITE)
        length_rect = length_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH_PX) // 2, sidebar_y + y_offset))
        self.screen.blit(length_text, length_rect)
        y_offset += 30
        
        # Food Type
        food_type = "Cherry" if self.food.sprite_name == 'cherry' else "Cookie"
        food_text = self.font_small.render(f"Next: {food_type}", True, WHITE)
        food_rect = food_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH_PX) // 2, sidebar_y + y_offset))
        self.screen.blit(food_text, food_rect)
        y_offset += 30
        
        # Points Value
        points_text = self.font_small.render(f"Worth: {self.food.points}", True, WHITE)
        points_rect = points_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH_PX) // 2, sidebar_y + y_offset))
        self.screen.blit(points_text, points_rect)
        y_offset += 30
        
        # Current Speed
        speed_text = self.font_small.render(f"Speed: {self.current_fps} FPS", True, WHITE)
        speed_rect = speed_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH_PX) // 2, sidebar_y + y_offset))
        self.screen.blit(speed_text, speed_rect)
        y_offset += 60
        
        # Controls
        controls = [
            "CONTROLS:",
            "Arrow Keys Move",
            "SPACE Pause",
            "F11 Fullscreen",
            "ESC Quit"
        ]
        
        for i, control in enumerate(controls):
            if i == 0:  # Title
                control_text = self.font_small.render(control, True, GREY)
            else:  # Individual controls
                control_text = self.font_tiny.render(control, True, GREY)
            control_rect = control_text.get_rect(center=(sidebar_x + (SIDEBAR_WIDTH_PX) // 2, sidebar_y + y_offset))
            self.screen.blit(control_text, control_rect)
            y_offset += 25
    
    def draw(self):
        """Draw the game"""
        self.screen.fill(BLACK)
        
        # Draw walls
        self.draw_walls()
        
        # Draw food
        offset_x = PADDING_OFFSET
        offset_y = PADDING_OFFSET
        food_x = offset_x + self.food.position[0] * SCALED_TILE_SIZE
        food_y = offset_y + self.food.position[1] * SCALED_TILE_SIZE
        self.screen.blit(self.sprites[self.food.sprite_name], (food_x, food_y))
        
        # Draw snake
        for i, segment in enumerate(self.snake.body):
            x = offset_x + segment[0] * SCALED_TILE_SIZE
            y = offset_y + segment[1] * SCALED_TILE_SIZE
            
            if i == 0:  # Head
                head_sprite = f'snake_head_{self.snake.direction.name.lower()}'
                self.screen.blit(self.sprites[head_sprite], (x, y))
            else:  # Body
                self.screen.blit(self.sprites['snake_body'], (x, y))
        
        # Draw sidebar
        self.draw_sidebar()
        
        # Draw game over/pause/start messages
        if self.game_over:
            # "GAME OVER" in red huge font
            game_over_text = self.font_huge.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            
            # "Press SPACE to restart" in grey smaller font
            restart_text = self.font_medium.render("Press SPACE to restart", True, GREY)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            
            # Draw black background for both texts
            combined_rect = pygame.Rect.union(game_over_rect, restart_rect)
            bg_rect = combined_rect.inflate(20, 10)  # Add padding around text
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            
            # Draw both texts
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        elif self.paused and not self.game_started:
            start_text = self.font_large.render("Press SPACE to start", True, GREEN)
            text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            # Draw black background
            bg_rect = text_rect.inflate(20, 10)  # Add padding around text
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            self.screen.blit(start_text, text_rect)
        elif self.paused and self.game_started:
            pause_text = self.font_large.render("PAUSED - Press SPACE to continue", True, GREEN)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            # Draw black background
            bg_rect = text_rect.inflate(20, 10)  # Add padding around text
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            self.screen.blit(pause_text, text_rect)
        
        pygame.display.flip()
    
    def restart_game(self):
        """Restart the game"""
        self.snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.paused = True  # Start paused after restart
        self.game_started = False  # Reset game started state
        
        # Reset FPS system
        self.food_count = 0
        self.current_fps = self.base_fps
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.current_fps)  # Dynamic FPS that increases with food intake
        
        pygame.quit()
        sys.exit()

class Snake:
    def __init__(self, x, y):
        self.body = [(x, y), (x - 1, y)]  # Start with head and one body segment
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT  # Queue for next direction change
    
    def move(self):
        """Move the snake in the current direction"""
        # Apply queued direction change if valid
        if self.can_change_direction(self.next_direction):
            self.direction = self.next_direction
        
        head = self.body[0]
        new_head = (head[0] + self.direction.value[0], head[1] + self.direction.value[1])
        self.body.insert(0, new_head)
        self.body.pop()
    
    def can_change_direction(self, new_direction):
        """Check if the snake can change to the new direction"""
        # Can't reverse direction
        if (self.direction == Direction.UP and new_direction == Direction.DOWN) or \
           (self.direction == Direction.DOWN and new_direction == Direction.UP) or \
           (self.direction == Direction.LEFT and new_direction == Direction.RIGHT) or \
           (self.direction == Direction.RIGHT and new_direction == Direction.LEFT):
            return False
        return True
    
    def set_direction(self, new_direction):
        """Set the next direction for the snake"""
        if self.can_change_direction(new_direction):
            self.next_direction = new_direction
    
    def grow(self):
        """Grow the snake by one segment"""
        tail = self.body[-1]
        self.body.append(tail)

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
        self.sprite_name = random.choice(['cherry', 'cookie'])
        self.points = 10 if self.sprite_name == 'cherry' else 20
    
    def generate_position(self, snake_body):
        """Generate a random position not occupied by snake"""
        while True:
            x = random.randint(1, GRID_WIDTH - 2)
            y = random.randint(1, GRID_HEIGHT - 1)
            if (x, y) not in snake_body:
                return (x, y)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
