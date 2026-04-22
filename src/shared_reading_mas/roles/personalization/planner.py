from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import (
    LastMessagePermission,
)


class PlannerRole(LangFuseRole):
    """
    Role that plans the personalization of a story.
    """

    def __init__(self):
        super().__init__(
            name="planner",
            permissions=[LastMessagePermission()],
            activities=[],
        )
