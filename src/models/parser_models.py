from pydantic import BaseModel, Field, model_validator, ValidationError


class LevelConfig(BaseModel):
    id: int = Field(gt=0, lt=20)

    height: int = Field(gt=5, lt=50)
    width: int = Field(gt=5, lt=50)

    max_time: int = Field(gt=30, lt=100)


class PointsConfig(BaseModel):
    ghost: int = Field(gt=0)
    super_pacgum: int = Field(gt=0)
    pacgum: int = Field(gt=0)


class Config(BaseModel):
    levels: list[LevelConfig]
    points: PointsConfig

    lives: int = Field(gt=0, lt=20)

    @model_validator(mode="after")
    def validate_levels(self):
        id_list = []
        for level in self.levels:
            id = level.get("id")
            if id in id_list:
                raise ValidationError("Two levels with same id")
            id_list.append(id)
