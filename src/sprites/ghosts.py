from sprites_base_class import Sprite
from pathlib import Path


class Ghost(Sprite):
    def __init__(self, pos: tuple[int, int],
                 points_given: int,
                 visible: bool,
                 lives: int,
                 alive: bool,
                 sprite: Path):
        super.__init__(pos, points_given,
                       visible, alive,
                       lives, sprite)
