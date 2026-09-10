from sprites_base_class import Sprite
from pacman import PacMan
from pathlib import Path
from enum import Enum

class GhostState(Enum):
    CHASE = "chase"
    SCATTER = "scatter"
    FRIGHTENED = "frightened"
    EATEN = "eaten"


class Ghost(Sprite):
    def __init__(self, pos: tuple[int, int],
                 points_given: int,
                 visible: bool,
                 lives: int,
                 alive: bool,
                 eatable: bool,
                 sprite: Path):
        super.__init__(pos, points_given,
                       visible, alive,
                       lives, eatable, sprite)

        if PacMan.can_eat is True:
            eatable is True
        if eatable is True:
            print("ghost switch mode color")


#1 Rouge )Poursuite directe
class Blinky(Ghost):
    def __init__(self, x: int, y: int, tile_size: int = 32) -> None:
        super().__init__(
            x=x,
            y=y,
            color=(255, 0, 0),
            scatter_target=(17, -2),
            tile_size=tile_size,
        )

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        if self.state == GhostState.CHASE:
            self.target_tile = pacman_pos
        else:
            super().update_target(pacman_pos, pacman_dir)


# 2. Rose 4 cases devant pacman
class Pinky(Ghost):
    def __init__(self, x: int, y: int, tile_size: int = 32) -> None:
        super().__init__(
            x=x,
            y=y,
            color=(255, 184, 255),
            scatter_target=(1, -2),
            tile_size=tile_size,
        )

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        if self.state == GhostState.CHASE:
            px, py = pacman_pos
            p_dx, p_dy = pacman_dir
            self.target_tile = (px + p_dx * 4, py + p_dy * 4)
        else:
            super().update_target(pacman_pos, pacman_dir)


# 3. pos pacman + Blinky
class Inky(Ghost):
    def __init__(
        self,
        x: int,
        y: int,
        blinky_ref: Ghost | None = None,
        tile_size: int = 32,
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            color=(0, 255, 255),
            scatter_target=(18, 22),
            tile_size=tile_size,
        )
        self.blinky_ref = blinky_ref

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        if self.state == GhostState.CHASE and self.blinky_ref:
            px, py = pacman_pos
            p_dx, p_dy = pacman_dir
            pivot_x, pivot_y = px + p_dx * 2, py + p_dy * 2
            bx, by = self.blinky_ref.grid_x, self.blinky_ref.grid_y
            vec_x, vec_y = pivot_x - bx, pivot_y - by

            self.target_tile = (bx + vec_x * 2, by + vec_y * 2)
        else:
            super().update_target(pacman_pos, pacman_dir)


# 4. orange traque des que 8 cases repart 
class Clyde(Ghost):
    def __init__(self, x: int, y: int, tile_size: int = 32) -> None:
        super().__init__(
            x=x,
            y=y,
            color=(255, 184, 82),
            scatter_target=(0, 22),
            tile_size=tile_size,
        )

    def update_target(
        self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]
    ) -> None:
        if self.state == GhostState.CHASE:
            px, py = pacman_pos
            dist_sq = (self.grid_x - px) ** 2 + (self.grid_y - py) ** 2

            # Si à plus de 8 cases poursuit Pacman
            # Si plus proche que 8 cases, se replie vers son coin
            if dist_sq > 64:
                self.target_tile = pacman_pos
            else:
                self.target_tile = self.scatter_target
        else:
            super().update_target(pacman_pos, pacman_dir)
