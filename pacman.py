import pygame
import math
import random
import sys
import os
import json
import heapq
from typing import List, Tuple, Dict, Optional, Callable, Any, Set
from dataclasses import dataclass
from enum import Enum

# --- CORE INITIALIZATION ---
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
except pygame.error as e:
    print(f"FATAL: Pygame failed to initialize: {e}")
    sys.exit(1)

# =============================================================================
# 1. ENGINE CORE & CONFIGURATION
# =============================================================================

class Settings:
    """Master configuration for the entire game engine."""
    SCREEN_WIDTH = 880
    SCREEN_HEIGHT = 1080
    FPS = 60
    
    # Maze layout and positioning
    CELL_SIZE = 32
    MAZE_OFFSET_X = 48
    MAZE_OFFSET_Y = 120
    
    # Colors
    COLOR_BLACK = (0, 0, 0)
    COLOR_DEEP_BLUE = (0, 0, 30)
    COLOR_MAZE_BLUE = (29, 32, 222)
    COLOR_MAZE_LIGHT_BLUE = (173, 216, 230)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_RED = (255, 0, 0)
    COLOR_PINK = (255, 184, 255)
    COLOR_CYAN = (0, 255, 255)
    COLOR_ORANGE = (255, 165, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_GRAY = (128, 128, 128)
    COLOR_FRIGHTENED_BLUE = (0, 0, 200)
    
    # Game parameters
    PLAYER_SPEED = 160.0
    GHOST_SPEED = 140.0
    GHOST_FRIGHTENED_SPEED = 80.0
    GHOST_EATEN_SPEED = 400.0
    POWER_PELLET_DURATION = 8.0
    PLAYER_INVULNERABILITY_DURATION = 3.0
    
    # File paths
    HIGH_SCORE_FILE = "pacman_highscore.dat"
    
    # Fonts
    FONT_PRIMARY_PATH = None # Use pygame default
    FONT_FANCY_PATH = None   # Use pygame default
    
    @staticmethod
    def get_font(size: int, fancy: bool = False) -> pygame.font.Font:
        try:
            path = Settings.FONT_FANCY_PATH if fancy else Settings.FONT_PRIMARY_PATH
            return pygame.font.Font(path, size)
        except:
            return pygame.font.SysFont("arial", size, bold=fancy)

class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    LEVEL_TRANSITION = 5

class Direction(Enum):
    NONE = (0, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0
    
    def __add__(self, other): return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar): return Vector2(self.x * scalar, self.y * scalar)
    def length(self): return math.sqrt(self.x**2 + self.y**2)
    def distance_to(self, other): return (self - other).length()
    def to_tuple_int(self): return (int(self.x), int(self.y))

# =============================================================================
# 2. UTILITY & MANAGER CLASSES
# =============================================================================

class SoundManager:
    """A robust, fail-safe manager for all game audio."""
    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.enabled = True
        self._load_sounds()

    def _load_sounds(self):
        try:
            self.sounds['intro'] = self._create_phaser_sound(0.5, 440, 880, 4)
            self.sounds['eat_pellet'] = self._create_beep(0.05, 1200, 1000)
            self.sounds['eat_power_pellet'] = self._create_phaser_sound(0.4, 200, 100)
            self.sounds['eat_ghost'] = self._create_phaser_sound(0.3, 200, 1000, 1)
            self.sounds['death'] = self._create_explosion_sound(0.8)
            self.sounds['menu_select'] = self._create_beep(0.1, 800, 2000)
        except Exception as e:
            print(f"Warning: SoundManager failed to initialize: {e}")
            self.enabled = False

    def play(self, sound_name: str, loops: int = 0):
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play(loops)

    @staticmethod
    def _create_beep(duration, freq, volume):
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration)
        buf = [int(volume * math.sin(2 * math.pi * i * freq / sample_rate)) for i in range(num_samples)]
        sound = pygame.sndarray.make_sound(pygame.array.array('h', buf))
        sound.set_volume(0.3)
        return sound

    @staticmethod
    def _create_phaser_sound(duration, start_freq, end_freq, num_phases=4):
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration)
        buf = [0] * num_samples
        for i in range(num_samples):
            progress = i / num_samples
            freq = start_freq + (end_freq - start_freq) * progress
            phase_shift = math.sin(2 * math.pi * num_phases * progress) * 0.5
            angle = 2 * math.pi * (i / sample_rate) * freq + phase_shift
            buf[i] = int(2000 * math.exp(-3 * progress) * math.sin(angle))
        sound = pygame.sndarray.make_sound(pygame.array.array('h', buf))
        sound.set_volume(0.4)
        return sound
        
    @staticmethod
    def _create_explosion_sound(duration):
        sample_rate = pygame.mixer.get_init()[0]
        num_samples = int(sample_rate * duration)
        buf = [0] * num_samples
        for i in range(num_samples):
            progress = i / num_samples
            freq = 800 * (1 - progress**2) + 100
            noise = random.uniform(-1, 1)
            volume = 4000 * math.exp(-5 * progress)
            buf[i] = int(volume * noise * math.sin(2 * math.pi * i * freq / sample_rate))
        sound = pygame.sndarray.make_sound(pygame.array.array('h', buf))
        sound.set_volume(0.5)
        return sound

