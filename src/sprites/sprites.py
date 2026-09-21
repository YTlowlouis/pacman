from pathlib import Path
from src.sprites.ghost import Ghost, GhostState


class Blinky(Ghost):
    """
    Classe représentant Blinky (fantôme rouge).
    Cible directement Pac-Man en mode CHASE.
    """

    def __init__(self, x: int, y: int, sprite_path: Path, tile_size: int = 32) -> None:
        super().__init__(
            x=x,
            y=y,
            points_given=200,
            visible=True,
            lives=1,
            alive=True,
            eatable=False,
            sprite=sprite_path,
            target=(x, y),
            progress=0.0,
            scatter_target=(17, -2),
            tile_size=tile_size,
        )

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE:
            self.target_tile = pacman_pos
        else:
            super().update_target(pacman_pos, pacman_dir)


class Pinky(Ghost):
    """
    Classe représentant Pinky (fantôme rose).
    Vise 4 cases devant Pac-Man en mode CHASE.
    """

    def __init__(self, x: int, y: int, sprite: Path, tile_size: int = 32) -> None:
        super().__init__(
            x=x,
            y=y,
            points_given=200,
            visible=True,
            lives=1,
            alive=True,
            eatable=False,
            sprite=sprite,
            target=(x, y),
            progress=0.0,
            scatter_target=(1, -2),
            tile_size=tile_size,
        )

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE:
            px, py = pacman_pos
            p_dx, p_dy = pacman_dir
            self.target_tile = (px + p_dx * 4, py + p_dy * 4)
        else:
            super().update_target(pacman_pos, pacman_dir)


class Inky(Ghost):
    """
    Classe représentant Inky (fantôme bleu).
    Utilise la position de Pac-Man et de Blinky pour calculer sa cible.
    """

    def __init__(self, x: int, y: int, sprite: Path, blinky_ref: Ghost | None = None, tile_size: int = 32) -> None:
        super().__init__(
            x=x,
            y=y,
            points_given=200,
            visible=True,
            lives=1,
            alive=True,
            eatable=False,
            sprite=sprite,
            target=(x, y),
            progress=0.0,
            scatter_target=(18, 22),
            tile_size=tile_size,
        )
        self.blinky_ref = blinky_ref

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE and self.blinky_ref:
            px, py = pacman_pos
            p_dx, p_dy = pacman_dir
            pivot_x, pivot_y = px + p_dx * 2, py + p_dy * 2

            bx, by = self.blinky_ref.grid_x, self.blinky_ref.grid_y
            vec_x, vec_y = pivot_x - bx, pivot_y - by

            self.target_tile = (bx + vec_x * 2, by + vec_y * 2)
        else:
            super().update_target(pacman_pos, pacman_dir)


class Clyde(Ghost):
    """
    Classe représentant Clyde (fantôme orange).
    Fuit vers sa zone scatter s'il est trop proche de Pac-Man (< 8 cases).
    """

    def __init__(self, x: int, y: int, sprite: Path, tile_size: int = 32) -> None:
        super().__init__(
            x=x,
            y=y,
            points_given=200,
            visible=True,
            lives=1,
            alive=True,
            eatable=False,
            sprite=sprite,
            target=(x, y),
            progress=0.0,
            scatter_target=(0, 22),
            tile_size=tile_size,
        )

    def update_target(self, pacman_pos: tuple[int, int], pacman_dir: tuple[int, int]) -> None:
        if self.state == GhostState.CHASE:
            px, py = pacman_pos
            dist_sq = (self.grid_x - px) ** 2 + (self.grid_y - py) ** 2

            if dist_sq > 64:
                self.target_tile = pacman_pos
            else:
                self.target_tile = self.scatter_target
        else:
            super().update_target(pacman_pos, pacman_dir)
