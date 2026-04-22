from typing import Optional

from pydantic import BaseModel, Field

from shared_reading_mas.domain.evaluation_aggregate.category import Category


class Evaluation(BaseModel):
    """
    Model to represent an evaluation of a personalization response.
    """

    label: str = Field(..., description="The label assigned to the evaluation.")
    changes: Optional[str] = Field(
        None,
        description="Concrete changes recommended for improvement regarding the criteria.",
    )
    criteria: Optional[Category] = Field(
        None, description="The criteria used for the evaluation."
    )
    reasoning: Optional[str] = Field(
        None, description="The reasoning behind the evaluation label."
    )
