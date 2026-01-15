from langchain_core.messages import SystemMessage

from roles.core.base_permission import Permission


class NoSystemPromptsPermission(Permission):
    """
    Permission that restricts access to any system prompts in LangGraph context.
    """

    def __init__(self):
        super().__init__(name="no_info")

    def apply(self, data: any) -> any:
        # Remove any system prompts or context information
        coppied_data = dict(data)
        coppied_data["messages"] = [
            m for m in coppied_data["messages"] if not isinstance(m, SystemMessage)
        ]
        return coppied_data
