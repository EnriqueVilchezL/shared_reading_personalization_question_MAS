import operator
from typing import Annotated, Required

from agents.core.base_information import Information as BaseInformation
from domain.book_aggregate.book import Book
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
    Book with integrated questions.
    """

    questions_books: Required[Annotated[list[Book], operator.add]]
    """
    Books with questions created about the original book.
    """



