from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import (
    LastMessagePermission,
)
from shared_reading_mas.roles.questions.types import COMPLETION_TYPE


class CompletionRefinerRole(LangFuseRole):
    """
    Role that creates completion questions for a story.
    """

    def __init__(self):
        super().__init__(
            name="completion_refiner",
            permissions=[LastMessagePermission()],
            activities=[],
        )

        self.prompt = COMPLETION_TYPE