class InputManager:
    """Handles all user input, providing a clean interface."""
    def __init__(self):
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()

    def update(self, events: List[pygame.event.Event]):
        self.keys_just_pressed.clear()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.keys_just_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed.remove(event.key)

    def is_key_down(self, key: int) -> bool: return key in self.keys_pressed
    def was_key_just_pressed(self, key: int) -> bool: return key in self.keys_just_pressed

class ParticleSystem:
    """Manages all particles for visual effects."""
    def __init__(self):
        self.particles: List[Tuple] = []

    def emit(self, pos: Vector2, color: Tuple, count: int, speed_range: Tuple, lifetime_range: Tuple):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            vel = Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.uniform(*lifetime_range)
            self.particles.append([pos, vel, lifetime, lifetime, color])

    def update(self, dt: float):
        for p in self.particles:
            p[0] += p[1] * dt
            p[1].y += 100 * dt  # Gravity
            p[2] -= dt
        self.particles[:] = [p for p in self.particles if p[2] > 0]

    def draw(self, screen: pygame.Surface):
        for pos, _, lifetime, max_lifetime, color in self.particles:
            alpha = int(255 * (lifetime / max_lifetime))
            size = int(4 * (lifetime / max_lifetime))
            if size > 0:
                pygame.draw.circle(screen, (*color, alpha), pos.to_tuple_int(), size)

# =============================================================================
# 3. GAME OBJECTS & ENTITIES
# =============================================================================

