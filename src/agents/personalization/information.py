import operator
from typing import Annotated, Required

from agents.core.base_information import Information as BaseInformation
from domain.book_aggregate.book import Book
from domain.evaluation_aggregate.evaluation import Evaluation
from domain.preference_aggregate.preference import Preference


class Information(BaseInformation):
    preferences: list[Preference]
    """
    User reading preferences.
    """

    original_book: Book
    """
    Original book to be shared.
    """

    modified_book: Book
    """
    Personalized version of the book.
    """

    evaluations: Required[Annotated[list[Evaluation], operator.add]]
    """
    Evaluations of the personalized book.
    """
