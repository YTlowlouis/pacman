from enum import Enum
import pygame
from src.sprites.base import Sprite


class GhostState(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"


class Ghost(Sprite):
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
        self.target_tile = pacman_pos
