from enum import Enum
from pathlib import Path
from src.sprites.base import Sprite


class GhostState(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


class Ghost(Sprite):
    def __init__(self, pos: tuple[int, int],
                 lives: int, alive: bool, eatable: bool, sprite: Path,
                 scatter_target: tuple[int, int],
                 tile_size: int) -> None:
        super().__init__(pos, sprite, lives, alive, "",
                         False, eatable, "", False)
        self.scatter_target = scatter_target
        self.tile_size = tile_size
        self.state = GhostState.SCATTER
        self.grid_x = pos[0]
        self.grid_y = pos[1]
        self.target_tile = scatter_target
