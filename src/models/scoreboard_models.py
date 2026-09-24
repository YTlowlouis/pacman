from pydantic import BaseModel, Field, field_validator


class Score(BaseModel):
    name: str
    score: int = Field(ge=0)

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, name: str) -> str:
        for i in name:
            if not i.isalnum() and i != " ":
                raise ValueError(f"Invalid name: {name}")
        if len(name) > 10:
            raise ValueError(f"Invalid name: {name}, max 10 characters")
        return name
