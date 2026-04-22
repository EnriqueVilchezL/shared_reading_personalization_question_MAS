from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from roles.core.base_permission import Permission


class LastNMessagesPermission(Permission):
    """
    Permission that restricts access to last N LangGraph messages only.
    """

    def __init__(self, n: int):
        super().__init__(name="last_message")
        self.n = n

    def apply(self, data: any) -> any:
        coppied_data = dict(data)

        if len(data["messages"]) > 0:
            # Messages to keep
            messages_to_keep = data["messages"][-self.n :]
            # Create a new list of messages with a RemoveMessage followed by the messages to keep
            coppied_data["messages"] = [RemoveMessage(id=REMOVE_ALL_MESSAGES)] + messages_to_keep

        return coppied_data
