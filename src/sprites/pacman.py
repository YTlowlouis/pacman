from pathlib import Path
from src.sprites.base import Sprite


class PacMan(Sprite):
    def __init__(self, lives: int, pos: tuple[int, int], alive: bool,
                 visible: bool, dir: str, can_eat: bool, next_dir: str,
                 respawn_coord: tuple[int, int], super_power: bool,
                 sprite: Path) -> None:
        super().__init__(pos, 0, visible, sprite, lives, alive, dir,
                         can_eat, False, next_dir, respawn_coord, super_power)
        self.points: int = 0
        self.VALID_DIRECTIONS = {"up", "down", "right", "left"}

        if self.lives <= 0:
            self.alive = False

        if self.super_power:
            self.can_eat = True
