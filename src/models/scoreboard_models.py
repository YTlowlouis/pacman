from pydantic import BaseModel, Field, field_validator, ValidationError


class Score(BaseModel):
    name: str
    score: int = Field(gt=0)

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, name: str) -> None:
        for i in name:
            if not i.isalnum() and i != " ":
                raise ValidationError(f"Invalid name: {name}")
        if len(name) > 10:
            raise ValidationError(f"Invalid name: {name}, max 10 characters")
