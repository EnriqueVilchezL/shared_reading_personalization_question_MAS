from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from roles.combined.combined import CombinedRole


class CombinedAgent(Agent):
    """
    Agent that is a combination of personalization and questions.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="combined",
            roles=[CombinedRole()],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        renderer = BookMarkdownRenderer()

        request = HumanMessage(
            "Hazlo para este cuento: \n"
            + renderer.render(data.get("original_book", ""))
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)
        last_message = data.get("messages", [])[-1].content
        personalized_book = BookParser().parse(last_message)

        return {"modified_book": personalized_book}
