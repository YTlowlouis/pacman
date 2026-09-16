from pathlib import Path
import pygame
from mazegenerator import MazeGenerator
from src.engine.scenes.scene_baseclass import Scene
from src.sprites.ghost import Ghost
from src.sprites.pacman import PacMan
from src.sprites.sprites import Blinky, Pinky, Inky, Clyde


class RunningScene(Scene):
    WALL_COLOR = (33, 33, 222)
    BG_COLOR = (0, 0, 0)
    MARGIN = 20
    THICKNESS = 3
    N, E, S, W = 1, 2, 4, 8
    DIRECTIONS = {
        "up": (0, -1, N),
        "down": (0, 1, S),
        "left": (-1, 0, W),
        "right": (1, 0, E),
    }
    MOVES_PER_SECOND = 6.0

    def __init__(self, engine):
        super().__init__(engine)
        self.maze_size: tuple[int, int] = (15, 15)
        self.maze = MazeGenerator(size=self.maze_size, perfect=False)
        self.cell_size = 0
        self.origin = (0, 0)
        self.layer: pygame.Surface | None = None
        self.move_timer = 0.0
        self.pacman = self._build_pacman()
        self.pacman_sprite = pygame.image.load(
            self.pacman.sprite
        ).convert_alpha()

        self.ghosts: list[Ghost] = []
        self.ghost_sprites: dict[Ghost, pygame.Surface] = {}
        self.ghost_images: dict[Ghost, pygame.Surface] = {}
        self._init_ghost()

    def _build_pacman(self) -> PacMan:
        conf = self.engine.config.pacman
        return PacMan(
            lives=self.engine.config.lives,
            pos=conf.pos,
            alive=True,
            visible=True,
            dir=conf.dir,
            can_eat=False,
            next_dir=conf.next_dir,
            respawn_coord=conf.pos,
            super_power=False,
            sprite=conf.sprite,
        )

    def _build_layer(self, size: tuple[int, int]) -> pygame.Surface:
        grid = self.maze.maze
        rows, cols = len(grid), len(grid[0])
        w, h = size

        self.cell_size = min(
            (w - 2 * self.MARGIN) // cols, (h - 2 * self.MARGIN) // rows
        )
        ox = (w - self.cell_size * cols) // 2
        oy = (h - self.cell_size * rows) // 2
        self.origin = (ox, oy)

        c = self.cell_size
        layer = pygame.Surface(size, pygame.SRCALPHA)
        for y in range(rows):
            for x in range(cols):
                cell = grid[y][x]
                left, top = ox + x * c, oy + y * c
                right, bottom = left + c, top + c

                if cell == 15:
                    pygame.draw.rect(layer, self.WALL_COLOR, (left, top, c, c))
                    continue
                if cell & self.N:
                    pygame.draw.line(
                        layer,
                        self.WALL_COLOR,
                        (left, top),
                        (right, top),
                        self.THICKNESS,
                    )
                if cell & self.S:
                    pygame.draw.line(
                        layer,
                        self.WALL_COLOR,
                        (left, bottom),
                        (right, bottom),
                        self.THICKNESS,
                    )
                if cell & self.E:
                    pygame.draw.line(
                        layer,
                        self.WALL_COLOR,
                        (right, top),
                        (right, bottom),
                        self.THICKNESS,
                    )
                if cell & self.W:
                    pygame.draw.line(
                        layer,
                        self.WALL_COLOR,
                        (left, top),
                        (left, bottom),
                        self.THICKNESS,
                    )
        return layer

    def _generate_new_maze(self) -> None:
        self.maze.generate()
        self.layer = None

    KEY_TO_DIR = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
    }

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self._generate_new_maze()
            if event.key in self.KEY_TO_DIR:
                self.pacman.next_dir = self.KEY_TO_DIR[event.key]
            if event.key == pygame.K_ESCAPE:
                pause_scene = self.engine.scenes["Pause"]
                pause_scene.background_snapshot = self.engine.screen.copy()
                self.engine.change_scene(pause_scene)

    def draw(self, surface: pygame.Surface) -> None:
        if self.layer is None:
            self.layer = self._build_layer(surface.get_size())
            self._scale_ghost_images()
        surface.fill(self.BG_COLOR)
        surface.blit(self.layer, (0, 0))
        self.draw_ghost(surface)
        self.draw_pacman(surface)

    def draw_pacman(self, surface: pygame.Surface) -> None:
        px, py = self.pacman.pos
        ox, oy = self.origin
        c = self.cell_size
        sprite = pygame.transform.scale(self.pacman_sprite, (c, c))
        surface.blit(sprite, (ox + px * c, oy + py * c))

    def draw_ghost(self, surface: pygame.Surface) -> None:
        ox, oy = self.origin
        c = self.cell_size
        for ghost in self.ghosts:
            x, y = ghost.pos
            surface.blit(self.ghost_images[ghost], (ox + x * c, oy + y * c))

    def _init_ghost(self) -> None:
        max_x, max_y = self.maze_size[0] - 1, self.maze_size[1] - 1
        blinky = Blinky((max_x, 0), Path("src/assets/Blinky.png"))
        pinky = Pinky((0, 0), Path("src/assets/Pinky.png"))
        inky = Inky((0, max_y), Path("src/assets/Inky.png"), blinky)
        clyde = Clyde((max_x, max_y), Path("src/assets/Clyde.png"))
        self.ghosts = [blinky, pinky, inky, clyde]

        for ghost in self.ghosts:
            self.ghost_sprites[ghost] = pygame.image.load(
                ghost.sprite
            ).convert_alpha()

    def _scale_ghost_images(self) -> None:
        size = (self.cell_size - 15, self.cell_size - 15)
        for ghost, image in self.ghost_sprites.items():
            self.ghost_images[ghost] = pygame.transform.smoothscale(
                image, size
            )

    def _can_move(self, x: int, y: int, direction: str) -> bool:
        dx, dy, wall_bit = self.DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        rows, cols = len(self.maze.maze), len(self.maze.maze[0])
        if not (0 <= nx < cols and 0 <= ny < rows):
            return False
        return (self.maze.maze[y][x] & wall_bit) == 0

    def update(self, dt: float) -> None:
        self.move_timer += dt
        move_interval = 1.0 / self.MOVES_PER_SECOND
        while self.move_timer >= move_interval:
            self.move_timer -= move_interval
            x, y = self.pacman.pos
            if self._can_move(x, y, self.pacman.next_dir):
                self.pacman.dir = self.pacman.next_dir
            if self._can_move(x, y, self.pacman.dir):
                dx, dy, _ = self.DIRECTIONS[self.pacman.dir]
                self.pacman.pos = (x + dx, y + dy)
