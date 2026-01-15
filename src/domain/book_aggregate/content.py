from enum import Enum

from pydantic import BaseModel, Field


class ContentType(str, Enum):
    TEXT = "text"
    QUESTION = "question"


class Content(BaseModel):
    """Represents a discrete block of text content."""

    type: ContentType = Field(..., description="The semantic type of the content.")
    text: str = Field(..., description="The actual textual body.")
