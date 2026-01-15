from pydantic import BaseModel, Field


class Image(BaseModel):
    """Represents an image resource within the book."""

    data: str = Field(
        ..., description="The image source, typically a URL or base64 string."
    )
    caption: str = Field(
        default="", description="A caption or description for the image."
    )
