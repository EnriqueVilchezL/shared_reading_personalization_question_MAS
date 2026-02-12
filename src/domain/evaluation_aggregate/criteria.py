from typing import Literal, Optional

from pydantic import BaseModel, Field


class Criteria(BaseModel):
    """
    Model to represent a criteria of a personalization response.
    """

    type: str = Field(..., description="The type of the criteria.")
    description: str = Field(..., description="Description of the criteria.")
    indicators: Optional[list[str]] = Field(
        ..., description="Indicators of the criteria."
    )
    importance: Optional[
        Literal["low", "medium", "high", "very high", "extremely high"]
    ] = Field(..., description="Importance level of the criteria.")

    @staticmethod
    def merge_criteria_lists(criteria_lists: list["Criteria"]) -> "Criteria":
        """
        Merges multiple lists of Criteria into a single list, avoiding duplicates based on the criteria type.

        Args:
            *criteria_lists: Multiple lists of Criteria to be merged.

        Returns:
            A single list of Criteria with unique types.
        """
        criteria = Criteria(
            type=" and".join([c.type for c in criteria_lists]),
            description="; ".join([c.description for c in criteria_lists]),
            indicators=[
                indicator for c in criteria_lists for indicator in c.indicators
            ],
            importance=None,
        )
        return criteria
