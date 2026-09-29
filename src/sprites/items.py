from src.sprites.base import GameObject


class PacGum(GameObject):
    """Small dot worth a few points."""

    def __init__(
        self, pos: tuple[int, int], points: int, visible: bool, sprite: str
    ) -> None:
        """Create a pacgum.

        Args:
            pos: Cell coordinates (x, y).
            points: Points given when the object is eaten.
            visible: Whether the object is drawn and can be eaten.
            sprite: Path of the object's image.
        """
        super().__init__(pos, points, visible, sprite)


class SuperPacGum(GameObject):
    """Power pellet placed in a maze corner; it frightens the ghosts."""

    def __init__(
        self, pos: tuple[int, int], points: int, visible: bool, sprite: str
    ) -> None:
        """Create a super pacgum.

        Args:
            pos: Cell coordinates (x, y).
            points: Points given when the object is eaten.
            visible: Whether the object is drawn and can be eaten.
            sprite: Path of the object's image.
        """
        super().__init__(pos, points, visible, sprite)
