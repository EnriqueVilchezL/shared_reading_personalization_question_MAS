from abc import ABC
from typing import override

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph_supervisor.handoff import (
    create_handoff_tool,
)
from langgraph_supervisor.supervisor import create_supervisor

from agents.core.base_information import Information
from agents.core.base_lm_config import LMConfiguration
from agents.core.base_organization import Organization
from roles.core.base_role import Role, RoleCollection


def get_llm(lm_config: LMConfiguration):
    """
    Initializes and returns a language model based on the provided configuration.

    Args:
        lm_config (LMConfiguration): The configuration for the language model.

    Returns:
        Language model instance.
    """

    if lm_config.base_provider == "ollama":
        model = init_chat_model(
            model_provider=lm_config.base_provider,
            model=lm_config.base_model,
            base_url=lm_config.base_url,
            temperature=lm_config.temperature,
            reasoning=lm_config.reasoning,
        )

    elif lm_config.base_provider == "inferencer":
        model = init_chat_model(
            model_provider="openai",
            model=lm_config.base_model,
            base_url=lm_config.base_url,
            temperature=lm_config.temperature,
            api_key=lm_config.api_key,
        )

    return model

class Agent(ABC):
    name: str
    """
    Name of the agent.
    """

    roles: RoleCollection
    """
    List of roles assigned to the agent.
    """

    lm_config: LMConfiguration
    """
    Language model configuration for the agent.
    """

    organization: Organization
    """
    Organization the agent belongs to.
    """

    information_schema: Information
    """
    Information schema for the agent.
    """

    def __init__(
        self,
        name: str,
        roles: list[Role] | RoleCollection | None = None,
        lm_config: LMConfiguration | None = None,
        organization: Organization | None = None,
        information_schema: type[Information] | None = None,
    ):
        """
        Initializes the agent with the given roles.
        """
        self.name = name
        self.roles = (
            roles
            if isinstance(roles, RoleCollection)
            else RoleCollection(roles)
            if roles is not None
            else RoleCollection()
        )
        self.lm_config = lm_config or LMConfiguration()
        self.organization = organization
        self.information_schema = information_schema or Information

    def add_organization(self, organization: Organization):
        """
        Assigns the organization to the agent.

        Args:
            organization (Organization): The organization to assign.
        """
        self.organization = organization

    def set_role_variables(self, data: dict):
        """
        Sets the role variables for the agent with the given data.

        Args:
            data (dict): The data to set to the agent.
        """
        self.instructions = self.roles.set_variables(data)

    def pre_core(self, data: dict) -> dict:
        """
        Prepares the agent for the core processing.

        Args:
            data (dict): The information data for the agent.

        Returns:
            dict: The prepared information data.
        """
        return {}

    def apply_permissions(self, data: dict) -> dict:
        """
        Applies the role permissions to the data.

        Args:
            data (dict): The information data for the agent.

        Returns:
            dict: The information data with permissions applied.
        """
        data = self.roles.apply_permissions(data.copy())
        return {"messages": data.get("messages", [])}

    def post_core(self, data: dict) -> dict:
        """
        Post-processes the information data after core processing.

        Args:
            data (dict): The information data for the agent.

        Returns:
            dict: The post-processed information data.
        """
        messages = data.get("messages", [])

        if messages and isinstance(messages[-1], AIMessage):
            messages[-1].name = self.name

        return {}

    def core(self) -> CompiledStateGraph:
        """
        Instantiates the agent.

        Args:
            system_prompt (str): The system prompt for the agent.

        Returns:
            CompiledStateGraph: The compiled state graph for the agent.
        """
        model = get_llm(self.lm_config)

        for protocol in self.roles.protocols:
            handoff_tool = create_handoff_tool(
                agent_name=protocol, add_handoff_messages=True
            )
            self.roles.activities.add(handoff_tool)

        agent = create_agent(
            model=model,
            name=self.name,
            system_prompt=self.instructions,
            tools=self.roles.activities,
            state_schema=self.organization.information_schema
            if self.organization
            else self.information_schema,
        )

        return agent

    def instanciate(self) -> CompiledStateGraph:
        """
        Invokes the agent with the given data.

        Args:
            data (dict): The information data for the agent.
        Returns:
            CompiledStateGraph: The compiled state graph for the agent.
        """
        graph = StateGraph(
            state_schema=self.organization.information_schema
            if self.organization
            else self.information_schema
        )
        graph.add_node(self.name + "_pre", self.pre_core)
        graph.add_node(self.name + "_permissions", self.apply_permissions)
        graph.add_node(self.name + "_agent", self.core())
        graph.add_node(self.name + "_post", self.post_core)
        graph.add_edge(self.name + "_pre", self.name + "_permissions")
        graph.add_edge(self.name + "_permissions", self.name + "_agent")
        graph.add_edge(self.name + "_agent", self.name + "_post")
        graph.set_entry_point(self.name + "_pre")
        graph.set_finish_point(self.name + "_post")
        agent = graph.compile()
        return agent


class Supervisor(Agent):
    """
    Supervisor agent that oversees other agents.
    """

    def __init__(
        self,
        name: str,
        roles: list[Role] | None = None,
        lm_config: LMConfiguration | None = None,
        organization: Organization | None = None,
    ):
        super().__init__(name, roles, lm_config, organization)

    @override
    def core(self) -> CompiledStateGraph:
        model = init_chat_model(
            model_provider=self.lm_config.base_provider,
            model=self.lm_config.base_model,
            temperature=self.lm_config.temperature,
        )

        supervised_agents = []
        for protocol in self.roles.protocols:
            agent = self.organization.get_agent(protocol)
            if agent:
                supervised_agents.append(agent)

        agent = create_supervisor(
            model=model,
            agents=supervised_agents,
            tools=self.roles.activities,
            state_schema=self.organization.information_schema,
        ).compile()

        return agent
