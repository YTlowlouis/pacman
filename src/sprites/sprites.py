import pygame
from src.sprites.ghost import Ghost


class Blinky(Ghost):
    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )


class Pinky(Ghost):
    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        px, py = pacman_pos
        p_dx, p_dy = pacman_dir
        self.target_tile = (px + p_dx * 4, py + p_dy * 4)


class Inky(Ghost):
    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        blinky_ref: Ghost | None = None,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )
        self.blinky_ref = blinky_ref

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        if self.blinky_ref is None:
            super().update_target(pacman_pos, pacman_dir)
            return
        px, py = pacman_pos
        p_dx, p_dy = pacman_dir
        pivot_x, pivot_y = px + p_dx * 2, py + p_dy * 2

        bx, by = self.blinky_ref.pos
        vec_x, vec_y = pivot_x - bx, pivot_y - by

        self.target_tile = (bx + vec_x * 2, by + vec_y * 2)


class Clyde(Ghost):
    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        px, py = pacman_pos
        gx, gy = self.pos
        dist_sq = (gx - px) ** 2 + (gy - py) ** 2

        if dist_sq > 64:
            self.target_tile = pacman_pos
        else:
            self.target_tile = self.respawn_coord