class Maze:
    """Manages the maze layout, rendering, and collision data."""
    LAYOUT = [
        "11111111111111111111111",
        "1P..........1..........P1",
        "1.111.11111.1.11111.111.1",
        "1.111.11111.1.11111.111.1",
        "1.......................1",
        "1.111.1.1111111.1.111.1",
        "1.....1...1...1...1.....1",
        "11111.111.1.111.11111",
        "    1.1   G   1.1    ",
        "11111.1 11111 1.11111",
        "1.......1   1.......1",
        "11111.1 11S11 1.11111",
        "    1.1       1.1    ",
        "11111.1 11111 1.11111",
        "1...........1...........1",
        "1.111.11111.1.11111.111.1",
        "1...P...1...1...1...P...1",
        "111.111.1.11111.1.111.111",
        "1.......1...1...1.......1",
        "1.111111111.1111111111.1",
        "1P.....................P1",
        "11111111111111111111111"
    ]

    def __init__(self, particle_system: ParticleSystem):
        self.particle_system = particle_system
        self.pellets: List['Pellet'] = []
        self.player_start_pos: Optional[Vector2] = None
        self.ghost_start_positions: Dict[str, Vector2] = {}
        self.ghost_house_exit: Optional[Vector2] = None
        self.layout_str = [row for row in self.LAYOUT]
        self._parse_layout()
        self.background_surface = self._pre_render_maze()

    def _parse_layout(self):
        ghost_spawn_index = 0
        for r, row in enumerate(self.layout_str):
            for c, char in enumerate(row):
                pos = Vector2(
                    Settings.MAZE_OFFSET_X + c * Settings.CELL_SIZE + Settings.CELL_SIZE / 2,
                    Settings.MAZE_OFFSET_Y + r * Settings.CELL_SIZE + Settings.CELL_SIZE / 2
                )
                if char == '.': self.pellets.append(Pellet(pos, False))
                elif char == 'P': self.pellets.append(Pellet(pos, True))
                elif char == 'S': self.player_start_pos = pos
                elif char == 'G':
                    ghost_name = ["blinky", "pinky", "inky", "clyde"][ghost_spawn_index % 4]
                    self.ghost_start_positions[ghost_name] = pos
                    ghost_spawn_index += 1

        if not self.player_start_pos: self.player_start_pos = self.grid_to_world((11, 16))
        self.ghost_house_exit = self.grid_to_world((11, 8))

    def _pre_render_maze(self) -> pygame.Surface:
        surface = pygame.Surface((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        for r, row in enumerate(self.layout_str):
            for c, char in enumerate(row):
                if char == '1':
                    rect = pygame.Rect(
                        Settings.MAZE_OFFSET_X + c * Settings.CELL_SIZE,
                        Settings.MAZE_OFFSET_Y + r * Settings.CELL_SIZE,
                        Settings.CELL_SIZE, Settings.CELL_SIZE
                    )
                    pygame.draw.rect(surface, Settings.COLOR_MAZE_BLUE, rect)
                    pygame.draw.rect(surface, Settings.COLOR_MAZE_LIGHT_BLUE, rect, 2)
        return surface
    
    def grid_to_world(self, grid_pos: Tuple[int, int]) -> Vector2:
        return Vector2(
            Settings.MAZE_OFFSET_X + grid_pos[0] * Settings.CELL_SIZE + Settings.CELL_SIZE / 2,
            Settings.MAZE_OFFSET_Y + grid_pos[1] * Settings.CELL_SIZE + Settings.CELL_SIZE / 2
        )

    def world_to_grid(self, world_pos: Vector2) -> Tuple[int, int]:
        c = int((world_pos.x - Settings.MAZE_OFFSET_X) / Settings.CELL_SIZE)
        r = int((world_pos.y - Settings.MAZE_OFFSET_Y) / Settings.CELL_SIZE)
        return c, r

    def is_wall(self, grid_pos: Tuple[int, int]) -> bool:
        r, c = grid_pos[1], grid_pos[0]
        return not (0 <= r < len(self.layout_str) and 0 <= c < len(self.layout_str[0]) and self.layout_str[r][c] != '1')

    def check_pellet_collision(self, player: 'Player') -> Tuple[int, bool]:
        score = 0
        power_pellet_eaten = False
        for pellet in self.pellets:
            if not pellet.eaten and player.position.distance_to(pellet.position) < Settings.CELL_SIZE / 2:
                pellet.eaten = True
                score += pellet.points
                self.particle_system.emit(pellet.position, Settings.COLOR_YELLOW, 5, (20, 80), (0.2, 0.5))
                if pellet.is_power:
                    power_pellet_eaten = True
        return score, power_pellet_eaten

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background_surface, (0, 0))
        for pellet in self.pellets:
            pellet.draw(screen)

class Pellet:
    """Represents a single pellet or power pellet."""
    def __init__(self, pos: Vector2, is_power: bool):
        self.position = pos
        self.is_power = is_power
        self.points = 50 if is_power else 10
        self.eaten = False
        self.animation_timer = random.uniform(0, 2 * math.pi)

    def draw(self, screen: pygame.Surface):
        if self.eaten: return
        
        size = 8 if self.is_power else 3
        if self.is_power:
            self.animation_timer += 0.1
            size = 8 + math.sin(self.animation_timer) * 2
        
        pygame.draw.circle(screen, Settings.COLOR_YELLOW, self.position.to_tuple_int(), int(size))

class Entity:
    """Base class for all moving objects in the game."""
    def __init__(self, pos: Vector2, speed: float, direction: Direction = Direction.NONE):
        self.position = pos
        self.start_pos = pos
        self.velocity = Vector2(0, 0)
        self.direction = direction
        self.speed = speed
    
    def get_grid_pos(self) -> Tuple[int, int]:
        return (
            int((self.position.x - Settings.MAZE_OFFSET_X) / Settings.CELL_SIZE),
            int((self.position.y - Settings.MAZE_OFFSET_Y) / Settings.CELL_SIZE)
        )

    def is_centered(self) -> bool:
        offset_x = (self.position.x - Settings.MAZE_OFFSET_X) % Settings.CELL_SIZE
        offset_y = (self.position.y - Settings.MAZE_OFFSET_Y) % Settings.CELL_SIZE
        return abs(offset_x - Settings.CELL_SIZE / 2) < 3 and abs(offset_y - Settings.CELL_SIZE / 2) < 3

class Player(Entity):
    """The player-controlled Pac-Man entity."""
    def __init__(self, pos: Vector2):
        super().__init__(pos, Settings.PLAYER_SPEED, Direction.LEFT)
        self.next_direction = Direction.LEFT
        self.lives = 3
        self.is_invulnerable = False
        self.invulnerable_timer = 0.0
        self.mouth_angle = 0.0
        self.is_mouth_opening = True

    def update(self, dt: float, input_manager: InputManager, maze: Maze):
        self._handle_input(input_manager)
        self._move(dt, maze)
        self._animate_mouth(dt)
        
        if self.is_invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0: self.is_invulnerable = False

    def _handle_input(self, input_manager: InputManager):
        if input_manager.is_key_down(pygame.K_LEFT) or input_manager.is_key_down(pygame.K_a): self.next_direction = Direction.LEFT
        elif input_manager.is_key_down(pygame.K_RIGHT) or input_manager.is_key_down(pygame.K_d): self.next_direction = Direction.RIGHT
        elif input_manager.is_key_down(pygame.K_UP) or input_manager.is_key_down(pygame.K_w): self.next_direction = Direction.UP
        elif input_manager.is_key_down(pygame.K_DOWN) or input_manager.is_key_down(pygame.K_s): self.next_direction = Direction.DOWN

    def _move(self, dt: float, maze: Maze):
        if self.is_centered():
            c, r = self.get_grid_pos()
            ndx, ndy = self.next_direction.value
            if not maze.is_wall((c + ndx, r + ndy)):
                self.direction = self.next_direction
        
        c, r = self.get_grid_pos()
        dx, dy = self.direction.value
        if maze.is_wall((c + dx, r + dy)) and self.is_centered():
             self.velocity = Vector2(0, 0)
        else:
            self.velocity = Vector2(dx * self.speed, dy * self.speed)
        
        self.position += self.velocity * dt

    def _animate_mouth(self, dt: float):
        if self.velocity.length() > 0:
            rate = 450 * dt
            self.mouth_angle = (self.mouth_angle + rate) % 90
        else:
            self.mouth_angle = 0
            
    def lose_life(self):
        self.lives -= 1
        self.is_invulnerable = True
        self.invulnerable_timer = Settings.PLAYER_INVULNERABILITY_DURATION
        
    def reset(self):
        self.position = self.start_pos
        self.direction = Direction.LEFT
        self.next_direction = Direction.LEFT
        
    def draw(self, screen: pygame.Surface):
        if self.is_invulnerable and int(self.invulnerable_timer * 10) % 2 == 0: return

        angle = math.atan2(self.direction.value[1], self.direction.value[0])
        if self.direction == Direction.NONE: angle = 0
        
        # Calculate mouth points based on angle
        display_angle = math.sin(self.mouth_angle * math.pi / 90) * 45
        p1 = self.position.to_tuple_int()
        p2 = (p1[0] + 14 * math.cos(angle - math.radians(display_angle)), p1[1] + 14 * math.sin(angle - math.radians(display_angle)))
        p3 = (p1[0] + 14 * math.cos(angle + math.radians(display_angle)), p1[1] + 14 * math.sin(angle + math.radians(display_angle)))
        
        pygame.draw.circle(screen, Settings.COLOR_YELLOW, p1, 14)
        if self.mouth_angle > 0:
            pygame.draw.polygon(screen, Settings.COLOR_DEEP_BLUE, [p1, p2, p3])

class Ghost(Entity):
    # TODO: Complete ghost AI
    def __init__(self, pos: Vector2, color: Tuple[int, int, int], name: str):
         super().__init__(pos, Settings.GHOST_SPEED, Direction.UP)
         self.color = color
         self.name = name
         
    def update(self, dt: float, maze: Maze):
        if self.is_centered():
            c, r = self.get_grid_pos()
            possible_dirs = []
            for d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                dx, dy = d.value
                if not maze.is_wall((c+dx, r+dy)):
                    possible_dirs.append(d)
            if self.direction in possible_dirs and len(possible_dirs) > 1:
                # Prevent going back
                rev_dir = Direction(tuple(-x for x in self.direction.value))
                if rev_dir in possible_dirs:
                    possible_dirs.remove(rev_dir)
            
            if possible_dirs:
                self.direction = random.choice(possible_dirs)
        
        dx, dy = self.direction.value
        self.velocity = Vector2(dx * self.speed, dy * self.speed)
        self.position += self.velocity * dt
        
    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.position.to_tuple_int(), 14)
        pygame.draw.rect(screen, self.color, (self.position.x - 14, self.position.y, 28, 14))
        
