from pathlib import Path

class GameObject():
    def __init__(pos: tuple[int, int], points: int, visible: bool, sprite: Path):
        self.pos = pos
        self.points = points
        self.visible = visible
        self.sprite = sprite

    def _switch_texture(self, active: bool):
        print("False")

    def diseappear(self):
        if self.visible == False:
            self._switch_texture(False)

class PacGum(GameObject):
    def __init__(self, pos: tuple[int, int], points: int, visible: bool, sprite: Path):
		super.-__init__(pos, points, visible, sprite)


class SuperPacGum(GameObject):
    def __init__(self, pos: tuple[int, int], points: int, visible: bool, sprite: Path):
		super.-__init__(pos, points, visible, sprite)
