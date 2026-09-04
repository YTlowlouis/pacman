from pydantic import BaseModel, Field


class LevelConfig(BaseModel):
    id: int = Field(gt=0, lt=20)

    height: int = Field(gt=5, lt=50)
    width: int = Field(gt=5, lt=50)

    max_time: int = Field(gt=30, lt=100)


class PointsConfig(BaseModel):
    ghost: int
    super_pacgum: int
    pacgum: int


class Config(BaseModel):
    levels: list[LevelConfig]
    points: PointsConfig

    lives: int = Field(gt=0, lt=20)
