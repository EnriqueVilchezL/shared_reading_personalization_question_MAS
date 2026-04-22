from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import (
    LastMessagePermission,
)


class ExtractorRole(LangFuseRole):
    """
    Role that extracts aspects of a story.
    """

    def __init__(self):
        super().__init__(
            name="questions_extractor",
            permissions=[LastMessagePermission()],
            activities=[],
        )
