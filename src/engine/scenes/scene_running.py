import pygame
from mazegenerator import MazeGenerator
from src.engine.scenes.scene_baseclass import Scene
from src.sprites.ghost import Ghost

from src.sprites.sprites import Blinky, Pinky, Inky, Clyde

"""from src.sprites.pacman import PacMan """


class RunningScene(Scene):
    WALL_COLOR = (33, 33, 222)
    BG_COLOR = (0, 0, 0)
    MARGIN = 20
    THICKNESS = 3
    N, E, S, W = 1, 2, 4, 8

    def __init__(self, engine):
        super().__init__(engine)
        self.maze_size: tuple[int, int] = (15, 15)
        self.maze = MazeGenerator(size=self.maze_size, perfect=False)
        self.cell_size = 0
        self.origin = (0, 0)
        self.layer: pygame.Surface | None = None

        self.ghosts: list[Ghost]
        self._init_ghost()


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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_scene = self.engine.scenes["Pause"]
                pause_scene.background_snapshot = self.engine.screen.copy()
                self.engine.change_scene(pause_scene)

    def draw(self, surface: pygame.Surface) -> None:
        if self.layer is None:
            self.layer = self._build_layer(surface.get_size())
        surface.fill(self.BG_COLOR)
        surface.blit(self.layer, (0, 0))
        self.draw_ghost(surface)

    def draw_ghost(self, surface: pygame.Surface) -> None:
        for ghost in self.ghosts:
            surface.blit(self.pinky_image, (self.origin[0] + self.pinky.pos[0] * self.cell_size, self.origin[1] + self.pinky.pos[1] * self.cell_size))

    def _init_ghost(self) -> None:
        pinky_spawn: tuple[int, int] = (0, 0)
        inky_spawn: tuple[int, int] = (0, self.maze_size[1])
        blinky_spawn: tuple[int, int] = (self.maze_size[0], 0)
        clyde_spawn: tuple[int, int] = (self.maze_size[0], self.maze_size[1])
        self.pinky = Pinky((0, 0), "src/assets/Pinky.png", pinky_spawn, False)
        self.inky = Inky((0, self.maze_size[1]), "src/assets/Inky.png", inky_spawn, False)
        self.blinky = Blinky((self.maze_size[0], 0), "src/assets/Blinky.png", blinky_spawn, False)
        self.clyde = Clyde((self.maze_size[0], self.maze_size[1]), "src/assets/Clyde.png", clyde_spawn, False)
        self.ghosts.append(self.pinky, self.inky, self.blinky, self.clyde)

        self.pinky_image = pygame.image.load(self.pinky.sprite).convert_alpha()
        self.inky_image = pygame.image.load(self.inky.sprite).convert_alpha()
        self.blinky_image = pygame.image.load(self.blinky.sprite).convert_alpha()
        self.clyde_image = pygame.image.load(self.clyde.sprite).convert_alpha()

    def update(self, dt: float) -> None:
        pass
