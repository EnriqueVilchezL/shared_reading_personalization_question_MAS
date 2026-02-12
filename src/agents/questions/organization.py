from typing import override

from langgraph.graph import START

from agents.core.base_lm_config import LMConfiguration
from agents.langfuse_organization import LangFuseOrganization
from agents.questions.aggregator import AggregatorAgent
from agents.questions.completion_questioner import CompletionQuestionerAgent
from agents.questions.distancing_questioner import DistancingQuestionerAgent
from agents.questions.information import Information
from agents.questions.open_ended_questioner import OpenEndedQuestionerAgent
from agents.questions.recall_questioner import RecallQuestionerAgent
from agents.questions.wh_questioner import WhQuestionerAgent


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
            name="questions_organization",
            information_schema=Information,
            configuration=configuration,
        )

    @override
    def instantiate(self):
        agents_config = self.configuration["agents"]
        lm_config = LMConfiguration.model_validate(agents_config["questioner"])
        self.add_agent(
            CompletionQuestionerAgent(
                lm_config=lm_config
            )
        )
        self.add_agent(
            RecallQuestionerAgent(
                lm_config=lm_config
            )
        )
        self.add_agent(
            OpenEndedQuestionerAgent(
                lm_config=lm_config
            )
        )
        self.add_agent(
            WhQuestionerAgent(
                lm_config=lm_config
            )
        )
        self.add_agent(
            DistancingQuestionerAgent(
                lm_config=lm_config
            )
        )
        self.add_agent(
            AggregatorAgent(
                lm_config=lm_config
            )
        )

        # Entry point
        self._core_graph.add_edge(START, "completition_questioner")
        self._core_graph.add_edge(START, "recall_questioner")
        self._core_graph.add_edge(START, "open_ended_questioner")
        self._core_graph.add_edge(START, "wh_questioner")
        self._core_graph.add_edge(START, "distancing_questioner")
        self._core_graph.add_edge("completition_questioner", "aggregator")
        self._core_graph.add_edge("recall_questioner", "aggregator")
        self._core_graph.add_edge("open_ended_questioner", "aggregator")
        self._core_graph.add_edge("wh_questioner", "aggregator")
        self._core_graph.add_edge("distancing_questioner", "aggregator")

        return self._core_graph.compile()
