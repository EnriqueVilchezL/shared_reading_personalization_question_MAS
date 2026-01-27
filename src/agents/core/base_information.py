from langchain.agents import AgentState


class Information(AgentState):
    lm_configs: dict[str, dict]
    """
    Language model configurations for the agents.
    """
