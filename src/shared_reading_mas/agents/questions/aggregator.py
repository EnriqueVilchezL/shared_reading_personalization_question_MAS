import copy
import random

from langchain.messages import HumanMessage

from shared_reading_mas.agents.core.base_agent import Agent
from shared_reading_mas.agents.core.base_lm_config import LMConfiguration
from shared_reading_mas.domain.book_aggregate.book import Book
from shared_reading_mas.domain.book_aggregate.content import Content, ContentType
from shared_reading_mas.domain.book_aggregate.page import Page
from shared_reading_mas.domain.services.book_parser import BookParser
from shared_reading_mas.domain.services.book_renderer import BookMarkdownRenderer
from shared_reading_mas.roles.questions.aggregator import AggregatorRole


class AggregatorAgent(Agent):
    """
    Agent that aggregates questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="aggregator",
            roles=[AggregatorRole()],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        super().pre_core(data)
        renderer = BookMarkdownRenderer()

        # Aggregate questions from different questioner agents into a single book with all the questions per page.
        aggregated_questions = Book(title="# CROWD Questions per page", pages=[])
        for page_number in range(len(data.get("original_book").pages)):
            content_str = ""

            books = list(data.get("questions_books", []))

            for questions_book in random.sample(books, len(books)):
                content_str += f"**{questions_book.title}**: {questions_book.pages[page_number].contents[0].text}\n"

            aggregated_questions.pages.append(
                Page(
                    contents=[
                        Content(
                            type=ContentType.TEXT,
                            text=content_str,
                        )
                    ]
                )
            )

        request = HumanMessage(
            "Porfavor, selecciona para este cuento:\n\n"
            + "**Cuento original**:\n"
            + renderer.render(data.get("original_book", ""))
            + "\n\n"
            + "**Intervenciones CROWD para cada página**:\n"
            + renderer.render(aggregated_questions)
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)

        last_message = data["messages"][-1].content

        parser = BookParser()
        book = parser.parse(last_message)

        modified_book = copy.deepcopy(data["original_book"])
        for original_page, output_page in zip(modified_book.pages, book.pages):
            original_page.contents.append(
                Content(type=ContentType.QUESTION, text=output_page.contents[0].text)
            )

        return {"questions_book": book, "modified_book": modified_book}
