from typing import override

from langgraph.graph import END, START

from agents.core.base_lm_config import LMConfiguration
from agents.langfuse_organization import LangFuseOrganization
from agents.questions.aggregator import AggregatorAgent
from agents.questions.completion_refiner import CompletionRefinerAgent
from agents.questions.extractor import ExtractorAgent
from agents.questions.information import Information
from agents.questions.questioner import (
    CompletionQuestionerAgent,
    DistancingQuestionerAgent,
    OpenEndedQuestionerAgent,
    RecallQuestionerAgent,
    WhQuestionerAgent,
)


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

    def collect_books(self, state: dict):
        return {"original_book": state.get("original_book")}

    def route_edition(self, state: dict) -> str:
        """Routes to the questions editor after evaluations."""

        last_evaluation = state.get("evaluations", [])[-1]
        if not (
            "cumple parcialmente" in last_evaluation.label.lower()
            or "no cumple" in last_evaluation.label.lower()
        ):
            return END

        else:
            return "questioner_editor"

    @override
    def instantiate(self):
        agents_config = self.configuration["agents"]
        lm_config = LMConfiguration.model_validate(agents_config["questioner"])
        completion_agent = CompletionQuestionerAgent(lm_config=lm_config)

        completion_refiner_agent = CompletionRefinerAgent(lm_config=lm_config)

        recall_agent = RecallQuestionerAgent(lm_config=lm_config)

        open_ended_agent = OpenEndedQuestionerAgent(lm_config=lm_config)

        wh_agent = WhQuestionerAgent(lm_config=lm_config)

        distancing_agent = DistancingQuestionerAgent(lm_config=lm_config)

        aggregator_agent = AggregatorAgent(
            lm_config=LMConfiguration.model_validate(agents_config["aggregator"])
        )

        extractor_agent = ExtractorAgent(
            lm_config=LMConfiguration.model_validate(agents_config["extractor"])
        )

        self.add_agents(
            [
                completion_agent,
                recall_agent,
                open_ended_agent,
                wh_agent,
                distancing_agent,
                aggregator_agent,
                completion_refiner_agent,
                extractor_agent,
            ]
        )

        self._core_graph.add_node("collector", self.collect_books)

        # Entry point
        self._core_graph.add_edge(START, extractor_agent.name)
        self._core_graph.add_edge(extractor_agent.name, completion_agent.name)
        self._core_graph.add_edge(extractor_agent.name, recall_agent.name)
        self._core_graph.add_edge(extractor_agent.name, open_ended_agent.name)
        self._core_graph.add_edge(extractor_agent.name, wh_agent.name)
        self._core_graph.add_edge(extractor_agent.name, distancing_agent.name)
        self._core_graph.add_edge(completion_agent.name, completion_refiner_agent.name)
        self._core_graph.add_edge(
            [
                completion_refiner_agent.name,
                recall_agent.name,
                open_ended_agent.name,
                wh_agent.name,
                distancing_agent.name,
            ],
            aggregator_agent.name,
        )

        self._core_graph.set_finish_point(aggregator_agent.name)
        # self._core_graph.add_edge(aggregator_agent.name, edition_critic_agent.name)

        # self._core_graph.add_conditional_edges(
        #     "edition_critic",
        #     self.route_edition,
        #     {
        #         "questioner_editor": "questioner_editor",
        #         END: END,
        #     },
        # )

        return self._core_graph.compile()
