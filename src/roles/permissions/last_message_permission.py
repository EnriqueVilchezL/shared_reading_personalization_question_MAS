from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from roles.core.base_permission import Permission


class LastMessagePermission(Permission):
    """
    Permission that restricts access to last LangGraph message only.
    """

    def __init__(self):
        super().__init__(name="last_message")

    def apply(self, data: any) -> any:
        coppied_data = dict(data)
        if len(data["messages"]) > 0:
            coppied_data["messages"] = [RemoveMessage(id=REMOVE_ALL_MESSAGES), data["messages"][-1]]
        return coppied_data
