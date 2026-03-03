from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.services.book_renderer import BookMarkdownRenderer
from roles.questions.extractor import ExtractorRole


class ExtractorAgent(Agent):
    """
    Agent that extracts aspects of a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="extractor",
            roles=[ExtractorRole()],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        renderer = BookMarkdownRenderer(include_num_pages=True)

        request = HumanMessage(
            "Hazlo para esta historia: \n"
            + renderer.render(data.get("original_book", ""))
        )

        return {"messages": [request]}

