import re
from typing import override

from langgraph.graph.state import END

from agents.core.base_lm_config import LMConfiguration
from agents.langfuse_organization import LangFuseOrganization
from agents.personalization.information import Information
from agents.personalization.personalizer import PersonalizerAgent
from agents.personalization.triage_critic import TriageCriticAgent

NO_ACEPTABLE_RE = re.compile(r"\b\s+cambio\b", re.IGNORECASE)


class Organization(LangFuseOrganization):
    """
    Organization focused on shared reading activities.
    """

    def __init__(self, configuration: dict = {}):
        """
        Initializes the personalization organization.

        Args:
            configuration (dict): Configuration for the organization.
        """
        super().__init__(
            name="personalization_organization",
            information_schema=Information,
            configuration=configuration,
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
        agents_config = self.configuration["agents"]
        self.add_agent(
            PersonalizerAgent(
                LMConfiguration.model_validate(agents_config["personalizer"])
            )
        )
        self.add_agent(
            TriageCriticAgent(
                LMConfiguration.model_validate(agents_config["triage_critic"])
            )
        )

        # Base flow
        self._core_graph.add_edge("personalizer", "triage_critic")

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
