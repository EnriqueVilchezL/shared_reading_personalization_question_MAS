from abc import ABC, abstractmethod

from langgraph.graph.state import StateGraph

from agents.core.base_information import Information


class Organization(ABC):
    """
    Abstract base class for organizations.
    """

    name: str
    """
    Name of the organization.
    """

    agents: list[any]
    """
    List of agents in the organization.
    """

    information_schema: Information
    """
    Information schema for the organization.
    """

    configuration: dict
    """
    Configuration for the organization.
    """

    _agents_variables: dict

    def __init__(self, name: str, information_schema: type[Information] = Information, configuration: dict = {}):
        """
        Initializes the organization with the given name and information schema.

        Args:
            name (str): The name of the organization.
            information_schema (type[Information]): The information schema for the organization.
            configuration (dict): The configuration for the organization.
        """
        self.name = name
        self.agents = []
        self.information_schema = information_schema
        self._core_graph = StateGraph(state_schema=information_schema)
        self.configuration = configuration
        self.set_agents_variables({})


    def set_agents_variables(self, data: dict):
        """
        Sets the variables for all agents in the organization with the given data.

        Args:
            data (dict): The data to set to the agents.
        """
        self._agents_variables = data

    def add_agent(self, agent: any):
        """
        Adds an agent to the organization.

        Args:
            agent (any): The agent to add.
        """
        agent.add_organization(self)

        if agent.name in self._agents_variables:
            agent.set_role_variables(self._agents_variables[agent.name])
        else:
            agent.set_role_variables({})

        self.agents.append(agent)
        self._core_graph.add_node(agent.name, agent.instanciate())

    def get_agent(self, name: str) -> any:
        """
        Retrieves an agent from the organization by name.

        Args:
            name (str): The name of the agent to retrieve.

        Returns:
            Agent | None: The agent if found, otherwise None.
        """
        for agent in self.agents:
            if agent.name == name:
                return agent

        return None

    @abstractmethod
    def instantiate(self):
        """
        Instantiates all agents in the organization.
        """
        ...

