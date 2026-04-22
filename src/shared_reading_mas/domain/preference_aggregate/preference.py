from pydantic import BaseModel, Field


class Preference(BaseModel):
    """Represents user configuration for content personalization."""

    type: str = Field(..., description="The category of preference.")
    value: str = Field(
        ..., description="The specific preference detail.", alias="preference"
    )
