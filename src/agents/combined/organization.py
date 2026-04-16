from typing import override

from langgraph.graph import END, START

from agents.combined.combined import CombinedAgent
from agents.core.base_lm_config import LMConfiguration
from agents.langfuse_organization import LangFuseOrganization
from agents.combined.information import Information


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
            name="combined_organization",
            information_schema=Information,
            configuration=configuration,
        )

    @override
    def instantiate(self):
        agents_config = self.configuration["agents"]
        lm_config = LMConfiguration.model_validate(agents_config["combined"])
        combined_agent = CombinedAgent(lm_config=lm_config)

        self.add_agents(
            [
                combined_agent
            ]
        )

        # Entry point
        self._core_graph.add_edge(START, combined_agent.name)
        self._core_graph.set_finish_point(combined_agent.name)

        return self._core_graph.compile()
