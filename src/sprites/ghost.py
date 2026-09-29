from enum import Enum
import pygame
from src.sprites.base import Sprite


class GhostState(Enum):
    """Behaviour mode of a ghost."""

    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"


class Ghost(Sprite):
    """Base class of the four ghosts.

    A ghost starts in its corner, which is also its respawn cell.
    """

    def __init__(
        self,
        pos: tuple[int, int],
        visible: bool,
        lives: int,
        alive: bool,
        eatable: bool,
        sprite: str,
        progress: float = 0.0,
        image: pygame.surface.Surface | None = None,
    ) -> None:
        """Create the ghost.

        Args:
            pos: Starting corner (x, y), also used as respawn cell.
            visible: Whether the ghost is drawn.
            lives: Lives of the ghost.
            alive: Whether the ghost is alive.
            eatable: Whether the ghost can be eaten.
            sprite: Path of the ghost's image.
            progress: Progress of the current move, from 0 to 1.
            image: Loaded image, set later by the running scene.
        """
        super().__init__(
            pos,
            visible,
            sprite,
            lives,
            alive,
            "",
            False,
            eatable,
            "",
            pos,
            False,
            pos,
            progress,
        )
        self.image = image
        self.state = GhostState.SCATTER
        self.target_tile = pos
        self.next_tile = pos
        self.respawn_timer = 0.0

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        """Aim at Pac-Man (default chase target).

        Args:
            pacman_pos: Pac-Man's cell.
            pacman_dir: Pac-Man's direction as a (dx, dy) vector.
        """
        self.target_tile = pacman_pos
