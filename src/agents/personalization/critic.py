from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from agents.personalization.information import Information
from domain.services.book_renderer import BookMarkdownRenderer
from domain.services.evaluation_parser import EvaluationParser
from roles.core.base_role import Role, RoleCollection
from roles.personalization.critic import ConsultantCriticRole, DeepReviewCriticRole


class CriticAgent(Agent):
    """
    Agent that evaluates responses based on user preferences.
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

        query = ""
        active_role = self.roles.get_active_role()
        if isinstance(active_role, DeepReviewCriticRole):
            query = "Porfavor, asigna una etiqueta a la personalización de este cuento."
        elif isinstance(active_role, ConsultantCriticRole):
            query = data.get("query", "")

        renderer = BookMarkdownRenderer()

        data["messages"].append(
            HumanMessage(
                query
                + "\n\n**Cuento original**:\n"
                + renderer.render(data.get("original_book", ""))
                + "\n\n**Cuento personalizado**:\n"
                + renderer.render(data.get("modified_book", ""))
            )
        )
        return data

    def post_core(self, data: dict) -> dict:
        data = super().post_core(data)

        last_message = data["messages"][-1].content

        return_dict = {}
        active_role = self.roles.get_active_role()

        if isinstance(active_role, DeepReviewCriticRole):
            evaluation = EvaluationParser().parse(last_message)
            evaluation.criteria = next(iter(self.roles)).criteria
            return_dict = {"evaluations": [evaluation]}

        return return_dict
