from roles.langfuse_role import LangFuseRole
from roles.permissions.last_message_permission import LastMessagePermission


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
