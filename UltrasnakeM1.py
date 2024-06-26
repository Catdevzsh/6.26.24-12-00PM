import pygame
import sys
import random
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Font setup
font = pygame.font.Font(None, 36)

# Define a function to generate pulse wave sounds
def generate_pulse_wave(frequency=440, duration=0.1, duty_cycle=0.5):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * (1 if i % (sample_rate // frequency) < (sample_rate // frequency) * duty_cycle else -1)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Define a function to generate noise sounds
def generate_noise_sound(duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * (random.random() * 2 - 1)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sound objects
eat_sound = generate_pulse_wave(440, 0.1, 0.5)  # Sound when the snake eats food
crash_sound = generate_noise_sound(0.1)  # Sound when the snake crashes

# Define the Snake class
class Snake:
    def __init__(self):
        self.positions = [(100, 100)]
        self.direction = (0, -CELL_SIZE)
        self.grow = False
        self.hp = 100  # Health points
        self.exp = 0   # Experience points

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % SCREEN_WIDTH, (head_y + dir_y) % SCREEN_HEIGHT)

        if new_head in self.positions[1:]:
            self.hp -= 10
            return False  # Collision with itself

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        self.grow = False
        return True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow_snake(self):
        self.grow = True
        self.exp += 10  # Gain experience points when eating food

    def draw(self, surface):
        for position in self.positions:
            pygame.draw.rect(surface, GREEN, pygame.Rect(position[0], position[1], CELL_SIZE, CELL_SIZE))

    def draw_status(self, surface):
        hp_text = font.render(f"HP: {self.hp}", True, BLUE)
        exp_text = font.render(f"EXP: {self.exp}", True, BLUE)
        surface.blit(hp_text, (10, 10))
        surface.blit(exp_text, (10, 50))

# Define the Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.new_position()

    def new_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

# Main game loop
def main_game():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    running = True
    update_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((CELL_SIZE, 0))

        update_count += 1
        if update_count % 15 == 0:  # Slow down the snake's movement to mimic Nokia Snake
            if not snake.move():
                crash_sound.play()
                if snake.hp <= 0:
                    running = False  # End game if snake collides with itself and HP is 0

            if snake.positions[0] == food.position:
                snake.grow_snake()
                food.new_position()
                eat_sound.play()

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        snake.draw_status(screen)

        pygame.display.flip()
        clock.tick(60)  # Run game at 60 frames per second

    pygame.quit()
    sys.exit()

# Main menu
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        title_text = font.render("Snake Game", True, WHITE)
        start_text = font.render("Press Enter to Start", True, WHITE)
        quit_text = font.render("Press ESC to Quit", True, WHITE)
        
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//3))
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT//2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                    main_game()
                elif event.key == pygame.K_ESCAPE:
                    menu_running = False
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