# =============================================================================
# 4. SCENE MANAGEMENT
# =============================================================================

class Scene:
    """Base class for all game scenes."""
    def __init__(self, game: 'GameEngine'):
        self.game = game
    def handle_events(self): pass
    def update(self, dt: float): pass
    def draw(self, screen: pygame.Surface): pass

class MainMenuScene(Scene):
    """The main menu of the game."""
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Start Game", "Quit"]
        self.selected_option = 0
        self.game.sound_manager.play('intro')
        
    def handle_events(self):
        input = self.game.input_manager
        if input.was_key_just_pressed(pygame.K_DOWN):
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.game.sound_manager.play('menu_select')
        elif input.was_key_just_pressed(pygame.K_UP):
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.game.sound_manager.play('menu_select')
        elif input.was_key_just_pressed(pygame.K_RETURN):
            if self.selected_option == 0: self.game.change_state(GameState.PLAYING)
            elif self.selected_option == 1: self.game.running = False

    def draw(self, screen):
        screen.fill(Settings.COLOR_DEEP_BLUE)
        title_text = Settings.get_font(90, True).render("PAC-MAN", True, Settings.COLOR_YELLOW)
        screen.blit(title_text, title_text.get_rect(center=(Settings.SCREEN_WIDTH/2, 250)))
        
        for i, option in enumerate(self.options):
            color = Settings.COLOR_YELLOW if i == self.selected_option else Settings.COLOR_WHITE
            text = Settings.get_font(50).render(option, True, color)
            rect = text.get_rect(center=(Settings.SCREEN_WIDTH/2, 500 + i * 80))
            screen.blit(text, rect)

