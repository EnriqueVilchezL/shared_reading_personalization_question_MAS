from domain.services.criteria_renderer import CriteriaMarkdownRenderer
from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission
from roles.personalization.criteria import (
    COHERENCE_CRITERIA,
    EMOTION_CRITERIA,
    LINGUISTIC_CRITERIA,
    MORAL_CRITERIA,
    NATURALNESS_CRITERIA,
    STYLE_CRITERIA,
    VALUE_CRITERIA,
    VERISIMILITUDE_CRITERIA,
)


class EditionCriticRole(LangFuseRole):
    """
    Role that evaluates the linguistic quality and coherence of a personalization response.
    """

    def __init__(self):
        super().__init__(
            name="personalization_edition_critic",
            permissions=[LastMessagePermission()],
            activities=[],
        )
        criteria_str = ""
        criteria_list = [
            COHERENCE_CRITERIA,
            LINGUISTIC_CRITERIA,
            NATURALNESS_CRITERIA,
            STYLE_CRITERIA,
            MORAL_CRITERIA,
            VALUE_CRITERIA,
            EMOTION_CRITERIA,
            VERISIMILITUDE_CRITERIA,
        ]
        for criteria in criteria_list:
            criteria_str += CriteriaMarkdownRenderer().render(
                criteria, indicators=False
            )

        self.configure(
            {
                "criteria": criteria_str,
            }
        )
