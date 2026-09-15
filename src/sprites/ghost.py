from enum import Enum
from pathlib import Path
from src.sprites.base import Sprite


class GhostState(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


class Ghost(Sprite):
    def __init__(self, pos: tuple[int, int], visible: bool,
                 lives: int, alive: bool, eatable: bool, sprite: Path,
                 color: tuple[int, int, int], scatter_target: tuple[int, int],
                 tile_size: int) -> None:
        super().__init__(pos, visible, sprite,
                         lives, alive, "",
                         False, eatable, pos, False)
        self.color = color
        self.scatter_target = scatter_target
        self.tile_size = tile_size
        self.state = GhostState.SCATTER
        self.target_tile = scatter_target

    def update_target(self, pacman_pos: tuple[int, int],
                      pacman_dir: tuple[int, int]) -> None:
        pass
