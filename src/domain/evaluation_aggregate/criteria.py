from pydantic import BaseModel, Field


class Criteria(BaseModel):
    """
    Model to represent a criteria of a personalization response.
    """

    type: str = Field(..., description="The type of the criteria.")
    description: str = Field(..., description="Description of the criteria.")
    indicators: list[str] = Field(..., description="Indicators of the criteria.")
