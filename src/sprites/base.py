from pathlib import Path


class GameObject:
    def __init__(self, pos: tuple[int, int],
                 points: int, visible: bool,
                 sprite: Path) -> None:
        self.pos = pos
        self.points = points
        self.visible = visible
        self.sprite = sprite

    def _switch_texture(self, active: bool) -> None:
        pass

    def disappear(self) -> None:
        if not self.visible:
            self._switch_texture(False)


class Sprite:
    def __init__(self,
                 pos: tuple[int, int],
                 visible: bool,
                 sprite: Path,
                 lives: int,
                 alive: bool,
                 dir: str,
                 can_eat: bool,
                 eatable: bool,
                 respawn_coord: tuple[int, int],
                 super_power: bool) -> None:
        self.pos = pos
        self.visible = visible
        self.sprite = sprite
        self.lives = lives
        self.alive = alive
        self.dir = dir
        self.can_eat = can_eat
        self.eatable = eatable
        self.respawn_coord = respawn_coord
        self.super_power = super_power

    def _switch_texture(self, active: bool) -> None:
        pass

    def disappear(self) -> None:
        if not self.alive:
            self.visible = False
        if not self.visible:
            self._switch_texture(False)
