from shared_reading_mas.roles.langfuse_role import LangFuseRole
from shared_reading_mas.roles.permissions.last_message_permission import (
    LastMessagePermission,
)


class ImageEditorRole(LangFuseRole):
    """
    Role that edits images.
    """

    def __init__(self):
        super().__init__(
            name="personalization_image_editor",
            permissions=[LastMessagePermission()],
            activities=[],
        )
