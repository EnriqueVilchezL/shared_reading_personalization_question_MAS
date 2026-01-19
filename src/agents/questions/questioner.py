from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from agents.personalization.information import Information
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from roles.core.base_role import Role, RoleCollection


class QuestionerAgent(Agent):
    """
    Agent that creates questions for a story.
    """

    def __init__(
        self,
        name: str,
        roles: list[Role] | RoleCollection | None = None,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name=name, roles=roles, lm_config=lm_config, information_schema=Information
        )

    def pre_core(self, data: dict) -> dict:
        data = super().pre_core(data)
        renderer = BookMarkdownRenderer()

        data["messages"].append(
            HumanMessage(
                "Creame preguntas para el siguiente cuento:\n\n"
                + renderer.render(data.get("original_book", ""))
            )
        )
        return data

    def post_core(self, data: dict) -> dict:
        data = super().post_core(data)

        last_message = data["messages"][-1].content
        print(last_message)
        parser = BookParser()
        book = parser.parse(last_message)
        print(book)

        return data
