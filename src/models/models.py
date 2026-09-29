from pathlib import Path
from pydantic import BaseModel, Field


class PointsConfig(BaseModel):
    ghost: int
    super_pacgum: int
    pacgum: int


class LevelConfig(BaseModel):
    id: int
    height: int = Field(ge=3)
    width: int = Field(ge=3)
    max_time: int
    seed: int = 0


class PacManConfig(BaseModel):
    dir: str
    next_dir: str
    sprite: Path


class Config(BaseModel):
    levels: list[LevelConfig]
    points: PointsConfig
    lives: int
    pacman: PacManConfig
