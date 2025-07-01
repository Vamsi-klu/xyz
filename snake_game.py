import random
import sys

# Game constants
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20
SNAKE_SPEED = 15
SNOW_SPEED = 5  # Slightly slower than snake's movement
SNOW_COUNT = 15  # Target number of snowflakes
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

try:
    import pygame
except ImportError:
    print("Pygame is not installed. Please install it using 'pip install pygame'")
    sys.exit()

class Snake:
    def __init__(self):
        self.body = [(WIDTH//2, HEIGHT//2)]
        self.direction = 'RIGHT'
        self.new_direction = 'RIGHT'
        
    def move(self):
        # Update direction with input delay to prevent 180° turns
        self.direction = self.new_direction
        head_x, head_y = self.body[0]
        
        if self.direction == 'RIGHT':
            new_head = (head_x + CELL_SIZE, head_y)
        elif self.direction == 'LEFT':
            new_head = (head_x - CELL_SIZE, head_y)
        elif self.direction == 'UP':
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + CELL_SIZE)
            
        self.body.insert(0, new_head)
        self.body.pop()
        
    def grow(self):
        self.body.append(self.body[-1])
        
    def check_collision(self):
        head = self.body[0]
        return (head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT or
                head in self.body[1:])

class Snowflake:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.speed = SNOW_SPEED
        
    def move(self):
        self.y += self.speed
        
    def off_screen(self):
        return self.y > HEIGHT

def game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = (random.randint(0, (WIDTH-CELL_SIZE)//CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT-CELL_SIZE)//CELL_SIZE) * CELL_SIZE)
    
    snowflakes = [Snowflake() for _ in range(SNOW_COUNT)]
    spawn_counter = 0
    
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'DOWN':
                    snake.new_direction = 'UP'
                elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                    snake.new_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                    snake.new_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                    snake.new_direction = 'RIGHT'
        
        # Snake movement
        snake.move()
        
        # Check collisions
        if (snake.check_collision() or 
            any((flake.x == snake.body[0][0] and flake.y == snake.body[0][1]) 
                for flake in snowflakes)):
            game_over(screen)
            return
        
        # Food consumption
        if snake.body[0] == food:
            snake.grow()
            food = (random.randint(0, (WIDTH-CELL_SIZE)//CELL_SIZE) * CELL_SIZE,
                    random.randint(0, (HEIGHT-CELL_SIZE)//CELL_SIZE) * CELL_SIZE)
        
        # Snow management
        spawn_counter += 1
        if spawn_counter >= 5:  # Spawn new snow periodically
            snowflakes.append(Snowflake())
            spawn_counter = 0
            
        # Update and clean snowflakes
        for flake in snowflakes:
            flake.move()
        snowflakes = [flake for flake in snowflakes if not flake.off_screen()]
        
        # Maintain minimum snow count
        while len(snowflakes) < SNOW_COUNT:
            snowflakes.append(Snowflake())
        
        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
        
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
            
        for flake in snowflakes:
            pygame.draw.circle(screen, WHITE, (flake.x + CELL_SIZE//2, flake.y + CELL_SIZE//2), 2)
            
        pygame.display.update()
        clock.tick(FPS)

def game_over(screen):
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over!', True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == "__main__":
    while True:
        game()