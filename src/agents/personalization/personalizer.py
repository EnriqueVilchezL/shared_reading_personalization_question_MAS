from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from domain.services.book_parser import BookParser
from domain.services.book_renderer import BookMarkdownRenderer
from roles.core.base_role import RoleCollection, RoleMode
from roles.personalization.personalizer import PersonalizerEditorRole, PersonalizerRole


class PersonalizerAgent(Agent):
    """
    Agent that personalizes responses based on user preferences.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="personalizer",
            roles=RoleCollection(
                [PersonalizerRole(), PersonalizerEditorRole()], RoleMode.OR
            ),
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        renderer = BookMarkdownRenderer()

        if len(data["evaluations"]) > 0:
            last_evaluation = data["evaluations"][-1]
            self.roles.activate(PersonalizerEditorRole)

            request = HumanMessage(
                "Después de hacer una evaluación de la personalización hecha por ti, se solicitaron las siguientes ediciones al cuento personalizado segun mis preferencias: \n"
                + "\n\n**Cuento original**:\n"
                + renderer.render(data.get("original_book", ""))
                + "\n\n**Cuento personalizado**:\n"
                + renderer.render(data.get("modified_book", ""))
                + "\n\n**Ediciones solicitadas**:\n"
                + last_evaluation.changes
            )

        else:
            self.roles.activate(PersonalizerRole)

            request = HumanMessage(
                "Porfavor, personaliza el siguiente libro segun mis preferencias: \n"
                + renderer.render(data.get("original_book", ""))
            )
        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)
        last_message = data.get("messages", [])[-1].content
        personalized_book = BookParser().parse(last_message)

        return {"modified_book": personalized_book}
