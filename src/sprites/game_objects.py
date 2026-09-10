from enum import Enum
from pathlib import Path

class GameObject:
    def __init__(self, pos: tuple[int, int], points: int, visible: bool, sprite: Path) -> None:
        self.pos = pos
        self.points = points
        self.visible = visible
        self.sprite = sprite

    def _switch_texture(self, active: bool) -> None:
        pass

    def disappear(self) -> None:
        if not self.visible:
            self._switch_texture(False)

class PacGum(GameObject):
    def __init__(self, pos: tuple[int, int], points: int, visible: bool, sprite: Path) -> None:
        super().__init__(pos, points, visible, sprite)

class SuperPacGum(GameObject):
    def __init__(self, pos: tuple[int, int], points: int, visible: bool, sprite: Path) -> None:
        super().__init__(pos, points, visible, sprite)

class Sprite:
    def __init__(self, pos: tuple[int, int], points_given: int, visible: bool,
                 sprite: Path, lives: int, alive: bool, dir: str, can_eat: bool,
                 eatable: bool, next_dir: str, respawn_coord: tuple[int, int],
                 super_power: bool) -> None:
        self.pos = pos
        self.points_given = points_given
        self.visible = visible
        self.sprite = sprite
        self.lives = lives
        self.alive = alive
        self.dir = dir
        self.can_eat = can_eat
        self.eatable = eatable
        self.next_dir = next_dir
        self.respawn_coord = respawn_coord
        self.super_power = super_power

    def _switch_texture(self, active: bool) -> None:
        pass

    def disappear(self) -> None:
        if not self.alive:
            self.visible = False
        if not self.visible:
            self._switch_texture(False)

class PacMan(Sprite):
    def __init__(self, lives: int, pos: tuple[int, int], alive: bool,
                 visible: bool, dir: str, can_eat: bool, next_dir: str,
                 respawn_coord: tuple[int, int], super_power: bool, sprite: Path) -> None:
        super().__init__(pos, 0, visible, sprite, lives, alive, dir,
                         can_eat, False, next_dir, respawn_coord, super_power)
        self.points: int = 0
        self.VALID_DIRECTIONS = {"up", "down", "right", "left"}

        if self.lives <= 0:
            self.alive = False

        if self.super_power:
            self.can_eat = True

class GhostState(Enum):
    CHASE = "chase"
    SCATTER = "scatter"

class Ghost(Sprite):
    def __init__(self, x: int, y: int, points_given: int, visible: bool,
                 lives: int, alive: bool, eatable: bool, sprite: Path, color: tuple[int, int, int],
                 scatter_target: tuple[int, int], tile_size: int) -> None:
        super().__init__((x, y), points_given, visible, sprite, lives, alive, "",
                         False, eatable, "", (x, y), False)
        self.color = color
        self.scatter_target = scatter_target
        self.tile_size = tile_size
        self.state = GhostState.SCATTER
        self.grid_x = x
        self.grid_y = y
        self.target_tile = scatter_target

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        pass

class Blinky(Ghost):
    def __init__(self, x: int, y: int, sprite: Path, tile_size: int = 32) -> None:
        super().__init__(x, y, 200, True, 1, True, False, sprite, (255, 0, 0), (17, -2), tile_size)

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE:
            self.target_tile = pacman_pos
        else:
            super().update_target(pacman_pos, pacman_dir)

class Pinky(Ghost):
    def __init__(self, x: int, y: int, sprite: Path, tile_size: int = 32) -> None:
        super().__init__(x, y, 200, True, 1, True, False, sprite, (255, 184, 255), (1, -2), tile_size)

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE:
            px, py = pacman_pos
            p_dx, p_dy = pacman_dir
            self.target_tile = (px + p_dx * 4, py + p_dy * 4)
        else:
            super().update_target(pacman_pos, pacman_dir)

class Inky(Ghost):
    def __init__(self, x: int, y: int, sprite: Path, blinky_ref: Ghost | None = None, tile_size: int = 32) -> None:
        super().__init__(x, y, 200, True, 1, True, False, sprite, (0, 255, 255), (18, 22), tile_size)
        self.blinky_ref = blinky_ref

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE and self.blinky_ref:
            px, py = pacman_pos
            p_dx, p_dy = pacman_dir
            pivot_x, pivot_y = px + p_dx * 2, py + p_dy * 2

            bx, by = self.blinky_ref.grid_x, self.blinky_ref.grid_y
            vec_x, vec_y = pivot_x - bx, pivot_y - by

            self.target_tile = (bx + vec_x * 2, by + vec_y * 2)
        else:
            super().update_target(pacman_pos, pacman_dir)

class Clyde(Ghost):
    def __init__(self, x: int, y: int, sprite: Path, tile_size: int = 32) -> None:
        super().__init__(x, y, 200, True, 1, True, False, sprite, (255, 184, 82), (0, 22), tile_size)

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE:
            px, py = pacman_pos
            dist_sq = (self.grid_x - px) ** 2 + (self.grid_y - py) ** 2

            if dist_sq > 64:
                self.target_tile = pacman_pos
            else:
                self.target_tile = self.scatter_target
        else:
            super().update_target(pacman_pos, pacman_dir)
