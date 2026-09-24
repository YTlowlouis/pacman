from enum import Enum
import pygame
from src.sprites.base import Sprite


class GhostState(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


class Ghost(Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        points_given: int,
        visible: bool,
        lives: int,
        alive: bool,
        eatable: bool,
        sprite: str,
        color: tuple[int, int, int],
        scatter_target: tuple[int, int],
        tile_size: int,
        progress: float = 0.0,
        image: pygame.Surface | None = None,
    ) -> None:
        super().__init__(
            pos,
            points_given,
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
            scatter_target,
            progress,
        )
        self.image = image
        self.color = color
        self.scatter_target = scatter_target
        self.tile_size = tile_size
        self.state = GhostState.SCATTER
        self.target_tile = scatter_target
        self.next_tile = pos

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        if self.state == GhostState.EATEN:
            self.target_tile = self.respawn_coord
        else:
            self.target_tile = self.scatter_target