class GameScene(Scene):
    """The main gameplay scene."""
    def __init__(self, game):
        super().__init__(game)
        self.particle_system = ParticleSystem()
        self.maze = Maze(self.particle_system)
        self.player = Player(self.maze.player_start_pos)
        self.ghosts = [
            Ghost(pos, Settings.COLOR_RED, name) for name, pos in self.maze.ghost_start_positions.items()
        ]
        self.score = 0
        self.is_power_pellet_active = False
        self.power_pellet_timer = 0.0

    def update(self, dt):
        self.particle_system.update(dt)
        self.player.update(dt, self.game.input_manager, self.maze)
        for ghost in self.ghosts:
            ghost.update(dt, self.maze)

        score_gain, power_pellet_eaten = self.maze.check_pellet_collision(self.player)
        if score_gain > 0:
            self.score += score_gain
            self.game.sound_manager.play('eat_pellet')
        if power_pellet_eaten:
            self.is_power_pellet_active = True
            self.power_pellet_timer = Settings.POWER_PELLET_DURATION
            self.game.sound_manager.play('eat_power_pellet')

        if self.is_power_pellet_active:
            self.power_pellet_timer -= dt
            if self.power_pellet_timer <= 0:
                self.is_power_pellet_active = False

    def draw(self, screen):
        screen.fill(Settings.COLOR_DEEP_BLUE)
        self.maze.draw(screen)
        self.player.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)
        self.particle_system.draw(screen)
        
        score_text = Settings.get_font(40).render(f"Score: {self.score}", True, Settings.COLOR_WHITE)
        screen.blit(score_text, (20, 20))
        lives_text = Settings.get_font(40).render(f"Lives: {self.player.lives}", True, Settings.COLOR_WHITE)
        screen.blit(lives_text, (Settings.SCREEN_WIDTH - 180, 20))


# =============================================================================
# 5. MAIN GAME ENGINE
# =============================================================================

class GameEngine:
    """The main orchestrator of the game."""
    def __init__(self):
        self.screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Ultimate Pac-Man Engine")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.sound_manager = SoundManager()
        self.input_manager = InputManager()
        
        self.scenes: Dict[GameState, Scene] = {}
        self.current_state = GameState.MAIN_MENU
        self._init_scenes()
        self.current_scene = self.scenes[self.current_state]

    def _init_scenes(self):
        self.scenes = {
            GameState.MAIN_MENU: MainMenuScene(self),
            GameState.PLAYING: GameScene(self)
        }

    def change_state(self, new_state: GameState):
        if new_state in self.scenes:
            if new_state == GameState.PLAYING:
                 self.scenes[GameState.PLAYING] = GameScene(self) # Re-init for new game
            self.current_state = new_state
            self.current_scene = self.scenes[new_state]
        else:
            print(f"Warning: Tried to change to unhandled state {new_state.name}")

    def run(self):
        """The main game loop."""
        while self.running:
            dt = self.clock.tick(Settings.FPS) / 1000.0
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.running = False
            
            self.input_manager.update(events)
            self.current_scene.handle_events()
            self.current_scene.update(dt)
            self.current_scene.draw(self.screen)
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    try:
        engine = GameEngine()
        engine.run()
    except Exception as e:
        print("An unexpected error occurred:")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit() 