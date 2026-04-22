from shared_reading_mas.domain.services.category_renderer import (
    CategoriesMarkdownRenderer,
)
from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import (
    LastMessagePermission,
)
from shared_reading_mas.roles.personalization.criteria import (
    COHERENCE_CRITERIA,
    EMOTION_CRITERIA,
    LINGUISTIC_CRITERIA,
    MORAL_CRITERIA,
    NATURALNESS_CRITERIA,
    STYLE_CRITERIA,
    VALUE_CRITERIA,
    VERISIMILITUDE_CRITERIA,
)


class PairCriticRole(LangFuseRole):
    """
    Role that evaluates pairs personalization response based on a query.
    """

    def __init__(self):
        super().__init__(
            name="personalization_pair_critic",
            permissions=[LastMessagePermission()],
            activities=[],
        )
        criteria_list = [
            COHERENCE_CRITERIA,
            NATURALNESS_CRITERIA,
            STYLE_CRITERIA,
            MORAL_CRITERIA,
            VALUE_CRITERIA,
            EMOTION_CRITERIA,
            LINGUISTIC_CRITERIA,
            VERISIMILITUDE_CRITERIA,
        ]
        criteria_str = ""
        for criteria in criteria_list:
            criteria_str += CategoriesMarkdownRenderer().render(
                criteria, indicators=False
            )

        self.configure(
            {
                "criteria": criteria_str,
            }
        )
