from domain.services.category_renderer import CategoriesMarkdownRenderer
from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission
from roles.questions.types import (
    COMPLETION_TYPE,
    DISTANCING_TYPE,
    OPEN_ENDED_TYPE,
    RECALL_TYPE,
    WH_TYPE,
)


class AggregatorRole(LangFuseRole):
    """
    Role that creates aggregates questions for a story.
    """

    def __init__(self):

        super().__init__(
            name="questions_aggregator",
            permissions=[LastMessagePermission()],
            activities=[],
        )

        criteria_list = [
            COMPLETION_TYPE,
            RECALL_TYPE,
            OPEN_ENDED_TYPE,
            WH_TYPE,
            DISTANCING_TYPE,
        ]
        criteria_str = ""
        for criteria in criteria_list:
            criteria_str += CategoriesMarkdownRenderer().render(
                criteria, indicators=False
            )

        self.configure({
            "description": criteria_str,
        })
