from typing import Literal, Optional

from pydantic import BaseModel, Field


class Category(BaseModel):
    """
    Model to represent generalized category.
    """

    type: str = Field(..., description="The type of the category.")
    description: str = Field(..., description="Description of the category.")
    indicators: Optional[list[str]] = Field(
        ..., description="Indicators of the category."
    )
    importance: Optional[
        Literal["low", "medium", "high", "very high", "extremely high"]
    ] = Field(..., description="Importance level of the category.")

    @staticmethod
    def merge_categories_lists(categories_list: list["Category"]) -> "Category":
        """
        Merges multiple lists of Categories into a single list, avoiding duplicates based on the category type.
        Args:
            *criteria_lists: Multiple lists of Categories to be merged.

        Returns:
            A single list of Categories with unique types.
        """
        category = Category(
            type=" and".join([c.type for c in categories_list]),
            description="; ".join([c.description for c in categories_list]),
            indicators=[
                indicator for c in categories_list for indicator in c.indicators
            ],
            importance=None,
        )
        return category
