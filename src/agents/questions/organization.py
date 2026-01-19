from typing import override

from agents.langfuse_organization import LangFuseOrganization
from agents.questions.completition_questioner import CompletitionQuestionerAgent
from agents.questions.information import Information


class Organization(LangFuseOrganization):
    """
    Organization focused on shared reading activities.
    """

    def __init__(self):
        super().__init__(
            name="personalization_organization",
            information_schema=Information,
        )

    @override
    def instantiate(self):
        self.add_agent(CompletitionQuestionerAgent())

        # Entry point
        self._core_graph.set_entry_point("completition_questioner")
        self._core_graph.set_finish_point("completition_questioner")

        return self._core_graph.compile()
