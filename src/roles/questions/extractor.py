from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission


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
