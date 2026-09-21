import pygame

from mazegenerator import MazeGenerator
from src.engine.scenes.scene_baseclass import Scene
from src.sprites.pacman import PacMan
from src.sprites.items import PacGum, SuperPacGum

""" from src.sprites.ghost import Ghost
from src.sprites.sprites import Blinky, Pinky, Inky, Clyde """


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
        self.maze = MazeGenerator(size=(15, 15), perfect=False)
        self.cell_size = 0
        self.origin = (0, 0)
        self.layer: pygame.Surface | None = None
        self.pacman = self._build_pacman()
        self.pacman_sprite_open = pygame.image.load(
            "src/assets/open_pacman.png"
        ).convert_alpha()
        self.pacman_sprite_closed = pygame.image.load(
            "src/assets/closed_pacman.png"
        ).convert_alpha()
        self.pacman_sprites = []
        self.pacman_sprites.append(self.pacman_sprite_open)
        self.pacman_sprites.append(self.pacman_sprite_closed)
        self.current_pacman_sprite = 0
        self.pacgums = self._build_pacgums()
        self.img_pacgum = pygame.image.load(
            "src/assets/pacgum.png"
        ).convert_alpha()

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
            target=conf.pos,
            progress=0.0,
        )

    def _build_pacgums(self) -> list[list[PacGum]]:
        pacgums = []
        pacgums_y = []
        for i in range(len(self.maze.maze)):
            for j in range(len(self.maze.maze[0])):
                pacgums_y.append(
                    PacGum((i, j), 15, True, "src/assets/cursor.png")
                )
            pacgums.append(pacgums_y)
            pacgums_y = []
        return pacgums

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
        font_score = pygame.font.Font("src/assets/sonicfont.ttf", 28)
        if self.layer is None:
            self.layer = self._build_layer(surface.get_size())
        surface.fill(self.BG_COLOR)
        surface.blit(self.layer, (0, 0))
        surface_score = font_score.render(f"Score: {self.pacman.points}", True,
                                          (255, 255, 0))
        surface.blit(surface_score, (15, 15))
        self.eat_pacgum()

        px, py = self.pacman.pos
        tx, ty = self.pacman.target
        progress = self.pacman.progress
        ox, oy = self.origin
        c = self.cell_size

        sprite = pygame.transform.scale(
            self.pacman_sprites[self.current_pacman_sprite], (c, c)
        )
        sprite_gum = pygame.transform.scale(self.img_pacgum, (c - 2, c - 2))
        self.images = {
            "right": sprite,
            "left": pygame.transform.flip(sprite, True, False),
            "up": pygame.transform.rotate(sprite, 90),
            "down": pygame.transform.rotate(sprite, -90),
        }
        fx = px + (tx - px) * progress
        fy = py + (ty - py) * progress

        for row in self.pacgums:
            for pacgum in row:
                if pacgum.visible is True:
                    surface.blit(
                        sprite_gum,
                        (ox + pacgum.pos[0] * c, oy + pacgum.pos[1] * c),
                    )
        surface.blit(
            self.images[self.pacman.dir],
            (round(ox + fx * c), round(oy + fy * c)),
        )

    def _can_move(self, x: int, y: int, direction: str) -> bool:
        dx, dy, wall_bit = self.DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        rows, cols = len(self.maze.maze), len(self.maze.maze[0])
        if not (0 <= nx < cols and 0 <= ny < rows):
            return False
        return (self.maze.maze[y][x] & wall_bit) == 0

    def update(self, dt: float) -> None:
        self.eat_pacgum()
        self.pacman.progress += self.MOVES_PER_SECOND * dt
        if self.pacman.progress < 1.0:
            return

        self.pacman.pos = self.pacman.target
        self.pacman.progress -= 1.0
        if self.current_pacman_sprite == 0:
            self.current_pacman_sprite = 1
        else:
            self.current_pacman_sprite = 0
        print(self.pacman.pos)

        x, y = self.pacman.pos
        if self._can_move(x, y, self.pacman.next_dir):
            self.pacman.dir = self.pacman.next_dir
        if self._can_move(x, y, self.pacman.dir):
            dx, dy, _ = self.DIRECTIONS[self.pacman.dir]
            self.pacman.target = (x + dx, y + dy)
        else:
            self.pacman.target = self.pacman.pos
            self.pacman.progress = 0.0

    def eat_pacgum(self):
        for row in self.pacgums:
            for gum in row:
                if self.pacman.pos == gum.pos and gum.visible is True:
                    self.pacman.points += 50
                if self.pacman.pos == gum.pos:
                    gum.visible = False
