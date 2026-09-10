from enum import Enum
from pathlib import Path
from src.sprites.base import Sprite


class GhostState(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


class Ghost(Sprite):
    def __init__(self, x: int, y: int, points_given: int, visible: bool,
                 lives: int, alive: bool, eatable: bool, sprite: Path,
                 color: tuple[int, int, int], scatter_target: tuple[int, int],
                 tile_size: int) -> None:
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
