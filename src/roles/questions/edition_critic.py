from domain.services.category_renderer import CategoriesMarkdownRenderer
from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission
from roles.questions.criteria import (
    CONTEXT_CRITERIA,
    INTERACTIVITY_CRITERIA,
    LIGUISTIC_CRITERIA,
)
from roles.questions.types import (
    COMPLETION_TYPE,
    DISTANCING_TYPE,
    OPEN_ENDED_TYPE,
    RECALL_TYPE,
    WH_TYPE,
)


class EditionCriticRole(LangFuseRole):
    """
    Role that evaluates the prompts response.
    """

    def __init__(self):
        super().__init__(
            name="questions_edition_critic",
            permissions=[LastMessagePermission()],
            activities=[],
        )
        criteria_str = ""
        criteria_list = [
            CONTEXT_CRITERIA,
            LIGUISTIC_CRITERIA,
            INTERACTIVITY_CRITERIA,
        ]
        for criteria in criteria_list:
            criteria_str += CategoriesMarkdownRenderer().render(
                criteria, indicators=False
            )

        types_str = ""
        types_list = [
            COMPLETION_TYPE,
            RECALL_TYPE,
            WH_TYPE,
            OPEN_ENDED_TYPE,
            DISTANCING_TYPE,
        ]
        for type in types_list:
            types_str += CategoriesMarkdownRenderer().render(
                type, indicators=False
            )

        self.configure(
            {
                "criteria": criteria_str,
                "types": types_str
            }
        )
