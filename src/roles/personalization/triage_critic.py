from typing import Callable

from langchain_core.tools.render import render_text_description

from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission
from roles.personalization.coherence_critic import CRITERIA as COHERENCE_CRITERIA
from roles.personalization.emotion_critic import CRITERIA as EMOTION_CRITERIA
from roles.personalization.moral_critic import CRITERIA as MORAL_CRITERIA
from roles.personalization.naturalness_critic import CRITERIA as NATURALNESS_CRITERIA
from roles.personalization.style_critic import CRITERIA as STYLE_CRITERIA
from roles.personalization.value_critic import CRITERIA as VALUE_CRITERIA


class TriageCriticRole(LangFuseRole):
    """
    Role that evaluates general aspects of a personalization response.
    """

    def __init__(self, activities: list[Callable] = None):
        super().__init__(
            name="personalization_triage_critic",
            permissions=[LastMessagePermission()],
            activities=activities,
        )
        criteria = f"""- {COHERENCE_CRITERIA.type} -> {COHERENCE_CRITERIA.description}
- {NATURALNESS_CRITERIA.type} -> {NATURALNESS_CRITERIA.description}
- {STYLE_CRITERIA.type} -> {STYLE_CRITERIA.description}
- {MORAL_CRITERIA.type} -> {MORAL_CRITERIA.description}
- {VALUE_CRITERIA.type} -> {VALUE_CRITERIA.description}
- {EMOTION_CRITERIA.type} -> {EMOTION_CRITERIA.description}
"""
        self.configure({
            "criteria": criteria,
            "critics_tools": render_text_description(activities),
        })
