class GameObject:
    """Static object placed on a maze cell, such as a pacgum."""

    def __init__(
        self, pos: tuple[int, int], points: int, visible: bool, sprite: str
    ) -> None:
        """Create the object.

        Args:
            pos: Cell coordinates (x, y).
            points: Points given when the object is eaten.
            visible: Whether the object is drawn and can be eaten.
            sprite: Path of the object's image.
        """
        self.pos = pos
        self.points = points
        self.visible = visible
        self.sprite = sprite

    def _switch_texture(self, active: bool) -> None:
        """Hook to change the texture; does nothing by default.

        Args:
            active: Whether the active texture should be shown.
        """
        pass

    def disappear(self) -> None:
        """Switch off the texture if the object is no longer visible."""
        if not self.visible:
            self._switch_texture(False)


class Sprite:
    """Base class of moving characters (Pac-Man and ghosts).

    Movement is tile based: the character goes from ``pos`` to the
    next cell while ``progress`` goes from 0 to 1.
    """

    def __init__(
        self,
        pos: tuple[int, int],
        visible: bool,
        sprite: str,
        lives: int,
        alive: bool,
        dir: str,
        can_eat: bool,
        eatable: bool,
        next_dir: str,
        respawn_coord: tuple[int, int],
        super_power: bool,
        target: tuple[int, int] | None,
        progress: float,
    ) -> None:
        """Create the character.

        Args:
            pos: Current cell (x, y).
            visible: Whether the character is drawn.
            sprite: Path of the character's image.
            lives: Remaining lives.
            alive: Whether the character is alive.
            dir: Current direction (up, down, left, right or empty).
            can_eat: Whether the character can eat others.
            eatable: Whether the character can be eaten.
            next_dir: Direction requested for the next move.
            respawn_coord: Cell where the character respawns.
            super_power: Whether a super pacgum effect is active.
            target: Cell the character is moving to, if any.
            progress: Progress of the move to the target, from 0 to 1.
        """
        self.pos = pos
        self.visible = visible
        self.sprite = sprite
        self.lives = lives
        self.alive = alive
        self.dir = dir
        self.can_eat = can_eat
        self.eatable = eatable
        self.next_dir = next_dir
        self.respawn_coord = respawn_coord
        self.super_power = super_power
        self.target = target
        self.progress = progress

    def _switch_texture(self, active: bool) -> None:
        """Hook to change the texture; does nothing by default.

        Args:
            active: Whether the active texture should be shown.
        """
        pass

    def disappear(self) -> None:
        """Hide the character once it is dead."""
        if not self.alive:
            self.visible = False
        if not self.visible:
            self._switch_texture(False)
