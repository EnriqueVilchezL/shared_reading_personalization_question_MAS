from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.services.book_renderer import BookMarkdownRenderer
from domain.services.evaluation_parser import EvaluationParser
from roles.core.base_role import RoleCollection, RoleMode
from roles.personalization.edition_critic import EditionCriticRole


class EditionCriticAgent(Agent):
    """
    Agent that evaluates personalization responses based on user preferences.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="edition_critic",
            roles=[EditionCriticRole()],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        super().pre_core(data)

        query = "Porfavor, asigna una etiqueta a la personalización de este cuento."
        renderer = BookMarkdownRenderer()

        request = HumanMessage(
            query
            + "\n\n**Cuento original**:\n"
            + renderer.render(data.get("original_book", ""))
            + "\n\n**Cuento personalizado**:\n"
            + renderer.render(data.get("modified_book", ""))
        )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)

        last_message = data["messages"][-1].content

        return_dict = {}

        evaluation = EvaluationParser().parse(last_message)
        return_dict = {"evaluations": [evaluation]}

        return return_dict
