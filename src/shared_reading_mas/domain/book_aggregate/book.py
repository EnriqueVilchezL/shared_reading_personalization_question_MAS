from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from shared_reading_mas.domain.book_aggregate.image import Image
from shared_reading_mas.domain.book_aggregate.page import Page


class Book(BaseModel):
    """The Root Aggregate representing a complete book."""

    title: str = Field(..., description="The title of the book.")
    front_page_image: Optional[Image] = Field(
        default=None, description="Cover artwork."
    )
    pages: list[Page] = Field(
        default_factory=list, description="Ordered collection of pages."
    )
    uid: Optional[UUID] = Field(
        default_factory=uuid4, description="Unique identifier for the book."
    )

    def __eq__(self, value):
        return isinstance(value, Book) and self.uid == value.uid

    def __hash__(self):
        return hash(self.uid)
