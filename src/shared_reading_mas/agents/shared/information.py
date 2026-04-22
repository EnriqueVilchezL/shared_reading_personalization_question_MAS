from typing import Required

from shared_reading_mas.agents.core.base_information import (
    Information as BaseInformation,
)
from shared_reading_mas.domain.book_aggregate.image import Image


class Information(BaseInformation):
    image: Required[Image]
    """
    Image to be captioned.
    """

    caption: str
    """
    Caption generated for the image.
    """
