from pathlib import Path


class Sprite():
    def __init__(self, pos: tuple[int, int],
                 points_given: int,
                 visible: bool,
                 sprite: Path,
                 lives: int,
                 alive: bool,
                 dir: str,
                 next_dir: str,
                 respawn_coord: list[int, int],
                 super_power: bool,):
        self.pos = pos
        self.points_given = points_given
        self.visible = visible
        self.sprite = sprite
        self.lives = lives
        self.alive = alive
        self.dir = dir
        self.next_dir = next_dir
        self.respawn_coord = respawn_coord
        self.super_power = super_power

    def _switch_texture(self, active: bool):
        print("False")

    def diseappear(self):
        if self.visible is False:
            self._switch_texture(False)
