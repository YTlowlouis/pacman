from pathlib import Path
from pydantic import BaseModel


class PointsConfig(BaseModel):
    ghost: int
    super_pacgum: int
    pacgum: int


class LevelConfig(BaseModel):
    id: int
    height: int
    width: int
    max_time: int


class PacManConfig(BaseModel):
    pos: tuple[int, int]
    dir: str
    next_dir: str
    sprite: Path


class Config(BaseModel):
    levels: list[LevelConfig]
    points: PointsConfig
    lives: int
    pacman: PacManConfig
