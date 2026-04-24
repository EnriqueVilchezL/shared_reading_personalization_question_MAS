from langchain.messages import HumanMessage

from shared_reading_mas.agents.core.base_agent import Agent
from shared_reading_mas.agents.core.base_lm_config import LMConfiguration
from shared_reading_mas.domain.services.book_parser import BookParser
from shared_reading_mas.domain.services.book_renderer import BookMarkdownRenderer
from shared_reading_mas.roles.core.base_role import RoleCollection, RoleMode
from shared_reading_mas.roles.personalization.personalizer import (
    PersonalizerEditorRole,
    PersonalizerRole,
)


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
                [PersonalizerRole(), PersonalizerEditorRole()],
                mode=RoleMode.OR,
            ),
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        renderer = BookMarkdownRenderer()

        if isinstance(self.roles.get_active_role(), PersonalizerEditorRole):
            last_evaluation = data["evaluations"][-1]

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
            # last_message = (
            #     data.get("messages", [])[-1].content if data.get("messages") else ""
            # )
            request = HumanMessage(
                "Hazlo para este cuento: \n"
                + renderer.render(data.get("original_book", ""))
                # +"\n\n**Debes hacer el cuento con actantes y conflicto similares al cuento de referencia**:\n"
                # + last_message
            )

        return {"messages": [request]}

    def post_core(self, data: dict) -> dict:
        super().post_core(data)
        last_message = data.get("messages", [])[-1].content

        print("Personalizer Response:", last_message)
        personalized_book = BookParser().parse(last_message)

        if isinstance(self.roles.get_active_role(), PersonalizerEditorRole):
            return {"modified_book": personalized_book}
        else:
            return {"intermediate_books": [personalized_book]}
