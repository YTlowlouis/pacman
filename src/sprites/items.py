from pathlib import Path
from src.sprites.base import GameObject


class PacGum(GameObject):
    def __init__(self, pos: tuple[int, int], points: int,
                 visible: bool, sprite: Path) -> None:
        super().__init__(pos, points, visible, sprite)


class SuperPacGum(GameObject):
    def __init__(self, pos: tuple[int, int], points: int,
                 visible: bool, sprite: Path) -> None:
        super().__init__(pos, points, visible, sprite)
