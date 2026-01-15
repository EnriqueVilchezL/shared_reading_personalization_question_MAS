from pydantic import BaseModel, Field

from domain.book_aggregate.content import Content
from domain.book_aggregate.image import Image


class Page(BaseModel):
    """Represents a single page containing a sequence of content and images."""

    contents: list[Content] = Field(
        default_factory=list, description="Ordered text content blocks."
    )
    images: list[Image] = Field(
        default_factory=list, description="Images associated with this page."
    )
