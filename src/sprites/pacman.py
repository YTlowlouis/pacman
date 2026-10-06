from pathlib import Path
from src.sprites.base import Sprite


class PacMan(Sprite):
    """The player's character."""

    def __init__(
        self,
        lives: int,
        pos: tuple[int, int],
        alive: bool,
        visible: bool,
        dir: str,
        can_eat: bool,
        next_dir: str,
        respawn_coord: tuple[int, int],
        super_power: bool,
        sprite: Path,
        target: tuple[int, int],
        progress: float,
    ) -> None:
        """Create Pac-Man.

        Args:
            lives: Starting lives.
            pos: Starting cell (x, y).
            alive: Whether Pac-Man is alive.
            visible: Whether Pac-Man is drawn.
            dir: Current direction (up, down, left or right).
            can_eat: Whether Pac-Man can eat ghosts.
            next_dir: Direction requested by the player.
            respawn_coord: Cell where Pac-Man respawns after losing a
                life.
            super_power: Whether a super pacgum effect is active.
            sprite: Path of Pac-Man's image.
            target: Cell Pac-Man is moving to.
            progress: Progress of the move to the target, from 0 to 1.
        """
        super().__init__(
            pos,
            visible,
            str(sprite),
            lives,
            alive,
            dir,
            can_eat,
            False,
            next_dir,
            respawn_coord,
            super_power,
            target,
            progress,
        )
        self.target: tuple[int, int] = target
        self.points: int = 0

        if self.lives <= 0:
            self.alive = False

        if self.super_power:
            self.can_eat = True
