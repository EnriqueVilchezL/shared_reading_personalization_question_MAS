import copy

from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.book_aggregate.content import Content, ContentType
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from roles.questions.aggregator import AggregatorRole


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

        request = HumanMessage(
            "Porfavor, selecciona las preguntas:\n\n"
            + "**Cuento original**:\n"
            + renderer.render(data.get("original_book", ""))
            + "\n\n"
            + "**Preguntas generadas para CROWD**:\n"
            + "\n\n".join(
                [
                    renderer.render(questions_book)
                    for questions_book in data.get("questions_books", [])
                ]
            )
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)

        last_message = data["messages"][-1].content

        parser = BookParser()
        book = parser.parse(last_message)

        print(book)
        original_book = copy.deepcopy(data["original_book"])
        for original_page, output_page in zip(original_book.pages, book.pages):
            original_page.contents.append(
                Content(type=ContentType.QUESTION, text=output_page.contents[0].text)
            )

        print(BookMarkdownRenderer().render(original_book))
        return {"modified_book": original_book}
