from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import LastMessagePermission
from shared_reading_mas.roles.questions.types import (
    COMPLETION_TYPE,
    RECALL_TYPE,
    OPEN_ENDED_TYPE,
    WH_TYPE,
    DISTANCING_TYPE
)

class CombinedRole(LangFuseRole):
    """
    Role that personalizes the responses based on user preferences.
    """

    def __init__(self):
        super().__init__(
            name="combined",
            permissions=[LastMessagePermission()],
            activities=[],
        )

        types = [
            COMPLETION_TYPE,
            RECALL_TYPE,
            OPEN_ENDED_TYPE,
            WH_TYPE,
            DISTANCING_TYPE
        ]

        description = "".join(f"- **{type.type}**: {type.description}\n" for type in types)
        tips = "".join(f"**{type.type}**: \n {"".join(f"- {indicator}\n" for indicator in type.indicators) }" for type in types)

        self.configure({
            "description": description,
            "tips": tips
        })

