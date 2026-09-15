from pathlib import Path
import pygame

from mazegenerator import MazeGenerator

from src.engine.scenes.scene_baseclass import Scene
from src.sprites.ghost import Ghost
from src.sprites.sprites import Blinky, Pinky, Inky, Clyde
from src.sprites.pacman import PacMan


class RunningScene(Scene):
<<<<<<< HEAD
    WALL_COLOR = (33, 33, 222)
    BG_COLOR = (0, 0, 0)
    MARGIN = 20
    THICKNESS = 3
    N, E, S, W = 1, 2, 4, 8

    def __init__(self, engine):
        super().__init__(engine)
        self.maze = MazeGenerator(size=(15, 15), perfect=False)
        self.cell_size = 0
        self.origin = (0, 0)
        self.layer: pygame.Surface | None = None

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

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self._generate_new_maze()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.engine.change_scene(self.engine.scenes["Pause"])
            elif event.key == pygame.KMOD_CTRL:
                pass

"""
    def __init__(self, engine) -> None:
        super().__init__(engine)

        pacman_conf = self.engine.config.pacman
        lives = self.engine.config.lives

        self.pacman = PacMan(
            lives=lives,
            pos=pacman_conf.pos,
            alive=True,
            visible=True,
            dir=pacman_conf.dir,
            can_eat=False,
            next_dir=pacman_conf.next_dir,
            respawn_coord=pacman_conf.pos,
            super_power=False,
            sprite=pacman_conf.sprite,
        )

        sprite_path = Path("src/assets/ghost.png")
        raw_image = pygame.image.load(str(sprite_path)).convert_alpha()
        self.ghost_texture = pygame.transform.scale(raw_image, (32, 32))

        self.blinky = Blinky(5, 5, sprite_path)
        self.pinky = Pinky(6, 5, sprite_path)
        self.inky = Inky(7, 5, sprite_path, blinky_ref=self.blinky)
        self.clyde = Clyde(8, 5, sprite_path)

        self.ghosts: list[Ghost] = [self.blinky, self.pinky, self.inky, self.clyde]

    def update(self, dt: float) -> None:
        self.engine.wave_manager.update(dt, self.ghosts)

        pacman_pos = self.pacman.pos
        
        dir_vectors = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        pacman_dir = dir_vectors.get(self.pacman.dir, (0, 0))

        for ghost in self.ghosts:
            ghost.update_target(pacman_pos, pacman_dir)

    def draw(self, surface: pygame.Surface) -> None:
<<<<<<< HEAD
        if self.layer is None:
            self.layer = self._build_layer(surface.get_size())
        surface.fill(self.BG_COLOR)
        surface.blit(self.layer, (0, 0))
=======
        surface.fill((0, 0, 0))

        for ghost in self.ghosts:
            screen_x = ghost.grid_x * ghost.tile_size
            screen_y = ghost.grid_y * ghost.tile_size
            surface.blit(self.ghost_texture, (screen_x, screen_y))
>>>>>>> cea1237d39beb069e1b0da799f99925d60939baf

"""