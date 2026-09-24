import pygame

from mazegenerator import MazeGenerator
from src.engine.scenes.scene_baseclass import Scene
from src.sprites.sprites import Inky, Pinky, Clyde, Blinky, Ghost
from src.sprites.pacman import PacMan
from src.sprites.items import PacGum, SuperPacGum
from src.sprites.base import GameObject

""" from src.sprites.ghost import Ghost
from src.sprites.sprites import Blinky, Pinky, Inky, Clyde """


class RunningScene(Scene):
    WALL_COLOR = (33, 33, 222)
    BG_COLOR = (0, 0, 0)
    SCORE_COLOR = (255, 255, 0)
    SCORE_POS = (15, 15)
    HUD_GAP = 25
    HUD_MARGIN = 15
    LIFE_ICON_SIZE = 28
    LIFE_SPACING = 6
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
    GUM_RATIO = 0.5
    SUPER_GUM_RATIO = 1.6
    FADE_DURATION = 0.8
    HIGH_TIMER = 3.0

    KEY_TO_DIR = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
    }

    def __init__(self, engine):
        super().__init__(engine)
        self.cell_size = 0
        self.origin = (0, 0)
        self.layer: pygame.Surface | None = None
        self.font_score = pygame.font.Font("src/assets/sonicfont.ttf", 28)
        self.maze: MazeGenerator

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

        self.img_pacgum = pygame.image.load(
            "src/assets/pacgum.png"
        ).convert_alpha()
        self.img_super_pacgum = pygame.image.load(
            "src/assets/super_pacgum.png"
        ).convert_alpha()
        self.life_icon = pygame.transform.scale(
            self.pacman_sprite_open,
            (self.LIFE_ICON_SIZE, self.LIFE_ICON_SIZE),
        )

        self.images: list[dict[str, pygame.Surface]] = []
        self.sprite_gum: pygame.Surface | None = None
        self.gum_offset = 0

        self.ghosts: list[Ghost] = []
        self.ghost_sprites: dict[Ghost, pygame.Surface] = {}
        self.ghost_images: dict[Ghost, pygame.Surface] = {}

        self.fade_veil = pygame.Surface(self.engine.screen.get_size())
        self.fade_veil.fill(self.BG_COLOR)
        self.fade_alpha = 0.0
        self.fade_target: Scene | None = None

        self.pacman = self._build_pacman()

        self.is_high_timer = 3.0

        self.cheat_mode = False
        self.lives_lost = 1
        self.die_when_touched = True
        self.ghost_move = True

        self.load_level(0)

    def _init_ghost(self) -> None:
        grid = self.maze.maze
        rows, cols = len(grid), len(grid[0])
        max_x, max_y = rows - 1, cols - 1
        blinky = Blinky(max_x, 0, ("src/assets/Blinky.png"))
        pinky = Pinky(0, 0, ("src/assets/Pinky.png"))
        inky = Inky(0, max_y, ("src/assets/Inky.png"), blinky)
        clyde = Clyde(max_x, max_y, ("src/assets/Clyde.png"))
        self.ghosts = [blinky, pinky, inky, clyde]

        for ghost in self.ghosts:
            self.ghost_sprites[ghost] = pygame.image.load(
                ghost.sprite
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

    def _build_pacgums(self) -> list[list[GameObject]]:
        points = self.engine.config.points.pacgum
        points2 = self.engine.config.points.super_pacgum
        pacgums: list[list[GameObject]] = [
            [
                PacGum((x, y), points, cell != 15, "src/assets/pacgum.png")
                for x, cell in enumerate(row)
            ]
            for y, row in enumerate(self.maze.maze)
        ]

        for y in (0, -1):
            for x in (0, -1):
                old = pacgums[y][x]
                pacgums[y][x] = SuperPacGum(
                    old.pos, points2, True, "src/assets/super_pacgum.png"
                )

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

    def _scale_sprites(self) -> None:
        c = self.cell_size
        self.images = []
        for frame in self.pacman_sprites:
            sprite = pygame.transform.scale(frame, (c, c))
            self.images.append(
                {
                    "right": sprite,
                    "left": pygame.transform.flip(sprite, True, False),
                    "up": pygame.transform.rotate(sprite, 90),
                    "down": pygame.transform.rotate(sprite, -90),
                }
            )
        gum_size = max(2, int(c * self.GUM_RATIO))
        self.sprite_gum = pygame.transform.scale(
            self.img_pacgum, (gum_size, gum_size)
        )
        self.gum_offset = (c - gum_size) // 2

        super_gum_size = max(2, int(c * self.SUPER_GUM_RATIO))
        self.sprite_super_gum = pygame.transform.scale(
            self.img_super_pacgum, (super_gum_size, super_gum_size)
        )
        self.super_gum_offset = (c - super_gum_size) // 2

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in self.KEY_TO_DIR:
                self.pacman.next_dir = self.KEY_TO_DIR[event.key]
            if event.key == pygame.K_ESCAPE:
                pause_scene = self.engine.scenes["Pause"]
                pause_scene.background_snapshot = self.engine.screen.copy()
                self.engine.change_scene(pause_scene)
            if event.key == pygame.K_c:
                self.cheat_mode = True
            if event.key == pygame.K_l and self.cheat_mode is True:
                self.lives_lost = 0 if self.lives_lost == 1 else 1
            if event.key == pygame.K_w and self.cheat_mode is True:
                self.load_level(self.level_index + 1)

    def draw(self, surface: pygame.Surface) -> None:
        if self.layer is None:
            self.layer = self._build_layer(surface.get_size())
            self._scale_sprites()

        surface.fill(self.BG_COLOR)
        surface.blit(self.layer, (0, 0))
        self._draw_pacgums(surface)
        self._draw_pacman(surface)
        self._draw_hud(surface)

        if self.fade_alpha > 0:
            self.fade_veil.set_alpha(int(self.fade_alpha))
            surface.blit(self.fade_veil, (0, 0))

    def _draw_pacgums(self, surface: pygame.Surface) -> None:
        ox, oy = self.origin
        c = self.cell_size
        for row in self.pacgums:
            for pacgum in row:
                if pacgum.visible is True:
                    if isinstance(pacgum, SuperPacGum):
                        surface.blit(
                            self.sprite_super_gum,
                            (
                                ox + pacgum.pos[0] * c + self.super_gum_offset,
                                oy + pacgum.pos[1] * c + self.super_gum_offset,
                            ),
                        )
                    else:
                        surface.blit(
                            self.sprite_gum,
                            (
                                ox + pacgum.pos[0] * c + self.gum_offset,
                                oy + pacgum.pos[1] * c + self.gum_offset,
                            ),
                        )

    def _draw_pacman(self, surface: pygame.Surface) -> None:
        px, py = self.pacman.pos
        tx, ty = self.pacman.target
        progress = self.pacman.progress
        ox, oy = self.origin
        c = self.cell_size

        fx = px + (tx - px) * progress
        fy = py + (ty - py) * progress
        sprite = self.images[self.current_pacman_sprite][self.pacman.dir]
        surface.blit(sprite, (round(ox + fx * c), round(oy + fy * c)))

    def _draw_hud(self, surface: pygame.Surface) -> None:
        x, y = self.SCORE_POS
        for text in (
            f"Score: {self.pacman.points}",
            f"Level: {self.level_index + 1}",
            f"Time: {max(0, int(self.time_left))}",
        ):
            rendered = self.font_score.render(text, True, self.SCORE_COLOR)
            surface.blit(rendered, (x, y))
            x += rendered.get_width() + self.HUD_GAP
        self._draw_lives(surface)

    def _draw_lives(self, surface: pygame.Surface) -> None:
        step = self.LIFE_ICON_SIZE + self.LIFE_SPACING
        right = surface.get_width() - self.HUD_MARGIN
        for i in range(max(0, self.pacman.lives)):
            surface.blit(
                self.life_icon,
                (right - (i + 1) * step, self.SCORE_POS[1]),
            )

    def _can_move(self, x: int, y: int, direction: str) -> bool:
        dx, dy, wall_bit = self.DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        rows, cols = len(self.maze.maze), len(self.maze.maze[0])
        if not (0 <= nx < cols and 0 <= ny < rows):
            return False
        return (self.maze.maze[y][x] & wall_bit) == 0

    def update(self, dt: float) -> None:
        if self.fade_target is not None:
            self.fade_alpha += 255.0 * dt / self.FADE_DURATION
            if self.fade_alpha >= 255.0:
                self.fade_alpha = 255.0
                self.engine.change_scene(self.fade_target)
                self.fade_target = None
            return

        self.time_left -= dt

        if self.pacman.super_power:
            self.is_high_timer -= dt
            if self.is_high_timer <= 0.0:
                self.is_high_timer = 0.0
                self.pacman.super_power = False

        if self.time_left <= 0.0:
            self.time_left = 0.0
            self._game_over()
            return

        self.eat_pacgum()

        if self.remaining_gums <= 0:
            self.load_level(self.level_index + 1)

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

    def eat_pacgum(self) -> None:
        x, y = self.pacman.pos
        gum = self.pacgums[y][x]
        if gum.visible:
            if isinstance(gum, SuperPacGum):
                self._start_high()
            gum.visible = False
            self.remaining_gums -= 1
            self.pacman.points += gum.points

    def _start_high(self) -> None:
        self.pacman.super_power = True
        self.is_high_timer = self.HIGH_TIMER

    def load_level(self, index: int) -> None:
        if index >= len(self.engine.config.levels):
            self.fade_target = self.engine.scenes["Win"]
            return
        conf = self.engine.config.levels[index]
        self.level_index = index

        self.maze = MazeGenerator(
            size=(conf.width, conf.height), perfect=False, seed=conf.seed
        )
        self.layer = None
        self.pacgums = self._build_pacgums()
        self.remaining_gums = sum(
            gum.visible for row in self.pacgums for gum in row
        )
        self.time_left = float(conf.max_time)
        self.fade_alpha = 0.0
        self.fade_target = None
        self._reset_pacman()

    def _reset_pacman(self) -> None:
        conf = self.engine.config.pacman
        self.pacman.pos = conf.pos
        self.pacman.target = conf.pos
        self.pacman.progress = 0.0
        self.pacman.dir = conf.dir
        self.pacman.next_dir = conf.next_dir

    def _game_over(self) -> None:
        gameover = self.engine.scenes["GameOver"]
        gameover.enter(self.pacman.points)
        self.fade_target = gameover

    def start_new_game(self) -> None:
        self.pacman.points = 0
        self.pacman.lives = self.engine.config.lives
        self.pacman.alive = True
        self._init_ghost()
        self.load_level(0)

    def draw_ghost(self, surface: pygame.Surface) -> None:
        ox, oy = self.origin
        c = self.cell_size
        for ghost in self.ghosts:
            x, y = ghost.pos
            if ghost in self.ghost_images:
                surface.blit(self.ghost_images[ghost],
                             (ox + x * c, oy + y * c))

    def _scale_ghost_images(self) -> None:
        size = (self.cell_size - 15, self.cell_size - 15)
        for ghost, image in self.ghost_sprites.items():
            self.ghost_images[ghost] = pygame.transform.smoothscale(
                image, size)
