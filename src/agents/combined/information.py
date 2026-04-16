import operator
from typing import Annotated, Required

from agents.core.base_information import Information as BaseInformation
from domain.book_aggregate.book import Book
from domain.evaluation_aggregate.evaluation import Evaluation
from domain.preference_aggregate.preference import Preference
from utils import preserve_last


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
