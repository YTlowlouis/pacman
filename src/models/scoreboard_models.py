from pydantic import BaseModel, Field, field_validator


class Score(BaseModel):
    """One highscore entry: a player name and a non-negative score."""

    name: str
    score: int = Field(ge=0)

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, name: str) -> str:
        """Check that the name only has letters, digits and spaces.

        Args:
            name: Player name to check.

        Returns:
            The unchanged name.

        Raises:
            ValueError: If the name has other characters or is longer
                than 10 characters.
        """
        for i in name:
            if not i.isalnum() and i != " ":
                raise ValueError(f"Invalid name: {name}")
        if len(name) > 10:
            raise ValueError(f"Invalid name: {name}, max 10 characters")
        return name
