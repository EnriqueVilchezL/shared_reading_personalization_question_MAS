from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from roles.questions.completion_refiner import CompletionRefinerRole


class CompletionRefinerAgent(Agent):
    """
    Agent that refines completion questions for a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="completion_refiner",
            roles=[CompletionRefinerRole()],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        super().pre_core(data)
        last_message = data["messages"][-1].content
        renderer = BookMarkdownRenderer()
        query = "Porfavor, reformula las siguientes preguntas:"

        request = HumanMessage(
            query
            + "\n\n**Cuento original**:\n"
            + renderer.render(data.get("original_book", {}))
            + "\n\n**Preguntas**:\n"
            + last_message
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)

        last_message = data["messages"][-1].content

        parser = BookParser()
        book = parser.parse(last_message)
        book.title = next(iter(self.roles)).prompt.type

        print(f"Refined book: {book.title}")
        return {"questions_books": [book]}
