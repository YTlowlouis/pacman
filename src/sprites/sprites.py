import pygame
from src.sprites.ghost import Ghost


class Blinky(Ghost):
    """Red ghost: chases Pac-Man directly."""

    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        """Create Blinky.

        Args:
            pos: Starting corner (x, y), also used as respawn cell.
            sprite: Path of the ghost's image.
            progress: Progress of the current move, from 0 to 1.
            image: Loaded image, set later by the running scene.
        """
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )


class Pinky(Ghost):
    """Pink ghost: ambushes by aiming 4 cells ahead of Pac-Man."""

    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        """Create Pinky.

        Args:
            pos: Starting corner (x, y), also used as respawn cell.
            sprite: Path of the ghost's image.
            progress: Progress of the current move, from 0 to 1.
            image: Loaded image, set later by the running scene.
        """
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        """Aim 4 cells ahead of Pac-Man.

        Args:
            pacman_pos: Pac-Man's cell.
            pacman_dir: Pac-Man's direction as a (dx, dy) vector.
        """
        px, py = pacman_pos
        p_dx, p_dy = pacman_dir
        self.target_tile = (px + p_dx * 4, py + p_dy * 4)


class Inky(Ghost):
    """Cyan ghost: its target depends on both Pac-Man and Blinky."""

    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        blinky_ref: Ghost | None = None,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        """Create Inky.

        Args:
            pos: Starting corner (x, y), also used as respawn cell.
            sprite: Path of the ghost's image.
            blinky_ref: Blinky, used to compute the target.
            progress: Progress of the current move, from 0 to 1.
            image: Loaded image, set later by the running scene.
        """
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )
        self.blinky_ref = blinky_ref

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        """Aim at Blinky's position mirrored around a point near Pac-Man.

        The point is 2 cells ahead of Pac-Man. Without a Blinky
        reference, Inky chases Pac-Man directly.

        Args:
            pacman_pos: Pac-Man's cell.
            pacman_dir: Pac-Man's direction as a (dx, dy) vector.
        """
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
    """Orange ghost: chases Pac-Man from afar, retreats when close."""

    def __init__(
        self,
        pos: tuple[int, int],
        sprite: str,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        """Create Clyde.

        Args:
            pos: Starting corner (x, y), also used as respawn cell.
            sprite: Path of the ghost's image.
            progress: Progress of the current move, from 0 to 1.
            image: Loaded image, set later by the running scene.
        """
        super().__init__(
            pos, True, 1, True, False, sprite, progress, image
        )

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        """Chase Pac-Man from afar, retreat to its corner within 8 cells.

        Args:
            pacman_pos: Pac-Man's cell.
            pacman_dir: Pac-Man's direction as a (dx, dy) vector.
        """
        px, py = pacman_pos
        gx, gy = self.pos
        dist_sq = (gx - px) ** 2 + (gy - py) ** 2

        if dist_sq > 64:
            self.target_tile = pacman_pos
        else:
            self.target_tile = self.respawn_coord
