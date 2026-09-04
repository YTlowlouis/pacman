from sprites_base_class import Sprite
from pathlib import Path

class PacMan(Sprite):
    def __init__(self, lives: int,
                 pos: list[int, int],
                 alive: bool,
                 visible: bool,
                 dir: str,
                 next_dir: str,
                 respawn_coord: list[int, int],
                 super_power: bool,
                 sprite: Path
                 ) -> None:
        super.__init__(lives, pos, alive,
                       visible, dir, next_dir,
                       respawn_coord, super_power, sprite)
        self.lives: int = 3
        self.pos = pos
        self.alive: bool = True
        self.dir = dir
        self.next_dir = next_dir
        self.points: int = 0
        self.respawn_coord = self.respawn_coord
        self.super_power: bool = False

        VALID_DIRECTIONS = {"up", "down", "right",
                            "left"}

        if lives == 0:
            alive = False
