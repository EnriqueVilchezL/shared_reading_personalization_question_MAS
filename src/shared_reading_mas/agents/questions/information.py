import operator
from typing import Annotated, Required

from shared_reading_mas.agents.core.base_information import Information as BaseInformation
from shared_reading_mas.domain.book_aggregate.book import Book
from shared_reading_mas.domain.evaluation_aggregate.evaluation import Evaluation
from shared_reading_mas.utils import add_to_set, preserve_last


class Information(BaseInformation):
    original_book: Required[Annotated[Book, preserve_last]]
    """
    Original book to be shared.
    """

    modified_book: Annotated[Book, preserve_last]
    """
    Book with integrated questions.
    """

    questions_book: Annotated[Book, preserve_last]
    """
    Books with questions created about the original book.
    """

    questions_books: Annotated[set[Book], add_to_set]
    """
    Books with questions created about the original book.
    """

    evaluations: Required[Annotated[list[Evaluation], operator.add]]
    """
    Evaluations of the personalized book.
    """
