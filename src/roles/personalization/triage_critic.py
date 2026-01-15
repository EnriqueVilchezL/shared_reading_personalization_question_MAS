from typing import Callable

from langchain_core.tools.render import render_text_description

from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission


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
        criteria = """- la coherencia
- la naturalidad
- el estilo
- la enseñanza
- el valor narrativo añadido
- el impacto emocional
"""
        self.configure({
            "criteria": criteria,
            "critics_tools": render_text_description(activities),
        })
