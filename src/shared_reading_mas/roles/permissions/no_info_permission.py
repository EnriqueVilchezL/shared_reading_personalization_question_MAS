from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from shared_reading_mas.roles.core.base_permission import Permission


class NoInfoPermission(Permission):
    """
    Permission that restricts access to any LangGraph context.
    """

    def __init__(self):
        super().__init__(name="no_info")

    def apply(self, data: any) -> any:
        coppied_data = dict(data)
        coppied_data["messages"] = [RemoveMessage(id=REMOVE_ALL_MESSAGES)]
        return coppied_data
