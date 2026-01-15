import re
from typing import override

from langgraph.graph.state import END

from agents.langfuse_organization import LangFuseOrganization
from agents.personalization.information import Information
from agents.personalization.personalizer import PersonalizerAgent
from agents.personalization.triage_critic import TriageCriticAgent

NO_ACEPTABLE_RE = re.compile(
    r"\bno\s+aceptable\b",
    re.IGNORECASE
)


class Organization(LangFuseOrganization):
    """
    Organization focused on shared reading activities.
    """

    def __init__(self):
        super().__init__(
            name="personalization_organization",
            information_schema=Information,
        )

    def route_by_evaluation(self, state: Information) -> str:
        evaluations = state.get("evaluations") or []

        if not evaluations:
            # Safe default: end the graph
            return "finish"

        label = evaluations[0].label or ""

        if NO_ACEPTABLE_RE.search(label):
            return "retry"

        return "finish"

    @override
    def instantiate(self):
        self.add_agent(PersonalizerAgent())
        self.add_agent(TriageCriticAgent())

        # Base flow
        self._core_graph.add_edge(
            "personalizer",
            "triage_critic",
        )

        # Conditional routing AFTER evaluation
        self._core_graph.add_conditional_edges(
            "triage_critic",
            self.route_by_evaluation,
            {
                "retry": "personalizer",
                "finish": END,
            },
        )

        # Entry point
        self._core_graph.set_entry_point("personalizer")

        return self._core_graph.compile()
