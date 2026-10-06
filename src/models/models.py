from pydantic import BaseModel, Field


class PointsConfig(BaseModel):
    """Points earned for each thing Pac-Man eats."""

    ghost: int
    super_pacgum: int
    pacgum: int


class LevelConfig(BaseModel):
    """Settings of one level: maze size, time limit and seed.

    A seed of 0 generates a random maze.
    """

    id: int
    height: int = Field(ge=3)
    width: int = Field(ge=3)
    max_time: int
    seed: int = 0


class PacManConfig(BaseModel):
    """Pac-Man's start directions."""

    dir: str
    next_dir: str


class Config(BaseModel):
    """Full game configuration, built from the JSON config file."""

    levels: list[LevelConfig]
    points: PointsConfig
    lives: int
    pacman: PacManConfig
