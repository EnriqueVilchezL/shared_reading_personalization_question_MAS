import operator
from typing import Annotated, Required

from shared_reading_mas.agents.core.base_information import Information as BaseInformation
from shared_reading_mas.domain.book_aggregate.book import Book
from shared_reading_mas.domain.evaluation_aggregate.evaluation import Evaluation
from shared_reading_mas.domain.preference_aggregate.preference import Preference
from shared_reading_mas.utils import preserve_last


class Information(BaseInformation):
    preferences: Annotated[list[Preference], preserve_last]
    """
    User reading preferences.
    """

    original_book: Annotated[Book, preserve_last]
    """
    Original book to be shared.
    """

    modified_book: Annotated[Book, preserve_last]
    """
    Personalized version of the book.
    """
