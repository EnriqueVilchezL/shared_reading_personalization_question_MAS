import operator
from typing import Annotated, Required

from agents.core.base_information import Information as BaseInformation
from domain.book_aggregate.book import Book
from utils import preserve_last


class Information(BaseInformation):
    original_book: Annotated[Book, preserve_last]
    """
    Original book to be shared.
    """

    modified_book: Annotated[Book, preserve_last]
    """
    Book with integrated questions.
    """

    questions_books: Required[Annotated[list[Book], operator.add]]
    """
    Books with questions created about the original book.
    """


