from langchain.messages import HumanMessage

from agents.core.base_agent import Agent
from agents.core.base_lm_config import LMConfiguration
from roles.personalization.planner import PlannerRole


class PlannerAgent(Agent):
    """
    Agent that plans the personalization of a story.
    """

    def __init__(
        self,
        lm_config: LMConfiguration | None = None,
    ):
        super().__init__(
            name="planner",
            roles=[PlannerRole()],
            lm_config=lm_config,
        )

    def pre_core(self, data: dict) -> dict:
        last_message = data["messages"][-1].content
        request = HumanMessage(
            "Hazlo para esto. Se creativo pero coherente: \n"
            + last_message
        )

        return {"messages": [request]}
